#!/usr/bin/env bash
# Rebuild the knowledge base from the latest sources.
#   1. git pull in copilot-cli/ (changelog)
#   2. sparse-clone github/docs into a temp dir
#   3. render the pages in selected-pages.txt into docs/
#   4. rebuild docs/INDEX.md and changelog-by-topic.md
# Usage: knowledge/scripts/refresh.sh
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
kdir="$(dirname "$here")"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

git -C "$kdir/copilot-cli" pull --ff-only

git clone --depth 1 --filter=blob:none --sparse https://github.com/github/docs.git "$tmp/docs"
git -C "$tmp/docs" sparse-checkout set content/copilot data/reusables data/variables
snap="$(git -C "$tmp/docs" log -1 --format='%h (%cs)')"

rm -rf "$kdir/docs"
DOCS_SNAPSHOT="$snap" python3 -I "$here/render.py" "$tmp/docs" "$kdir/docs" "$here/selected-pages.txt" | grep -v '^ok' || true
DOCS_SNAPSHOT="$snap" python3 -I "$here/build_index.py" "$kdir"
echo "Done. Docs snapshot: $snap. CLI changelog: $(grep -m1 '^## ' "$kdir/copilot-cli/changelog.md")"
echo "Re-check cli-safety-controls.md quotes against the new pages."
