#!/usr/bin/env bash
# Capture help text from the installed Copilot CLI into knowledge/cli-live/.
# Runs only --help / help <topic>: no prompts, no AI credits.
set -euo pipefail

out="$(cd "$(dirname "$0")/.." && pwd)/cli-live"
mkdir -p "$out/help"
rm -f "$out"/help/*.txt

copilot version > "$out/version.txt" 2>&1
copilot --help > "$out/help/copilot.txt" 2>&1

topics=$(sed -n '/^Help Topics:/,/^$/p' "$out/help/copilot.txt" | awk 'NR>1 && NF {print $1}')
for t in $topics; do copilot help "$t" > "$out/help/topic-$t.txt" 2>&1; done

cmds=$(sed -n '/^Commands:/,/^$/p' "$out/help/copilot.txt" | awk 'NR>1 && NF {print $1}' | grep -v '^help$')
for c in $cmds; do copilot "$c" --help > "$out/help/cmd-$c.txt" 2>&1; done

echo "Captured $(head -1 "$out/version.txt") into $out"
echo "Update the version and findings in cli-live/README.md."
