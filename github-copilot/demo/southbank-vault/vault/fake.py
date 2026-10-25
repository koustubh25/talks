#!/usr/bin/env python3
"""Pretend to be Copilot: write a scripted round (or a recorded one) into the event log in real time.

Rehearse the left pane without spending AI credits:
  ./demo rehearse 3            scripted Round 3 (vault/scenarios.py)
  ./demo replay round3-good    a round recorded with ./demo record
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths  # noqa: E402
from rounds import norm  # noqa: E402
from scenarios import SCENARIOS  # noqa: E402


def load_recording(path):
    """A recorded events.jsonl -> [(seconds_from_start, event)] using the 't' stamps."""
    events = [json.loads(line) for line in open(path) if line.strip()]
    rid = next((e["round"] for e in events if e.get("round") is not None), "0")
    t0 = next((e["t"] for e in events if e.get("kind") != "reset" and "t" in e), None)
    out = []
    for e in events:
        if e.get("kind") == "reset":
            continue
        at = (e.get("t", t0) - t0) if t0 is not None else 0.0
        e = {k: v for k, v in e.items() if k != "t"}
        out.append((max(0.0, at) + 0.5, e))
    return str(rid), out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--round", default="3")
    p.add_argument("--file", help="replay a recorded events.jsonl instead of a scripted round")
    p.add_argument("--events", default=paths.events())
    p.add_argument("--speed", type=float, default=1.0, help="2.0 = twice as fast")
    args = p.parse_args()

    if args.file:
        rid, script = load_recording(args.file)
    else:
        rid = norm(args.round)
        if rid is None or rid not in SCENARIOS:
            sys.exit(f"No scripted round {args.round!r}. Scripted: {' '.join(SCENARIOS)}")
        script = SCENARIOS[rid]

    os.makedirs(os.path.dirname(args.events), exist_ok=True)
    with open(args.events, "w") as f:  # truncating starts a fresh round in the renderer
        f.write(json.dumps({"kind": "reset", "round": rid}) + "\n")
    start = time.monotonic()
    for at, ev in script:
        delay = at / args.speed - (time.monotonic() - start)
        if delay > 0:
            time.sleep(delay)
        ev = dict(ev, round=rid, t=time.time())
        with open(args.events, "a") as f:
            f.write(json.dumps(ev) + "\n")
        print(f"{at:5.1f}s  {ev['kind']:<15} {ev.get('detail', '')}", flush=True)


if __name__ == "__main__":
    main()
