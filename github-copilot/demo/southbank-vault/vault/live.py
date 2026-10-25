#!/usr/bin/env python3
"""doitlive-style right pane: mash any keys and the next real command types itself out.

  ./demo live [ROUND]

Keys at the prompt:
  any key   type the next few characters
  Enter     finish typing and run it (the round is switched just before its first command)
  ctrl+n    skip this command          ctrl+b  back one command
  ctrl+d    quit
"""
import os
import shlex
import subprocess
import sys
import termios
import tty

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ctl  # noqa: E402
import paths  # noqa: E402
from rounds import ORDER, ROUNDS, norm  # noqa: E402

CHARS_PER_KEY = 3
B, DIM, CY, GR, YE, X = "\033[1m", "\033[2m", "\033[36m", "\033[32m", "\033[33m", "\033[0m"
DEMO = os.path.join(paths.DEMO, "demo")


def display(cmd):
    """How the command looks on screen: flags quoted for the shell, the prompt in plain double quotes."""
    out = []
    i = 0
    while i < len(cmd):
        if cmd[i] == "-i" and i + 1 < len(cmd):
            out.append(f'-i "{cmd[i + 1]}"')
            i += 2
        else:
            out.append(shlex.quote(cmd[i]))
            i += 1
    return " ".join(out)


def steps(start):
    """[(round, variant, shown_text, argv, env_secret)] from START to the end of the demo."""
    out = []
    for rid in ORDER[ORDER.index(start):]:
        r = ROUNDS[rid]
        if rid == "5":
            out += [(rid, "", "sudo ./demo hq on", ["sudo", DEMO, "hq", "on"], False),
                    (rid, "", "copilot", ["copilot"], False),
                    (rid, "", "copilot --yolo", ["copilot", "--yolo"], False),
                    (rid, "", "sudo ./demo hq off", ["sudo", DEMO, "hq", "off"], False)]
            continue
        variants = ["", "fix"] if r.get("fix_cmd") else [""]
        for v in variants:
            cmd = ctl.build_command(rid, v)
            out.append((rid, v, display(cmd), cmd, bool(r.get("env_secret"))))
    return out


def read_key(fd):
    return os.read(fd, 8).decode(errors="ignore")


def main():
    start = norm(sys.argv[1]) if len(sys.argv) > 1 else "0"
    if start is None:
        sys.exit(f"Unknown round. Rounds: {' '.join(ORDER)}")
    ctl.need_stage()
    plan = steps(start)
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    prompt = f"{GR}southbank-roasters{X} {B}${X} "
    i, switched = 0, None
    try:
        while i < len(plan):
            rid, variant, shown, argv, secret = plan[i]
            needs_switch = switched != (rid, variant)
            if needs_switch and (switched is None or switched[0] != rid):
                title = ROUNDS[rid]["title"].title().replace("Ai ", "AI ").replace("Hq ", "HQ ")
                sys.stdout.write(f"\n{DIM}# Round {rid} · {title}{X}\n")
            sys.stdout.write(prompt)
            sys.stdout.flush()
            typed = 0
            tty.setcbreak(fd)
            action = None
            while action is None:
                k = read_key(fd)
                if "\x04" in k:
                    action = "quit"
                elif "\x0e" in k:
                    action = "skip"
                elif "\x02" in k:
                    action = "back"
                elif "\r" in k or "\n" in k:
                    if needs_switch:
                        ctl.apply_round(rid, variant)
                        switched, needs_switch = (rid, variant), False
                    sys.stdout.write(shown[typed:])
                    typed = len(shown)
                    action = "run"
                elif needs_switch:
                    # First key of a new round: switch now, not when the last round ended,
                    # so the left pane keeps showing the result until you move on.
                    ctl.apply_round(rid, variant)  # files, sandbox rules, fresh left pane
                    switched, needs_switch = (rid, variant), False
                    chunk = shown[:CHARS_PER_KEY]
                    sys.stdout.write(chunk)
                    typed = len(chunk)
                elif typed < len(shown):
                    chunk = shown[typed:typed + CHARS_PER_KEY]
                    sys.stdout.write(chunk)
                    typed += len(chunk)
                sys.stdout.flush()
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            sys.stdout.write("\n")
            if action == "quit":
                break
            if action == "skip":
                i += 1
                continue
            if action == "back":
                i = max(0, i - 1)
                switched = None
                continue
            env = dict(os.environ)
            if secret:
                env["SECRET_CAPPUCCINO_RECIPE"] = ctl.SECRET_VALUE
            try:
                subprocess.run(argv, cwd=paths.stage(), env=env)
            except FileNotFoundError as e:
                sys.stdout.write(f"{YE}{e}{X}\n")
            except KeyboardInterrupt:
                pass
            i += 1
        sys.stdout.write(f"\n{DIM}# end of the demo{X}\n")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == "__main__":
    main()
