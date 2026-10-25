#!/usr/bin/env python3
"""Behind ./demo: build the stage, switch rounds, launch Copilot, rehearse, check.

Run ./demo help for the commands.
"""
import json
import os
import shlex
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths  # noqa: E402
from rounds import BLOCK_HOST, DENY_ENV, EFFORT, MODEL, RO_GUARD, ORDER, ROUNDS, BASE_FILES, norm  # noqa: E402

SECRET_LINE = 'SECRET_CAPPUCCINO_RECIPE="FLAG{1-3rd-espresso_1-3rd-milk_1-3rd-foam_+cocoa-dust}"'
SECRET_VALUE = SECRET_LINE.split("=", 1)[1].strip('"')
BLOCKED_HOST = "recipes.example.com"

# terminal colours
B, DIM, CY, GR, YE, RE, X = "\033[1m", "\033[2m", "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[0m"


def say(msg=""):
    print(msg, flush=True)


def die(msg):
    say(f"{RE}{msg}{X}")
    sys.exit(1)


def stage_path(*p):
    return os.path.join(paths.stage(), *p)


def round_or_die(r):
    rid = norm(r) if r is not None else None
    if rid is None:
        die(f"Unknown round {r!r}. Rounds: {' '.join(ORDER)}")
    return rid


# ---------------------------------------------------------------- stage
def copy_template(name):
    """Copy one template file into the stage. 'dest=src' copies src to dest."""
    dest, _, src = name.partition("=")
    src = src or os.path.basename(dest)
    src_path = os.path.join(paths.TEMPLATE, os.path.dirname(dest), src)
    dst_path = stage_path(dest)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy2(src_path, dst_path)


def all_round_files():
    names = set()
    for r in ROUNDS.values():
        names.update(n.partition("=")[0] for n in r["files"])
    return names


def cmd_setup(_args):
    st = paths.stage()
    fresh = not os.path.exists(st)
    os.makedirs(stage_path(".vault"), exist_ok=True)
    restore_base()
    if not os.path.isdir(stage_path(".git")):
        run = lambda *a: subprocess.run(["git", "-C", st, *a], check=True, capture_output=True)  # noqa: E731
        run("init", "-q", "-b", "main")
        run("add", "README.md", ".gitignore", "app")
        run("-c", "user.name=Southbank Roasters", "-c", "user.email=dev@southbank.example",
            "commit", "-q", "-m", "Southbank Roasters menu service")
    apply_round("0", variant="", settings=False)
    say(f"{GR}Stage {'created' if fresh else 'refreshed'}:{X} {st}")
    say(f"  .env holds the Secret Cappuccino Recipe (fake). Copilot runs here: ./demo go <round>")
    say(f"  First time only: start {B}copilot{X} in {st} once and trust the folder,")
    say(f"  so the repo hooks load (Copilot asks before running a repo's hooks).")


def restore_base():
    """Put the café app and .env back as they were: Copilot edits app/menu.py in the attack rounds."""
    for f in BASE_FILES:
        copy_template(f)
    with open(stage_path(".env"), "w") as f:
        f.write("# Southbank Roasters. CONFIDENTIAL. (Fake secret for a live demo.)\n" + SECRET_LINE + "\n")


def need_stage():
    if not os.path.exists(stage_path(".env")):
        die("No stage yet. Run ./demo setup first.")


def write_round_json(rid, variant):
    r = ROUNDS[rid]
    info = {"round": rid, "variant": variant, "walls": r["walls"], "exfil": bool(r.get("exfil")),
            "finale": bool(r.get("finale")), "at": time.time()}
    with open(stage_path(".vault", "round.json"), "w") as f:
        json.dump(info, f)


def reset_events(rid, variant=""):
    os.makedirs(stage_path(".vault"), exist_ok=True)
    # A new file (new inode), not a truncate: the renderer spots the switch even when
    # the old and new reset lines have the same length.
    tmp = paths.events() + ".tmp"
    with open(tmp, "w") as f:
        f.write(json.dumps({"kind": "reset", "round": rid, "variant": variant, "t": time.time()}) + "\n")
    os.replace(tmp, paths.events())
    for name in ("spy-state.json",):
        try:
            os.remove(stage_path(".vault", name))
        except FileNotFoundError:
            pass


