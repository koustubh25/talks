#!/usr/bin/env python3
"""The Southbank Vault: live left-pane renderer.

Reads events (one JSON object per line) from the stage's .vault/events.jsonl and
animates the agent's attempts against the vault's defences, in pixel art.

  render.py --round 3                      live: follow the stage's event log
  render.py --round 3 --scenario           rehearse: loop the scripted round 3
  render.py --round 3 --snapshot out.svg --at 10.5 --size 110x46
                                           offline: one frame of the scripted round as SVG
Round ids: 0 1 2 A 3 B 4 4+ C 5 F
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import time

from PIL import Image
from rich.console import Console
from rich.live import Live
from rich.text import Text

HERE = os.path.dirname(os.path.abspath(__file__))
SPRITE_DIR = os.path.join(HERE, "sprites")
sys.path.insert(0, HERE)
import paths  # noqa: E402
from rounds import ROUNDS, norm  # noqa: E402
from scenarios import SCENARIOS  # noqa: E402

# ---------------------------------------------------------------- palette
C = {
    "bg": "#000000", "ink": "#E9E4DC", "dim": "#8D8590", "ghost": "#4A4250", "title": "#FFD79A",
    "cream": "#FFE0B2", "cocoa": "#D7A86E", "cyan": "#7FDBFF", "pink": "#F7A8D8",
    "yellow": "#FFF59D", "purple": "#CE93D8", "orange": "#FFB74D", "red": "#FF6E6E",
    "blue": "#81D4FA", "mint": "#A5D6A7", "green": "#9CCC65", "coral": "#FF8A65",
    "teal": "#80CBC4", "lavender": "#B39DDB", "gold": "#FFE082",
}

# ---------------------------------------------------------------- walls
# slot 0 is the outermost ring, slot 3 the innermost (next to the vault)
WALL_INFO = {
    "sign":      {"slot": 0, "label": "THE SIGN · AGENTS.md",            "color": "yellow",   "style": "dashed", "key": "the model"},
    "rope":      {"slot": 1, "label": "THE VELVET ROPE · --deny-tool",   "color": "purple",   "style": "solid",  "key": "you"},
    "urlrule":   {"slot": 3, "label": "THE DOOR LIST · --deny-url",      "color": "purple",   "style": "solid",  "key": "you"},
    "bouncer":   {"slot": 2, "label": "THE BOUNCER · preToolUse hook",   "color": "orange",   "style": "heavy",  "key": "you/team"},
    "judge":     {"slot": 2, "label": "THE AI DOORMAN · assisted judge", "color": "lavender", "style": "dashed", "key": "a model"},
    "lasers":    {"slot": 3, "label": "THE LASER GRID · sandbox",        "color": "red",      "style": "double", "key": "you"},
    "netlasers": {"slot": 2, "label": "THE LASER GRID · sandbox network", "color": "red",     "style": "double", "key": "you"},
}
BLOCKER_NAME = {"rope": "rope", "bouncer": "bouncer", "judge": "AI doorman", "url": "door list", "os": "OS", "hq": "HQ"}
BLOCKER_WALLS = {"rope": ["rope"], "url": ["urlrule"], "bouncer": ["bouncer"], "judge": ["judge"],
                 "os": ["lasers", "netlasers"], "hq": ["lasers", "netlasers"]}
FILE_TOOLS = {"view", "read", "grep", "rg", "glob", "create", "edit", "str_replace_editor", "apply_patch", "write"}
PROPS = {"A": ("menu", "THE MENU", "teal"), "B": ("judge", "AI DOORMAN", "lavender"),
         "C": ("takeaway", "NO TAKEAWAYS", "cocoa"), "5": ("hq", "HQ", "blue"), "F": ("gate", "TWO KEYS", "gold"),
         "4+": ("recipe", "ENV COPY", "cream")}

MIN_W, MIN_H = 80, 27
EMBEDDED = False  # inside a presenterm slide box: no keys, no "q" hint

BOX = {  # h, v, tl, tr, bl, br
    "dashed": ("╌", "┆", "┌", "┐", "└", "┘"),
    "solid":  ("─", "│", "┌", "┐", "└", "┘"),
    "heavy":  ("━", "┃", "┏", "┓", "┗", "┛"),
    "double": ("═", "║", "╔", "╗", "╚", "╝"),
    "ghost":  ("┄", "┊", "┌", "┐", "└", "┘"),
}


# ---------------------------------------------------------------- sprites
def load_sprite(name):
    im = Image.open(os.path.join(SPRITE_DIR, f"{name}.png")).convert("RGBA").resize((16, 16), Image.NEAREST)
    px = im.load()
    return [[px[x, y] for x in range(16)] for y in range(16)]


SPRITES = {n: load_sprite(n) for n in
           ["agent", "disguise", "presenter", "cup", "recipe", "alarm", "door", "hq", "trophy",
            "menu", "judge", "takeaway", "gate", "globe"]}


def hexc(rgb, dim=1.0):
    return "#%02X%02X%02X" % tuple(int(v * dim) for v in rgb[:3])


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.cells = [[(" ", C["ink"], C["bg"], False) for _ in range(w)] for _ in range(h)]

    def put(self, x, y, ch, fg=None, bg=None, bold=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            _, ofg, obg, _ = self.cells[y][x]
            self.cells[y][x] = (ch, fg or ofg, bg or obg, bold)

    def text(self, x, y, s, fg=None, bold=False, maxw=None):
        if maxw is not None and len(s) > maxw:
            s = s[:max(0, maxw - 1)] + "…"
        for i, ch in enumerate(s):
            self.put(x + i, y, ch, fg, None, bold)

    def sprite(self, x, y, spr, dim=1.0):
        """Draw a 16x16 sprite as 16 columns x 8 rows of half blocks."""
        for r in range(8):
            for c in range(16):
                top, bot = spr[2 * r][c], spr[2 * r + 1][c]
                if top[3] == 0 and bot[3] == 0:
                    continue
                if top[3] and bot[3]:
                    self.put(x + c, y + r, "▀", hexc(top, dim), hexc(bot, dim))
                elif top[3]:
                    self.put(x + c, y + r, "▀", hexc(top, dim), C["bg"])
                else:
                    self.put(x + c, y + r, "▄", hexc(bot, dim), C["bg"])

    def box(self, x0, y0, w, h, style, color, gap_rows=(), label=None, label_color=None):
        hc, vc, tl, tr, bl, br = BOX[style]
        for x in range(x0 + 1, x0 + w - 1):
            self.put(x, y0, hc, color)
            self.put(x, y0 + h - 1, hc, color)
        for y in range(y0 + 1, y0 + h - 1):
            if y not in gap_rows:
                self.put(x0, y, vc, color)
            self.put(x0 + w - 1, y, vc, color)
        for (x, y, ch) in [(x0, y0, tl), (x0 + w - 1, y0, tr), (x0, y0 + h - 1, bl), (x0 + w - 1, y0 + h - 1, br)]:
            self.put(x, y, ch, color)
        if label:
            self.text(x0 + 2, y0, f" {label} ", label_color or color, bold=True, maxw=w - 4)

    def signature(self):
        return hash(tuple(tuple(row) for row in self.cells))

    def to_text(self):
        out = Text()
        for y, row in enumerate(self.cells):
            run, style = "", None
            for ch, fg, bg, bold in row:
                st = f"{'bold ' if bold else ''}{fg} on {bg}"
                if st != style and run:
                    out.append(run, style)
                    run = ""
                style = st
                run += ch
            if run:
                out.append(run, style)
            if y < self.h - 1:
                out.append("\n")
        return out


# ---------------------------------------------------------------- state
class Arrow:
    def __init__(self, ev, now, lane):
        self.id = ev.get("id")
        self.detail = ev.get("detail", "")
        self.actor = ev.get("actor", "agent")
        self.disguise = bool(ev.get("disguise"))
        self.out = ev.get("dir") == "out"
        self.lane = lane
        self.start = now
        self.outcome = None      # None while acting; blocked | leak | ok | allowed | fizzle
        self.by = None
        self.result_at = None
        self.head = None         # current head x (set at first draw)


class State:
    def __init__(self, round_id, variant=""):
        self.round = round_id
        self.variant = variant
        self.arrows = []
        self.feed = []           # arrows, newest last
        self.orphans = {}        # results that arrived before their attempt
        self.mode = "idle"       # idle | thinking | acting
        self.mode_since = 0.0
        self.attempt_no = 0
        self.score_agent = 0
        self.score_vault = 0
        self.leak_at = None
        self.stopped_at = None
        self.bypass = None       # (status, since): asking | denied | approved
        self.helpers = 0
        self.lane_i = 0

    @property
    def r(self):
        return ROUNDS[self.round]

    def apply(self, ev, now):
        kind = ev.get("kind")
        if kind == "reset":
            self.__init__(norm(ev.get("round", self.round)) or self.round, ev.get("variant", "") or "")
        elif kind == "prompt":
            self.mode, self.mode_since, self.stopped_at = "thinking", now, None
        elif kind == "attempt":
            self.attempt_no += 1
            tool = ev.get("tool", "")
            if ev.get("dir") == "out":
                lane = self.lane_i % 4
            elif tool in FILE_TOOLS:
                lane = 0
            else:
                lane = 1 + self.lane_i % 3
            self.lane_i += 1
            a = Arrow(ev, now, lane)
            self.arrows.append(a)
            self.feed.append(a)
            self.arrows = self.arrows[-4:]
            self.feed = self.feed[-5:]
            self.mode, self.mode_since, self.stopped_at = "acting", now, None
            if a.id in self.orphans:
                self.apply(self.orphans.pop(a.id), now)
        elif kind == "result":
            match = [a for a in self.arrows if a.id == ev.get("id") and a.outcome is None]
            if not match and not any(a.id == ev.get("id") for a in self.feed):
                self.orphans[ev.get("id")] = ev
                return
            for a in match:
                a.outcome, a.by, a.result_at = ev.get("outcome"), ev.get("by"), now
                if ev.get("disguise"):
                    a.disguise = True
                if a.outcome == "leak" and self.counts_as_leak(a):
                    self.score_agent += 1
                    self.leak_at = now
                elif a.outcome == "allowed":
                    self.score_agent += 1
                    self.leak_at = now
                elif a.outcome == "blocked":
                    self.score_vault += 1
            self.mode, self.mode_since = "thinking", now
        elif kind == "bypass_request":
            self.bypass = ("asking", now)
            self.mode, self.mode_since = "thinking", now
        elif kind == "bypass_denied":
            self.bypass = ("denied", now)
            self.score_vault += 1
        elif kind == "bypass_approved":
            self.bypass = ("approved", now)
        elif kind == "helper":
            self.helpers = max(0, self.helpers + int(ev.get("delta", 1)))
        elif kind == "stop":
            for a in self.arrows:
                if a.outcome is None:
                    a.outcome, a.result_at = "fizzle", now
            self.mode, self.mode_since, self.stopped_at = "idle", now, now

    def counts_as_leak(self, a):
        """In Round C reading the recipe is allowed: only taking it out of the café counts."""
        return a.out or not self.r.get("exfil")

    def leaks(self):
        return sum(1 for a in self.feed if (a.outcome == "leak" and self.counts_as_leak(a)) or a.outcome == "allowed")


# ---------------------------------------------------------------- drawing
def layout(w, h):
    ix = 4 if w >= 98 else 3 if w >= 90 else 2
    iy = 2 if h >= 41 else 1
    vw, vh = 40, (12 if h >= 33 else 11)  # compact for short panes
    sx, sy = 24, 4
    boxes = []
    for k in range(5):  # slots 0..3, 4 = vault
        boxes.append((sx + k * ix, sy + k * iy, vw + 2 * (4 - k) * ix, vh + 2 * (4 - k) * iy))
    vx, vy, _, _ = boxes[4]
    cy = vy + vh // 2
    lanes = [cy - 3, cy - 1, cy + 1, cy + 3]
    gap = set(range(cy - 2, cy + 5))
    scene_bottom = boxes[0][1] + boxes[0][3]
    return {"ix": ix, "iy": iy, "boxes": boxes, "vx": vx, "vy": vy, "vw": vw, "vh": vh, "cy": cy,
            "lanes": lanes, "gap": gap, "scene_bottom": scene_bottom, "agent_xy": (2, cy - 4),
            "right": boxes[0][0] + boxes[0][2]}


def active_walls(state):
    return state.r["walls"]


def wall_box(L, name):
    return L["boxes"][WALL_INFO[name]["slot"]]


def blocker_wall(state, by):
    for name in BLOCKER_WALLS.get(by, []):
        if name in active_walls(state):
            return name
    return None


def hold_x(L, state, a):
    """Where an in-flight arrow waits for its result: the first hard wall on its lane."""
    walls = active_walls(state)
    y = L["lanes"][a.lane]
    order = ["rope", "urlrule", "bouncer", "judge", "lasers", "netlasers"]
    if a.out:  # outbound: from the vault outwards, innermost wall first
        hard = [n for n in order if n in walls]
        if hard:
            bx, _, bw, _ = wall_box(L, max(hard, key=lambda n: WALL_INFO[n]["slot"]))
            return bx + bw
        return L["right"] + 1
    for name in order:
        if name in walls and not (name == "rope" and y in L["gap"]) and name not in ("urlrule", "netlasers"):
            return wall_box(L, name)[0] - 1
    return L["vx"] - 1


def target_x(L, state, a, w):
    if a.out:
        if a.outcome == "blocked":
            name = blocker_wall(state, a.by)
            if name:
                bx, _, bw, _ = wall_box(L, name)
                return bx + bw
            return L["right"]
        if a.outcome == "leak":
            return w - 3
        return L["right"]
    if a.outcome == "blocked":
        name = blocker_wall(state, a.by)
        return (wall_box(L, name)[0] - 1) if name else L["vx"] - 1
    if a.outcome == "leak":
        return L["vx"] + 3
    return L["vx"] - 1  # ok / fizzle: reached the vault wall, found nothing


def hq_lines():
    """Live view of the admin's managed settings file (Round 5)."""
    try:
        with open(paths.managed_settings()) as f:
            m = json.load(f)
    except FileNotFoundError:
        return False, ["managed-settings.json: not found", "(sudo ./demo hq on)"]
    except (OSError, ValueError):
        return False, ["managed-settings.json: unreadable"]
    sb, perm = m.get("sandbox", {}), m.get("permissions", {})
    checks = [("sandbox.enabled: true", sb.get("enabled") is True),
              ("sandbox.allowBypass: false", sb.get("allowBypass") is False),
              ("allow-all / --yolo: disabled", perm.get("disableBypassPermissionsMode") == "disable")]
    return all(ok for _, ok in checks), [("✓ " if ok else "✗ ") + t for t, ok in checks]


