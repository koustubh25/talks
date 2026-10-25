#!/usr/bin/env bash
# Opens the deck, with the round slides sized for this window (resize first).
#   --present  no live reload (a reload would start a second set of vaults)
#   -P         report each slide change, so → can start a round (vault/cue.py)
#   -X         the vaults and the round prompts start by themselves
#   -x         ctrl+e for Round 5 (full-screen Copilot)
cd "$(dirname "$0")" || exit 1
python3 build_rounds.py "$(tput cols)" "$(tput lines)" || exit 1
../demo/southbank-vault/vault/cue.py &
CUE=$!
trap 'kill $CUE 2>/dev/null' EXIT
presenterm --present -P -x -X deck.md "$@"
