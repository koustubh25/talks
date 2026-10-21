#!/usr/bin/env bash
# Launch the talk deck. -X enables auto-rendered (exec_replace) diagram blocks.
cd "$(dirname "$0")"
exec presenterm -x -X demo.md