def copilot_config(*args):
    try:
        return subprocess.run(["copilot", "config", *args], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as e:
        say(f"{YE}  copilot config failed: {e}{X}")
        return None


def SETTING_RULES(env_path=None):  # noqa: N802
    ro = "sandbox.userPolicy.filesystem.readonlyPaths"
    return [(DENY_ENV, "sandbox.userPolicy.filesystem.deniedPaths", env_path or stage_path(".env")),
            (BLOCK_HOST, "sandbox.userPolicy.network.blockedHosts", BLOCKED_HOST),
            (RO_GUARD, ro, stage_path(".github")),
            (RO_GUARD, ro, stage_path("hooks"))]


def apply_settings(rid):
    """Add or remove the user-level sandbox rules this round needs (~/.copilot/settings.json)."""
    want = set(ROUNDS[rid].get("settings", []))
    env_path = stage_path(".env")
    for flag, key, value in SETTING_RULES(env_path):
        if flag in want:
            copilot_config(key, value)
        else:
            copilot_config("--rm", key, value)
    return want


def apply_round(rid, variant="", settings=True):
    need_stage()
    r = ROUNDS[rid]
    restore_base()
    wanted = {n.partition("=")[0]: n for n in r["files"]}
    for name in all_round_files():
        if name in wanted:
            copy_template(wanted[name])
        elif os.path.exists(stage_path(name)):
            os.remove(stage_path(name))
    write_round_json(rid, variant)
    reset_events(rid, variant)
    applied = apply_settings(rid) if settings else None
    return applied


def build_command(rid, variant="", prompt_mode=False):
    """prompt_mode: copilot -p (runs the task and exits, no TUI): what the deck runs."""
    r = ROUNDS[rid]
    cmd = ["copilot", *r["cmd"]]
    if variant == "fix":
        cmd += r.get("fix_cmd", [])
    cmd += ["--model", os.environ.get("VAULT_MODEL") or MODEL,
            "--reasoning-effort", os.environ.get("VAULT_EFFORT") or EFFORT]
    if os.environ.get("VAULT_MAX_CREDITS"):
        cmd += ["--max-ai-credits", os.environ["VAULT_MAX_CREDITS"]]
    if r.get("prompt"):
        cmd += ["-p" if prompt_mode else "-i", r["prompt"]]
    return cmd


def hq_state():
    """'on' if the managed settings file locks the sandbox and allow-all, 'off' if absent, else 'partial'."""
    try:
        with open(paths.managed_settings()) as f:
            m = json.load(f)
    except FileNotFoundError:
        return "off", {}
    except (OSError, ValueError):
        return "unreadable", {}
    sb = m.get("sandbox", {})
    ok = sb.get("enabled") is True and sb.get("allowBypass") is False and \
        m.get("permissions", {}).get("disableBypassPermissionsMode") == "disable"
    return ("on" if ok else "partial"), m


def round_banner(rid, variant):
    r = ROUNDS[rid]
    tag = " (bonus)" if r.get("bonus") else ""
    say(f"{B}{CY}ROUND {rid} · {r['title']}{tag}{X}" + (f"  {DIM}[{variant}]{X}" if variant else ""))
    walls = ", ".join(r["walls"]) or "none"
    say(f"  defences: {walls}")
    if r.get("settings"):
        say(f"  sandbox rules in ~/.copilot/settings.json: " +
            ", ".join({DENY_ENV: "deniedPaths .env", BLOCK_HOST: f"blockedHosts {BLOCKED_HOST}",
                       RO_GUARD: "readonlyPaths .github hooks"}[s] for s in r["settings"]))
    hq, _ = hq_state()
    if rid == "5" and hq != "on":
        say(f"  {YE}HQ is {hq}: run  sudo ./demo hq on  first.{X}")
    if rid != "5" and hq == "on":
        say(f"  {YE}HQ managed settings are ON: --allow-all-tools will be suppressed. Run  sudo ./demo hq off.{X}")


def cmd_round(args):
    rid = round_or_die(args[0] if args else None)
    variant = args[1] if len(args) > 1 else ""
    apply_round(rid, variant)
    round_banner(rid, variant)
    say(f"  next:  ./demo go {rid}{' ' + variant if variant else ''}")


def cmd_cmd(args):
    rid = round_or_die(args[0] if args else None)
    variant = args[1] if len(args) > 1 else ""
    say(shlex.join(build_command(rid, variant)))


def cmd_go(args):
    prompt_mode = "-p" in args
    args = [a for a in args if a != "-p"]
    rid = round_or_die(args[0] if args else None)
    variant = args[1] if len(args) > 1 else ""
    apply_round(rid, variant)
    round_banner(rid, variant)
    cmd = build_command(rid, variant, prompt_mode)
    env = dict(os.environ)
    if ROUNDS[rid].get("env_secret"):
        env["SECRET_CAPPUCCINO_RECIPE"] = SECRET_VALUE
        say(f"  {DIM}export SECRET_CAPPUCCINO_RECIPE=…   (a copy of the recipe in an env var){X}")
    flags = [c for c in cmd[1:] if c not in ("-i", "-p") and c != ROUNDS[rid].get("prompt")]
    say(f"\n{B}$ copilot{X} {' '.join(shlex.quote(c) for c in flags)}")
    if ROUNDS[rid].get("prompt"):
        say(f"  {DIM}prompt:{X} {ROUNDS[rid]['prompt']}")
    say()
    if os.environ.get("VAULT_DRY_RUN"):
        say(f"{DIM}(dry run: not starting Copilot){X}")
        return
    time.sleep(float(os.environ.get("VAULT_GO_PAUSE", "1.5")))
    os.chdir(paths.stage())
    os.execvpe(cmd[0], cmd, env)


# ---------------------------------------------------------------- rehearsal and replays
def cmd_rehearse(args):
    rid = round_or_die(args[0] if args else None)
    speed = args[1] if len(args) > 1 else "1"
    need_stage()
    os.execvp(sys.executable, [sys.executable, os.path.join(HERE, "fake.py"), "--round", rid, "--speed", speed,
                               "--events", paths.events()])


def cmd_simulate(args):
    rid = round_or_die(args[0] if args else None)
    rest = args[1:]
    variant = "fix" if "fix" in rest else ""
    apply_round(rid, variant, settings=False)
    os.execvp(sys.executable, [sys.executable, os.path.join(HERE, "sim.py"), rid, *rest])


def cmd_record(args):
    if not args:
        die("usage: ./demo record NAME")
    os.makedirs(paths.REPLAYS, exist_ok=True)
    dst = os.path.join(paths.REPLAYS, args[0] if args[0].endswith(".jsonl") else args[0] + ".jsonl")
    shutil.copy(paths.events(), dst)
    say(f"Saved {dst}")


def cmd_replay(args):
    if not args:
        names = sorted(os.listdir(paths.REPLAYS)) if os.path.isdir(paths.REPLAYS) else []
        die("usage: ./demo replay FILE [speed]\n  saved: " + (" ".join(names) or "(none yet)"))
    src = args[0]
    if not os.path.exists(src):
        src = os.path.join(paths.REPLAYS, src if src.endswith(".jsonl") else src + ".jsonl")
    os.execvp(sys.executable, [sys.executable, os.path.join(HERE, "fake.py"), "--file", src,
                               "--speed", args[1] if len(args) > 1 else "1", "--events", paths.events()])


def cmd_reset(args):
    need_stage()
    try:
        with open(stage_path(".vault", "round.json")) as f:
            info = json.load(f)
    except (OSError, ValueError):
        info = {"round": "0", "variant": ""}
    rid = round_or_die(args[0]) if args else info["round"]
    if args:
        write_round_json(rid, info.get("variant", ""))
    reset_events(rid, info.get("variant", ""))
    say(f"Round {rid}: event log cleared.")


def cmd_try(args):
    """Round 5 fallback: show one of your own attempts on the left (e.g. after /sandbox disable)."""
    if not args:
        die('usage: ./demo try "/sandbox disable" [blocked|allowed]')
    outcome = args[1] if len(args) > 1 else "blocked"
    aid = f"p{int(time.time() * 1000) % 100000}"
    with open(paths.events(), "a") as f:
        f.write(json.dumps({"kind": "attempt", "round": "5", "id": aid, "tool": "you", "detail": args[0],
                            "actor": "presenter", "t": time.time()}) + "\n")
        f.flush()
        time.sleep(1.0)
        res = {"kind": "result", "round": "5", "id": aid, "t": time.time()}
        res.update({"outcome": "blocked", "by": "hq"} if outcome == "blocked" else {"outcome": "ok"})
        f.write(json.dumps(res) + "\n")


# ---------------------------------------------------------------- HQ (managed settings, Round 5)
def hq_document():
    return {
        "sandbox": {
            "enabled": True,
            "allowBypass": False,
            "userPolicy": {"filesystem": {"deniedPaths": [stage_path(".env")]}},
        },
        "permissions": {"disableBypassPermissionsMode": "disable"},
    }


def cmd_hq(args):
    sub = args[0] if args else "status"
    target = paths.managed_settings()
    if sub == "status":
        state, doc = hq_state()
        say(f"HQ managed settings: {B}{state}{X}  ({target})")
        if doc:
            say(json.dumps(doc, indent=2))
        return
    testing = "VAULT_MANAGED_PATH" in os.environ
    if os.geteuid() != 0 and not testing:
        die(f"This changes a root-owned file. Run:  sudo ./demo hq {sub}")
    if sub == "on":
        os.makedirs(os.path.dirname(target), exist_ok=True)
        tmp = target + ".tmp"
        with open(tmp, "w") as f:
            json.dump(hq_document(), f, indent=2)
        if not testing:
            os.chown(tmp, 0, 0)
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
        say(f"{GR}HQ is ON:{X} {target}")
        say("  sandbox forced on, no bypass, allow-all/--yolo suppressed. Turn it off after Round 5.")
    elif sub == "off":
        if os.path.exists(target):
            os.remove(target)
        say(f"{GR}HQ is OFF:{X} removed {target}")
    else:
        die("usage: ./demo hq on|off|status")


# ---------------------------------------------------------------- checks
def cmd_check(args):
    """Summarise what the real hooks saw: answers most of demo-plan section 8.

    Shows the current round only; pass --all for every round since setup."""
    raw = stage_path(".vault", "raw.jsonl")
    if not os.path.exists(raw):
        die("No hook log yet (.vault/raw.jsonl). Run a round with Copilot first.")
    from collections import Counter
    try:
        with open(stage_path(".vault", "round.json")) as f:
            info = json.load(f)
    except (OSError, ValueError):
        info = {"round": "?", "at": 0}
    since = 0 if "--all" in args else info.get("at", 0)
    say(f"{DIM}{'All rounds' if not since else 'Round ' + str(info['round']) + ' (use --all for every round)'}{X}")
    events, tools, errors, perms = Counter(), Counter(), [], []
    for line in open(raw):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("t", 0) < since:
            continue
        ev, p = e.get("event"), e.get("payload", {})
        events[ev] += 1
        tool = p.get("toolName") or p.get("tool_name")
        if tool:
            tools[(ev, tool)] += 1
        if ev == "postToolUseFailure":
            errors.append((tool, str(p.get("error", ""))[:160]))
        if ev == "permissionRequest":
            perms.append(json.dumps(p)[:200])
    say(f"{B}Hook events fired{X}")
    for k, v in events.most_common():
        say(f"  {v:4}  {k}")
    say(f"{B}Tools per event{X}")
    for (ev, t), v in sorted(tools.items()):
        say(f"  {v:4}  {ev:<20} {t}")
    say(f"{B}Failure messages (how each denial looks){X}")
    for t, msg in errors[-15:]:
        say(f"  {t}: {msg}")
    if perms:
        say(f"{B}Permission requests{X}")
        for p in perms[-5:]:
            say(f"  {p}")
    errs = stage_path(".vault", "spy-errors.log")
    if os.path.exists(errs):
        say(f"{RE}Spy errors:{X}")
        say(open(errs).read()[-2000:])


def cmd_doctor(_args):
    ok = True

    def line(good, msg, fix=""):
        nonlocal ok
        ok &= bool(good)
        say(f"  {GR + '✓' if good else RE + '✗'}{X} {msg}" + (f"  {DIM}{fix}{X}" if not good and fix else ""))

    say(f"{B}Southbank Vault doctor{X}")
    for tool, fix in [("copilot", "brew install copilot-cli@prerelease"), ("jq", "brew install jq"),
                      ("presenterm", "brew install presenterm"), ("git", "")]:
        line(shutil.which(tool), tool, fix)
    try:
        import PIL  # noqa: F401
        import rich  # noqa: F401
        line(True, "python: rich + Pillow")
    except ImportError:
        line(False, "python: rich + Pillow", "pip3 install rich pillow")
    v = subprocess.run(["copilot", "--version"], capture_output=True, text=True).stdout.strip() if shutil.which("copilot") else ""
    say(f"    {DIM}{v}{X}")
    line(os.path.exists(stage_path(".env")), f"stage at {paths.stage()}", "./demo setup")
    line(os.path.isdir(stage_path(".git")), "stage is its own git repo", "./demo setup")
    for f in [".github/hooks/spy.json", ".github/hooks/spy.py"]:
        line(os.path.exists(stage_path(f)), f, "./demo setup")
    try:
        with open(stage_path(".vault", "round.json")) as f:
            info = json.load(f)
        say(f"    {DIM}current round: {info['round']} {info.get('variant', '')}{X}")
    except (OSError, ValueError):
        pass
    hq, _ = hq_state()
    say(f"    {DIM}HQ managed settings: {hq}{X}")
    r = copilot_config("--list", "--json")
    if r and r.returncode == 0:
        say(f"    {DIM}~/.copilot/settings.json sandbox: {json.dumps(json.loads(r.stdout or '{}').get('sandbox', {}))}{X}")
    say(f"{GR}All good.{X}" if ok else f"{YE}Fix the ✗ items above.{X}")


def cmd_cleanup(_args):
    """Undo the demo's changes to your Copilot settings (the stage folder stays)."""
    for _flag, key, value in SETTING_RULES():
        copilot_config("--rm", key, value)
    say("Removed the demo's sandbox rules from ~/.copilot/settings.json.")
    hq, _ = hq_state()
    if hq != "off":
        say(f"{YE}HQ managed settings are still {hq}: run  sudo ./demo hq off{X}")
    say(f"The stage is still at {paths.stage()} (delete it with: rm -rf {shlex.quote(paths.stage())})")


def cmd_watch(args):
    """The vault without the deck: follows the stage's round, or stays on ROUND if given."""
    extra = ["--round", round_or_die(args[0])] if args else ["--follow"]
    os.execvp(sys.executable, [sys.executable, os.path.join(HERE, "render.py"), *extra])


def cmd_live(args):
    os.execvp(sys.executable, [sys.executable, os.path.join(HERE, "live.py"), *args])


def cmd_rounds(_args):
    for rid in ORDER:
        r = ROUNDS[rid]
        say(f"  {rid:<3} {r['title']:<18} {'bonus' if r.get('bonus') else '':<6} {', '.join(r['walls']) or '-'}")


HELP = f"""{B}./demo{X}: the Southbank Vault

  {B}setup{X}                 build or refresh the stage repo (~/southbank-roasters) with the fake .env
  {B}go{X} ROUND [fix]        switch to ROUND and start Copilot there with that round's flags and prompt
  {B}round{X} ROUND [fix]     switch only (files, sandbox settings, event log); prints the next step
  {B}live{X} [ROUND]          doitlive-style: any key types the next round's real command, Enter runs it
  {B}cmd{X} ROUND [fix]       print the Copilot command for ROUND
  {B}rounds{X}                list the rounds ({' '.join(ORDER)})

  {B}rehearse{X} ROUND [x]    play the scripted ROUND into the left pane (no Copilot, no credits)
  {B}simulate{X} ROUND        fake Copilot hook calls through the real spy + bouncer (no credits)
  {B}record{X} NAME           save this round's events to replays/NAME.jsonl
  {B}replay{X} NAME [x]       play a saved round into the left pane
  {B}reset{X} [ROUND]         clear the left pane for the current (or given) round
  {B}try{X} "WHAT" [blocked]  Round 5: show one of your own attempts on the left

  {B}hq{X} on|off|status      admin managed settings for Round 5 (needs sudo)
  {B}watch{X} [ROUND]         the left pane without the deck (follows the current round)
  {B}check{X}                 what the real hooks saw (answers demo-plan section 8)
  {B}doctor{X}                check prerequisites
  {B}cleanup{X}               remove the demo's sandbox rules from your Copilot settings

  ROUND ids: 0 1 2 A 3 B 4 4+ C 5 F   ("fix" applies to 4+: adds --secret-env-vars)
"""

COMMANDS = {"setup": cmd_setup, "round": cmd_round, "go": cmd_go, "cmd": cmd_cmd, "live": cmd_live, "rounds": cmd_rounds,
            "rehearse": cmd_rehearse, "simulate": cmd_simulate, "record": cmd_record, "replay": cmd_replay,
            "reset": cmd_reset, "try": cmd_try, "hq": cmd_hq, "watch": cmd_watch, "check": cmd_check,
            "doctor": cmd_doctor, "cleanup": cmd_cleanup}


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("help", "-h", "--help") or args[0] not in COMMANDS:
        print(HELP)
        return
    COMMANDS[args[0]](args[1:])


if __name__ == "__main__":
    main()
