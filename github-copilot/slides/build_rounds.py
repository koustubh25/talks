#!/usr/bin/env python3
"""Generate rounds.gen.md: one slide per round, sized for the terminal the deck runs in.

  build_rounds.py COLS ROWS      (present.sh runs it with `tput cols` / `tput lines`)

Each round slide (windows at least 150 columns wide; narrower ones stack top/bottom):
  left    the vault for that round
  right   a shell prompt. Press → and the round's command types itself out and runs
          (copilot -p). → again goes to the next round.

How → drives it:
  - presenterm starts every +exec_replace box when the deck opens, so each slide's box is
    already running deckrun.py --cue N, waiting at an empty prompt.
  - The slide ends with a <!-- pause -->, so the first → stays on the slide (step 2).
  - presenterm -P reports every move over UDP; vault/cue.py writes it to the stage, and the
    box for slide N starts when it sees "slide N, step 2".
Round 5 is the exception: sudo needs a password, which a box can't take, so its ctrl+e
opens Copilot full screen.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.join("..", "demo", "southbank-vault", "vault")  # relative to slides/
sys.path.insert(0, os.path.join(HERE, VAULT))
from rounds import ORDER, ROUNDS  # noqa: E402

# Measured on presenterm 0.16.1, dark theme, margin percent 2 (deck.md front matter).
SIDE_BY_SIDE_MIN_COLS = 150
VAULT_MIN_W, VAULT_MIN_H = 80, 27   # render.py's MIN_W, MIN_H
FULL_SCREEN = {"5"}                 # needs typing (sudo password, /sandbox disable)

NOTES = {
    "0": "→ types a quick tour of the stage: the files, the spy hook, the café app. No Copilot, no credits.",
    "1": "\"Instructions guide the model, but do not guarantee that it will follow every rule.\"",
    "2": "\"The rule covered a tool, not the intent.\" (Antigravity did exactly this.)",
    "A": "(bonus) available-tools decides what it can SEE; allow/deny decides what it may USE.",
    "3": "\"Real code, but it only catches what you thought of. And it fails open on timeout.\"",
    "B": "(bonus) \"The judge is probabilistic and not a security boundary.\" (copilot --help)",
    "4": "\"That's macOS saying no.\" Sandbox rules live in user/managed settings, not the repo.",
    "4+": "(bonus) the recipe is also in an env var: it leaks. Next slide adds --secret-env-vars.",
    "C": "(bonus) Reading is fine, leaving isn't. The lethal trifecta needs a way out.",
    "5": "ctrl+e (the one exception): sudo password (HQ on), then Copilot --yolo full screen. "
         "Try /sandbox disable, then a prompt, then /exit. HQ switches off by itself.\n"
         "\"Does it stop me, on a bad day, at 6 pm, wanting to ship?\"",
    "F": "\"The guardrails need guardrails.\" CODEOWNERS + ruleset on github.com.",
}


def usable(cols):
    return cols - 2 * max(1, round(cols * 0.02))


def columns(cols):
    """(left share, right share, vault box width, runner box width).

    presenterm's columns come out narrower than their share; a box wider than its column
    wraps every line. The 0.92/-4 factors were measured at 150, 164, 191 and 220 columns."""
    u = usable(cols)
    left = max(92, round(u * 0.55))
    right = u - left
    return left, right, int(left * 0.92) - 4, int(right * 0.92) - 4


def first_round_slide():
    """Slide number (1-based, as presenterm -P reports it) of the first round slide."""
    with open(os.path.join(HERE, "deck.md")) as f:
        text = f.read()
    front = re.match(r"---\n(.*?)\n---\n", text, re.S)
    intro = 1 if front and re.search(r"^title:", front.group(1), re.M) else 0
    before = text[:text.index("<!-- include: rounds.gen.md -->")]
    return intro + before.count("<!-- end_slide -->") + 1


def runner(rid, variant, slide, w, h):
    if rid in FULL_SCREEN:
        return ["```bash +exec +acquire_terminal",
                f"/// copilot() {{ {VAULT}/deckrun.py {rid} --interactive; }}",
                "copilot --yolo", "```", "",
                "**ctrl+e**: HQ on (sudo), then Copilot full screen.",
                "Try **/sandbox disable**, then **/exit**.", ""]
    args = f"{rid} {variant}".strip()
    return ["```bash +exec_replace +pty:%d:%d" % (w, h),
            f"{VAULT}/deckrun.py {args} --cue {slide}", "```", ""]


def side_by_side(rid, variant, slide, cols, rows):
    left, right, vault_w, run_w = columns(cols)
    out = ["<!-- no_footer -->", f"<!-- column_layout: [{left}, {right}] -->", "<!-- column: 0 -->", "",
           "```bash +exec_replace +pty:%d:%d" % (vault_w, rows - 3),
           f"{VAULT}/render.py --embedded --round {rid}", "```", "",
           "<!-- column: 1 -->", ""]
    out += runner(rid, variant, slide, run_w, rows - 4)
    out += ["<!-- reset_layout -->"]
    return out


def stacked(rid, variant, slide, cols, rows):
    w = usable(cols) - 6
    bottom = 6 if rid in FULL_SCREEN else max(6, round((rows - 3) * 0.25))
    vault = max(VAULT_MIN_H, rows - 4 - bottom)
    bottom = rows - 4 - vault
    out = ["<!-- no_footer -->", "", "```bash +exec_replace +pty:%d:%d" % (w, vault),
           f"{VAULT}/render.py --embedded --round {rid}", "```", ""]
    return out + runner(rid, variant, slide, w, max(4, bottom))


def slide_md(rid, variant, slide, cols, rows):
    r = ROUNDS[rid]
    label = f"{rid} fix" if variant else rid
    wide = cols >= SIDE_BY_SIDE_MIN_COLS and columns(cols)[3] >= 40
    out = (side_by_side if wide else stacked)(rid, variant, slide, cols, rows)
    if rid not in FULL_SCREEN:
        # The first → stays here (step 2) and starts the run. A pause needs something after
        # it to count as a step: a dim marker in the bottom-right corner.
        out += ["", "<!-- pause -->", "", "<!-- alignment: right -->",
                '<span style="color: #4A4250">▶</span>']
    note = f"Round {label} · {r['title'].title()}\n" + NOTES.get(rid, "")
    if variant:
        note = f"Round {label}\nSame round with --secret-env-vars: the env var is scrubbed from Copilot's tools."
    if rid not in FULL_SCREEN:
        note += "\n→ runs this round (the command types itself). → again: next round. n skips the round."
    out += ["", "<!--", "speaker_note: |"] + ["  " + line for line in note.splitlines()] + ["-->", ""]
    return "\n".join(out)


def main():
    cols, rows = (int(a) for a in sys.argv[1:3]) if len(sys.argv) > 2 else (164, 40)
    slide = first_round_slide()
    parts = []
    for rid in ORDER:
        for variant in ([""] + (["fix"] if ROUNDS[rid].get("fix_cmd") else [])):
            parts.append(slide_md(rid, variant, slide, cols, rows))
            slide += 1
    # presenterm reads every HTML comment in an included file as a command: no plain comments here.
    with open(os.path.join(HERE, "rounds.gen.md"), "w") as f:
        f.write("\n<!-- end_slide -->\n\n".join(parts))
    print(f"rounds.gen.md: {len(parts)} round slides for {cols}x{rows}")


if __name__ == "__main__":
    main()
