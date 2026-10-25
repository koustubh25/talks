#!/usr/bin/env python3
"""Run one round from a slide (what the deck's ctrl+e starts).

  deckrun.py ROUND [fix] [--quiet]  switch the stage to ROUND, show the command (unless --quiet), run copilot -p
  deckrun.py ROUND --interactive    full-terminal copilot (Round 0: /env; Round 5: HQ on, copilot --yolo, HQ off)
  deckrun.py ROUND [fix] --cue N    wait at an empty prompt until the deck reaches slide N, step 2
                                    (→ on the slide), then type the command out and run it

--cue is what the deck uses: presenterm starts every box when the deck opens, so each
round's box sits at its prompt until cue.py reports the presenter pressed → on its slide.

The -p form needs no typing, so it can run inside a presenterm box next to the vault.
"""
import os
import shlex
import shutil
import subprocess
import sys
import textwrap
import time
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ctl  # noqa: E402
import paths  # noqa: E402
from rounds import EFFORT, MODEL, ROUNDS, norm  # noqa: E402

B, DIM, GR, CY, YE, X = "\033[1m", "\033[2m", "\033[32m", "\033[36m", "\033[33m", "\033[0m"
PROMPT = f"{GR}southbank-roasters{X} {B}${X} "
DEMO = os.path.join(paths.DEMO, "demo")


def show(cmd, prompt_text=None):
    """Print the command like a shell would show it, wrapped to the box."""
    width = max(40, shutil.get_terminal_size((100, 10)).columns - 2)
    words = [shlex.quote(c) for c in cmd]
    if prompt_text:
        words += ["-p", f'"{prompt_text}"']
    lines = textwrap.wrap(" ".join(words), width - 20, break_on_hyphens=False, break_long_words=False)
    sys.stdout.write(PROMPT + f"{B}{lines[0]}{X}\n")
    for line in lines[1:]:
        sys.stdout.write(f"    {B}{line}{X}\n")
    sys.stdout.write("\n")
    sys.stdout.flush()


TOUR = ["ls -A", "ls .github/hooks", "python3 app/menu.py"]  # Round 0: meet the stage (no AGENTS.md yet)


def command_lines(rid, variant, width):
    """The command as you'd type it, wrapped with \\ (model flags hidden: they're pinned)."""
    r = ROUNDS[rid]
    cmd = ctl.build_command(rid, variant, prompt_mode=True)
    prompt = r.get("prompt")
    words, skip = [], 0
    for c in cmd[1:]:
        if skip:
            skip -= 1
        elif c in ("--model", "--reasoning-effort"):
            skip = 1
        elif c not in ("-p", prompt):
            name, eq, value = c.partition("=")
            words.append(name + eq + shlex.quote(value) if eq else shlex.quote(c))
    lines, cur = [], "copilot"
    first = width - len("southbank-roasters $ ")  # the first line shares the prompt's row
    for w in words:
        if len(cur) + 1 + len(w) + 2 > (first if not lines else width):
            lines.append(cur + " \\")
            cur = "  " + w
        else:
            cur += " " + w
    lines.append(cur + " \\")
    body = textwrap.wrap(prompt, width - 8)
    lines.append('  -p "' + body[0])
    lines += ["      " + t for t in body[1:]]
    lines[-1] += '"'
    return lines


def type_out(lines, cps=90):
    """Type like a person (fast), the way doitlive does."""
    import random
    for i, line in enumerate(lines):
        if i:
            sys.stdout.write("\n" + ("" if line.startswith(" ") else "  "))
        for ch in line:
            sys.stdout.write(f"{B}{ch}{X}")
            sys.stdout.flush()
            time.sleep(random.uniform(0.4, 1.6) / cps)
    time.sleep(0.3)
    sys.stdout.write("\n")
    sys.stdout.flush()


def wait_for_cue(slide):
    """Block until the deck is on SLIDE, step 2 or later (seen after this box started)."""
    path = os.path.join(paths.stage(), ".vault", "cue.json")
    start = time.time()
    while True:
        try:
            with open(path) as f:
                c = json.load(f)
            if c.get("slide") == slide and c.get("chunk", 0) >= 1 and c.get("t", 0) > start:
                return
        except (OSError, ValueError):
            pass
        time.sleep(0.1)