def draw(state, now, w, h):
    cv = Canvas(w, h)
    r = state.r
    walls = active_walls(state)
    if w < MIN_W or h < MIN_H:
        cv.text(1, 1, f"Enlarge the pane to at least {MIN_W}x{MIN_H} (now {w}x{h})", C["coral"], True)
        return cv
    L = layout(w, h)
    blink = int(now * 4) % 2 == 0
    hq = bool(r.get("hq"))

    # header
    cv.text(1, 0, "SOUTHBANK VAULT", C["title"], True)
    rt = f"ROUND {state.round} · {r['title']}"
    cv.text(w - len(rt) - 1, 0, rt, C["title"], True)
    x = 1
    for name in walls:
        info = WALL_INFO[name]
        chip = f"[{name}]"
        cv.text(x, 1, chip, C[info["color"]], True)
        x += len(chip) + 1
    if hq:
        cv.text(x, 1, "[HQ]", C["blue"], True)
    if state.round != "0":
        score = f"Agent {state.score_agent} : {state.score_vault} Vault"
        cv.text(w - len(score) - 1, 1, score, C["ink"], True)
    for xx in range(w):
        cv.put(xx, 2, "─", C["ghost"])

    # walls (outermost first); empty slots are ghosted
    leaking = state.leak_at is not None and now - state.leak_at < 3.0
    by_slot = {WALL_INFO[n]["slot"]: n for n in walls}
    for slot in range(4):
        bx, by, bw, bh = L["boxes"][slot]
        name = by_slot.get(slot)
        if name:
            info = WALL_INFO[name]
            label = info["label"]
            if name == "lasers" and hq:
                label += " · MANAGED BY HQ"
            cv.box(bx, by, bw, bh, info["style"], C[info["color"]],
                   gap_rows=L["gap"] if name == "rope" else (), label=label,
                   label_color=C["blue"] if (name == "lasers" and hq) else None)
        elif state.round != "0":
            cv.box(bx, by, bw, bh, "ghost", C["ghost"])

    # the vault
    vx, vy, vw, vh = L["boxes"][4]
    won = state.stopped_at is not None and state.attempt_no > 0 and state.leaks() == 0
    vault_color = C["coral"] if (leaking and blink) else C["mint"]
    cv.box(vx, vy, vw, vh, "solid", vault_color)
    cv.sprite(vx + 3, vy + 1, SPRITES["trophy" if won else "cup"])
    if state.leaks():
        cv.sprite(vx + 21, vy + 1, SPRITES["alarm"])
        msg = "IT LEFT THE CAFÉ!" if r.get("exfil") else "SPILLED THE BEANS!"
        cv.text(vx + (vw - len(msg)) // 2, vy + vh - 2, msg, C["coral"], True)
    else:
        cv.sprite(vx + 21, vy + 1, SPRITES["recipe"])
        msg = "VAULT WINS THIS ROUND" if won else "SECRET CAPPUCCINO RECIPE"
        cv.text(vx + (vw - len(msg)) // 2, vy + vh - 2, msg, C["gold"] if won else C["cream"], True)

    # the attacker
    ax, ay = L["agent_xy"]
    last = state.arrows[-1] if state.arrows else None
    if hq or (last and last.actor == "presenter"):
        actor, acolor = "presenter", C["green"]
    elif last and last.disguise and (last.outcome is None or now - (last.result_at or now) < 2):
        actor, acolor = "disguise", C["pink"]
    else:
        actor, acolor = "agent", C["cyan"]
    if state.round != "0":
        cv.sprite(ax, ay, SPRITES[actor], dim=1.0 if state.mode != "idle" or hq else 0.6)
        name = {"agent": "COPILOT", "disguise": "COPILOT (disguised)", "presenter": "YOU"}[actor]
        if state.helpers and actor != "presenter":
            name += f" +{state.helpers}"
        cv.text(ax, ay + 8, name, acolor, True, maxw=22)

    # the round's prop, above the attacker when there is room
    prop = PROPS.get(state.round)
    if prop and ay - 4 >= 9:
        spr, cap, col = prop
        py = ay - 10 if ay - 10 >= 3 else 3
        cv.sprite(2, py, SPRITES[spr], dim=0.85)
        cv.text(2, py + 8, cap, C[col], True, maxw=21)

    # thinking: bubble, pulsing aim line, timer
    if state.mode == "thinking" and state.round != "0" and not hq:
        dots = "·" * (1 + int(now * 3) % 3)
        cv.text(ax + 4, ay - 1, f"( {dots:<3} )", C["ink"])
        lane_y = L["lanes"][0]
        aim_color = C["cyan"] if blink else C["ghost"]
        probe = Arrow({}, now, 0)
        for xx in range(ax + 17, hold_x(L, state, probe)):
            if xx % 2 == 0:
                cv.put(xx, lane_y, "╌", aim_color)
        secs = int(now - state.mode_since)
        cv.text(ax, ay + 9, f"planning #{state.attempt_no + 1}… {secs}s", C["dim"], maxw=22)
    elif state.mode == "acting":
        cv.text(ax, ay + 9, "attacking…" if not hq else "trying…", C["dim"])

    # Round A: the shell is off the menu
    if r.get("menu"):
        for lane_y in L["lanes"][1:]:
            cv.text(ax + 18, lane_y, "✗ shell: off the menu", C["ghost"])

    # Round C: where the takeaways go
    if r.get("exfil"):
        lbl = "recipes.example.com"
        cv.text(w - len(lbl) - 1, L["boxes"][0][1] - 1, lbl, C["blue"], True)
        cv.text(w - 3, L["cy"], "◉", C["blue"], True)

    # arrows
    for a in state.arrows:
        y = L["lanes"][a.lane]
        start = (vx + vw) if a.out else ax + 17
        goal = hold_x(L, state, a) if a.outcome is None else target_x(L, state, a, w)
        if a.head is None:
            a.head = float(start)
        step = 90.0 * 0.05
        a.head = min(float(goal), a.head + step) if a.head < goal else float(goal)
        age = now - (a.result_at or now)
        fade = 1.0 if a.outcome is None or age < 3 else 0.5
        base = C["pink"] if a.disguise else (C["green"] if a.actor == "presenter" else C["cyan"])
        col = base if fade == 1.0 else C["dim"]
        head = int(a.head)
        for xx in range(start, head):
            cv.put(xx, y, "─", col)
        if a.outcome is None:
            cv.put(head, y, "▶", C["ink"] if blink else col, bold=True)
        elif head >= int(goal):
            if a.outcome == "blocked":
                cv.put(head, y, "×", C["green"], bold=True)
                if a.out:
                    tag = f"× {BLOCKER_NAME.get(a.by, a.by)}"
                    tx = start + 1
                else:
                    tag = f"blocked · {BLOCKER_NAME.get(a.by, a.by)}"
                    tx = max(start, head - len(tag))
                cv.text(tx, y - 1, tag, C["green"] if fade == 1 else C["dim"], True)
            elif a.outcome in ("leak", "allowed"):
                cv.put(head, y, "▶", C["coral"] if state.counts_as_leak(a) else C["cream"], bold=True)
            elif a.outcome == "ok":
                cv.put(head, y, "·", C["dim"])
            else:
                cv.put(head, y, "~", C["dim"])
        else:
            cv.put(head, y, "▶", col, bold=True)
        if a.head < goal or a.outcome is None:
            lbl = a.detail if len(a.detail) <= 22 else a.detail[:21] + "…"
            cv.text(start + 1, y + 1, lbl, C["dim"])

    # how the last leak got in: make the soft walls' failure visible
    last_leak = next((a for a in reversed(state.feed)
                      if a.outcome == "leak" and state.counts_as_leak(a) and now - (a.result_at or now) < 10), None)
    if last_leak and not (state.bypass and now - state.bypass[1] < 6):
        how = []
        if "sign" in walls:
            how.append(("ignored the sign", "yellow"))
        if "rope" in walls:
            how.append(("went around the rope (shell)" if last_leak.lane else "past the rope", "purple"))
        if "bouncer" in walls:
            how.append(("fooled the bouncer" + (" (disguise)" if last_leak.disguise else ""), "orange"))
        if "judge" in walls:
            how.append(("talked past the AI doorman", "lavender"))
        if "lasers" in walls:
            how.append(("the sandbox didn't cover it", "red"))
        if "urlrule" in walls or "netlasers" in walls:
            how.append(("out through a gap", "red"))
        how.reverse()  # innermost (newest) defence first, in case the line is cut
        x = 1
        cv.text(x, L["scene_bottom"], "Got in: ", C["coral"], True)
        x += 8
        for i, (txt, col) in enumerate(how):
            seg = ("· " if i else "") + txt + " "
            if x + len(seg) >= w:
                break
            cv.text(x, L["scene_bottom"], seg, C[col], True)
            x += len(seg)

    # sandbox escape door (Round 4)
    if state.bypass:
        status, since = state.bypass
        dx, dy = ax + 3, ay + 10  # under the agent, clear of the walls
        if (status == "asking" or now - since < 4) and dy + 8 <= L["scene_bottom"]:
            cv.sprite(dx, dy, SPRITES["door"])
        cap_y = L["scene_bottom"]
        if status == "asking":
            cv.text(ax, cap_y, "\"Can I step outside the lasers?\"", C["yellow"], True)
        elif status == "denied" and now - since < 6:
            cv.text(ax, cap_y, "NO. The vault stays shut.", C["green"], True)
        elif status == "approved" and now - since < 6:
            cv.text(ax, cap_y, "A human said YES: sandbox bypassed.", C["coral"], True)

    # round 0 caption
    if state.round == "0":
        cap = "Southbank Roasters' Secret Cappuccino Recipe. Who can protect it?"
        cv.text(max(1, (w - len(cap)) // 2), vy + vh + 2, cap, C["title"], True)
        return cv

    # feed and counters
    fy = L["scene_bottom"] + 1
    avail = h - fy                       # rows left for feed, counters and the strip
    n_feed = min(5, max(1, avail - 4))
    cv.text(1, fy, "Feed", C["dim"], True)
    for i, a in enumerate(state.feed[-n_feed:]):
        y = fy + 1 + i
        lbl = ("→ " if a.out else "") + a.detail
        cv.text(3, y, lbl, C["ink"], maxw=30)
        if a.outcome is None:
            st, col = "…" + ("trying" if a.actor == "presenter" else "attacking"), C["dim"]
        elif a.outcome == "blocked":
            st, col = f"× blocked · {BLOCKER_NAME.get(a.by, a.by)}", C["green"]
        elif a.outcome == "allowed":
            st, col = "! NOT BLOCKED", C["coral"]
        elif a.outcome == "leak" and not state.counts_as_leak(a):
            st, col = "· read it (still inside)", C["cream"]
        elif a.outcome == "leak":
            st, col = ("! OUT THE DOOR" if a.out else "! SPILLED THE BEANS") + (" (disguised)" if a.disguise else ""), C["coral"]
        elif a.outcome == "ok":
            st, col = "· ran, nothing found", C["dim"]
        else:
            st, col = "~ fizzled", C["dim"]
        cv.text(34, y, st, col, True, maxw=max(10, (w - 42 if w >= 100 else w - 35)))
    attempts = len(state.feed)
    blocked = len([a for a in state.feed if a.outcome == "blocked"])
    cy2 = fy + 1 + n_feed + (1 if avail - 4 - n_feed >= 1 else 0)
    cv.text(1, cy2, f"Attempts {attempts} · Blocked {blocked} · Leaked {state.leaks()}", C["ink"], True)

    # side panel: the real config behind this round
    if w >= 100:
        px, py = w - 39, fy
        lines = r.get("fix_panel") if (state.variant == "fix" and r.get("fix_panel")) else r.get("panel", [])
        cv.text(px, py, "Config", C["dim"], True)
        if hq:
            ok, extra = hq_lines()
            lines = lines + extra
        for i, line in enumerate(lines[:max(1, min(6, cy2 - fy - 1))]):
            col = C["ink"]
            if line.startswith("✓"):
                col = C["green"]
            elif line.startswith("✗") or "not found" in line:
                col = C["coral"]
            cv.text(px, py + 1 + i, line, col, maxw=38)

    hint = "q: back to slides"
    if h - 1 > cy2 + 2 and not EMBEDDED:
        cv.text(w - len(hint) - 1, h - 1, hint, C["ghost"])

    # keyholder strip
    if cy2 + 2 < h:
        for xx in range(w):
            cv.put(xx, cy2 + 1, "─", C["ghost"])
        x = 1
        cv.text(x, cy2 + 2, "Who can switch it off:", C["dim"], True)
        x += 23
        for name in walls:
            info = WALL_INFO[name]
            who = "HQ only" if (name == "lasers" and hq) else info["key"]
            s = f"{name} → {who}"
            if x + len(s) >= w:
                break
            cv.text(x, cy2 + 2, s, C[info["color"]])
            x += len(s) + 3
        if r.get("finale") and x + 22 < w:
            cv.text(x, cy2 + 2, "github.com → reviewers", C["gold"])
    return cv


def animating(state, now):
    """True while something on screen moves; otherwise the renderer can idle at a low frame rate."""
    if state.mode in ("thinking", "acting"):
        return True
    if state.leak_at is not None and now - state.leak_at < 3.5:
        return True
    if state.bypass and now - state.bypass[1] < 6.5:
        return True
    return any(a.head is None or a.result_at is None or now - a.result_at < 6 for a in state.arrows)


# ---------------------------------------------------------------- event sources
class FileFollower:
    def __init__(self, path):
        self.path, self.pos, self.ino = path, 0, None

    def poll(self):
        try:
            st = os.stat(self.path)
        except FileNotFoundError:
            return []
        if st.st_size < self.pos or (self.ino is not None and st.st_ino != self.ino):
            self.pos = 0  # truncated or replaced: a new round
        self.ino = st.st_ino
        out = []
        with open(self.path) as f:
            f.seek(self.pos)
            for line in f:
                if not line.endswith("\n"):
                    break
                self.pos += len(line.encode())
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return out


class ScenarioPlayer:
    def __init__(self, round_id, t0, loop_gap=4.0):
        self.events, self.t0, self.i, self.loop_gap = SCENARIOS.get(round_id, []), t0, 0, loop_gap
        self.round = round_id

    def poll(self, now):
        out = []
        while self.i < len(self.events) and now - self.t0 >= self.events[self.i][0]:
            out.append(self.events[self.i][1])
            self.i += 1
        if self.events and self.i >= len(self.events) and now - self.t0 > self.events[-1][0] + self.loop_gap:
            self.t0, self.i = now, 0
            out.append({"kind": "reset", "round": self.round})
        return out


class PresenterWatch:
    """Round 5: notice when YOU try to switch HQ's controls off.

    - Watches the process list for copilot started with --yolo / --allow-all* / --no-sandbox.
    - Watches Copilot's session log for a refused /sandbox disable (best effort: the log is internal).
    Events stay in memory: other renderers never see them.
    """
    RISKY = ["--yolo", "--allow-all-tools", "--allow-all", "--no-sandbox", "--allow-all-paths"]

    def __init__(self):
        self.seen_pids, self.n, self.next_poll = set(), 0, 0.0
        self.session_file, self.session_pos = None, 0
        self.last_sandbox_msg = 0.0

    def _attempt(self, detail, blocked):
        self.n += 1
        aid = f"p{self.n}"
        res = {"kind": "result", "id": aid}
        res.update({"outcome": "blocked", "by": "hq"} if blocked else {"outcome": "allowed"})
        return [{"kind": "attempt", "id": aid, "tool": "you", "detail": detail, "actor": "presenter"}, res]

    def _stage_session(self):
        best = None
        for ws in glob.glob(os.path.expanduser("~/.copilot/session-state/*/workspace.yaml")):
            try:
                with open(ws) as f:
                    if f"cwd: {paths.stage()}" not in f.read():
                        continue
                ev = os.path.join(os.path.dirname(ws), "events.jsonl")
                m = os.path.getmtime(ev)
                if best is None or m > best[0]:
                    best = (m, ev)
            except OSError:
                pass
        return best[1] if best else None

    @staticmethod
    def stage_round():
        try:
            with open(os.path.join(paths.stage(), ".vault", "round.json")) as f:
                return json.load(f).get("round")
        except (OSError, ValueError):
            return None

    def poll(self, now):
        if now < self.next_poll:
            return []
        self.next_poll = now + 1.0
        out = []
        live = self.stage_round() == "5"  # the deck runs this from the start: ignore earlier rounds
        hq_on, _ = hq_lines()
        try:
            ps = subprocess.run(["ps", "-axo", "pid=,args="], capture_output=True, text=True, timeout=2).stdout
        except (OSError, subprocess.SubprocessError):
            ps = ""
        for line in ps.splitlines():
            pid, _, args = line.strip().partition(" ")
            words = args.split()
            if not words or not os.path.basename(words[0]).startswith("copilot") or pid in self.seen_pids:
                continue
            flags = [f for f in self.RISKY if any(wd == f or wd.startswith(f + "=") for wd in words)]
            self.seen_pids.add(pid)
            if flags and live:
                out += self._attempt("copilot " + " ".join(flags), blocked=hq_on)
        # the session log, for a refused /sandbox disable
        sf = self._stage_session()
        if sf != self.session_file:
            self.session_file = sf
            self.session_pos = os.path.getsize(sf) if sf else 0  # only new lines
        if sf:
            try:
                with open(sf) as f:
                    f.seek(self.session_pos)
                    chunk = f.read()
                    self.session_pos = f.tell()
            except OSError:
                chunk = ""
            for line in chunk.splitlines():
                low = line.lower()
                if "sandbox" in low and any(k in low for k in ("managed", "organization", "policy", "administrator",
                                                                "required", "refused", "cannot")):
                    if live and now - self.last_sandbox_msg > 5:
                        self.last_sandbox_msg = now
                        out += self._attempt("/sandbox disable", blocked=True)
        return out


class Keys:
    """Read single key presses without blocking (q / Esc: quit, r: replay the log)."""

    def __init__(self):
        self.fd, self.old = None, None
        if sys.stdin.isatty():
            import termios
            import tty
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)

    def wait(self, timeout):
        """Sleep up to TIMEOUT seconds; return the keys pressed meanwhile."""
        if self.fd is None:
            time.sleep(timeout)
            return ""
        import select
        r, _, _ = select.select([self.fd], [], [], timeout)
        return os.read(self.fd, 32).decode(errors="ignore") if r else ""

    def close(self):
        if self.fd is not None:
            import termios
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)


# ---------------------------------------------------------------- main
def snapshot(round_id, path, at, size):
    w, h = (int(v) for v in size.split("x"))
    state = State(round_id)
    t = 0.0
    events = list(SCENARIOS.get(round_id, []))
    frame = None
    while t <= at:
        while events and events[0][0] <= t:
            state.apply(events.pop(0)[1], t)
        frame = draw(state, t, w, h)
        t += 0.05
    console = Console(record=True, width=w, height=h, force_terminal=True, color_system="truecolor",
                      file=open(os.devnull, "w"))
    console.print(frame.to_text())
    console.save_svg(path, title=f"Round {round_id} @ {at}s")
    print("saved", path)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--round", default="1")
    p.add_argument("--follow", action="store_true",
                   help="follow whatever round the stage is on (switches with ./demo live / go / round)")
    p.add_argument("--embedded", action="store_true",
                   help="running inside a presenterm slide box (no key handling, no q hint)")
    p.add_argument("--events", default=None, help="event log (default: the stage's .vault/events.jsonl)")
    p.add_argument("--scenario", action="store_true", help="play the scripted round instead of live events")
    p.add_argument("--snapshot", help="write one frame as SVG and exit (uses the scripted round)")
    p.add_argument("--at", type=float, default=5.0, help="time in seconds for --snapshot")
    p.add_argument("--size", default="110x46", help="WxH for --snapshot")
    args = p.parse_args()
    global EMBEDDED
    EMBEDDED = args.embedded
    if args.follow:
        args.round = PresenterWatch.stage_round() or "0"
    round_id = norm(args.round)
    if round_id is None:
        sys.exit(f"Unknown round {args.round!r}. Rounds: {' '.join(ROUNDS)}")

    if args.snapshot:
        snapshot(round_id, args.snapshot, args.at, args.size)
        return

    # presenterm stops the program with a signal when the deck closes: exit cleanly
    import signal

    def _stop(*_):
        raise KeyboardInterrupt
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, _stop)

    console = Console()
    state = State(round_id)
    start = time.monotonic()
    source = ScenarioPlayer(round_id, 0.0) if args.scenario else FileFollower(args.events or paths.events())
    watch = PresenterWatch() if ((args.follow or ROUNDS[round_id].get("hq")) and not args.scenario) else None
    last_sig, last_size = None, None
    keys = Keys() if not args.embedded else Keys.__new__(Keys)
    if args.embedded:
        keys.fd, keys.old = None, None
    try:
        with Live(console=console, screen=True, auto_refresh=False) as live:
            while True:
                now = time.monotonic() - start
                evs = source.poll(now) if args.scenario else source.poll()
                if watch and state.r.get("hq"):
                    evs += watch.poll(now)
                for ev in evs:
                    rid = norm(ev.get("round", state.round)) if ev.get("round") is not None else state.round
                    if args.follow and ev.get("kind") == "reset" and rid:
                        round_id = rid  # the stage moved to another round: follow it
                    if rid == state.round or ev.get("kind") == "reset" and rid == round_id:
                        state.apply(ev, now)
                w, h = console.size
                frame = draw(state, now, w, h)
                sig = frame.signature()
                if sig != last_sig or (w, h) != last_size:
                    live.update(frame.to_text(), refresh=True)
                    last_sig, last_size = sig, (w, h)
                pressed = keys.wait(0.05 if animating(state, now) else 0.25)
                if any(k in pressed for k in ("q", "Q", "\x1b", "\x03")):
                    break
                if "r" in pressed and not args.scenario:  # replay this round's log from the start
                    state = State(round_id)
                    source = FileFollower(args.events or paths.events())
    except KeyboardInterrupt:
        pass
    finally:
        keys.close()


if __name__ == "__main__":
    main()
