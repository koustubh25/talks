#!/usr/bin/env python3
"""Tell the round slides where the presenter is.

presenterm --publish-speaker-notes sends a UDP datagram to 127.0.0.1:59418 on every
slide change: {"event": {"command": "GoTo", "slide": N, "chunk": C}}. This writes the
latest one to <stage>/.vault/cue.json, which each round's runner box watches
(deckrun.py --cue). present.sh starts it and stops it when the deck closes.
"""
import json
import os
import socket
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths  # noqa: E402

ADDR = ("127.0.0.1", 59418)


def cue_file():
    return os.path.join(paths.stage(), ".vault", "cue.json")


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind(ADDR)
    except OSError as e:
        sys.exit(f"cue: can't listen on {ADDR[0]}:{ADDR[1]} ({e}). Is another deck open?")
    path = cue_file()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    while True:
        data = s.recv(65536)
        try:
            ev = json.loads(data)["event"]
        except (ValueError, KeyError, TypeError):
            continue
        if ev.get("command") != "GoTo":
            continue
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"slide": ev.get("slide"), "chunk": ev.get("chunk", 0), "t": time.time()}, f)
        os.replace(tmp, path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