def run_cued(rid, variant, slide):
    width = max(40, shutil.get_terminal_size((80, 20)).columns - 4)
    sys.stdout.write("\033[?25l")  # no cursor while waiting; the prompt is enough
    sys.stdout.write(PROMPT + f"{DIM}  → run this round    n skip it{X}")
    sys.stdout.flush()
    try:
        wait_for_cue(slide)
    except KeyboardInterrupt:
        return
    sys.stdout.write("\r\033[K" + PROMPT)  # clear the hint, then type
    sys.stdout.flush()
    if rid == "0":
        ctl.apply_round(rid)
        for i, c in enumerate(TOUR):
            if i:
                sys.stdout.write(PROMPT)
            type_out([c])
            subprocess.run(["bash", "-c", c], cwd=paths.stage())
        sys.stdout.write(f"\n{DIM}# → next round{X}\n")
        return
    ctl.apply_round(rid, variant)
    r = ROUNDS[rid]
    env = dict(os.environ)
    if r.get("env_secret"):
        env["SECRET_CAPPUCCINO_RECIPE"] = ctl.SECRET_VALUE
        type_out(["export SECRET_CAPPUCCINO_RECIPE=…"])
        sys.stdout.write(PROMPT)
    type_out(command_lines(rid, variant, width))
    try:
        rc = subprocess.run(ctl.build_command(rid, variant, prompt_mode=True), cwd=paths.stage(), env=env).returncode
    except FileNotFoundError as e:
        sys.stdout.write(f"{YE}{e}{X}\n")
        return
    except KeyboardInterrupt:
        rc = 130
    sys.stdout.write(f"\n{DIM}# copilot exited ({rc}) · → next round{X}\n")


def run_prompt_mode(rid, variant, quiet=False):
    ctl.apply_round(rid, variant)
    r = ROUNDS[rid]
    cmd = ctl.build_command(rid, variant, prompt_mode=True)
    env = dict(os.environ)
    if r.get("env_secret"):
        env["SECRET_CAPPUCCINO_RECIPE"] = ctl.SECRET_VALUE
        sys.stdout.write(PROMPT + f"{DIM}export SECRET_CAPPUCCINO_RECIPE=…{X}\n")
    if not quiet:  # the slide already shows the command as code
        show([c for c in cmd if c not in ("-p", r.get("prompt"))], r.get("prompt"))
    try:
        rc = subprocess.run(cmd, cwd=paths.stage(), env=env).returncode
    except FileNotFoundError as e:
        sys.exit(f"{YE}{e}{X}")
    except KeyboardInterrupt:
        rc = 130
    sys.stdout.write(f"\n{DIM}# copilot exited ({rc}){X}\n")


def run_interactive(rid):
    ctl.apply_round(rid)
    os.chdir(paths.stage())
    model = ["--model", os.environ.get("VAULT_MODEL") or MODEL,
             "--reasoning-effort", os.environ.get("VAULT_EFFORT") or EFFORT]
    if rid != "5":
        print(f"{DIM}# type /env to see the hooks, then /exit{X}")
        subprocess.run(["copilot", *model])
        return
    print(f"{CY}{B}HQ Override{X}: switching on managed settings (sudo)")
    if subprocess.run(["sudo", DEMO, "hq", "on"]).returncode != 0:
        print(f"{YE}HQ is not on: skipping.{X}")
        return
    try:
        print(f"\n{DIM}# in Copilot: try /sandbox disable, then /exit{X}")
        print(PROMPT + f"{B}copilot --yolo{X}")
        subprocess.run(["copilot", "--yolo", *model])
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\n{DIM}# switching HQ off again{X}")
        subprocess.run(["sudo", DEMO, "hq", "off"])


def main():
    args = sys.argv[1:]
    interactive = "--interactive" in args
    quiet = "--quiet" in args
    cue = None
    if "--cue" in args:
        i = args.index("--cue")
        cue = int(args[i + 1])
        del args[i:i + 2]
    args = [a for a in args if a not in ("--interactive", "--quiet")]
    rid = norm(args[0]) if args else None
    if rid is None:
        sys.exit("usage: deckrun.py ROUND [fix] [--interactive]")
    ctl.need_stage()
    if cue is not None:
        run_cued(rid, args[1] if len(args) > 1 else "", cue)
    elif interactive:
        run_interactive(rid)
    else:
        run_prompt_mode(rid, args[1] if len(args) > 1 else "", quiet)


if __name__ == "__main__":
    main()
