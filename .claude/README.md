# Continuing this project on another machine

Everything Claude Code needs to pick up where we left off is committed here.

## What's in this folder

- `agents/azure-evals-expert.md` — the Azure/Foundry subagent. Auto-available when
  you open Claude Code anywhere in this repo.
- `skills/ai-evals-talk/` — the talk-prep skill: SKILL.md plus `references/`
  (distilled notes from the AI-evals videos, and the Azure-2026 research). Invoke
  it with `/ai-evals-talk`.
- `memory/` — a **snapshot** of the auto-memory (who Koustubh is, the no-em-dash
  rule, the learnings-log pointer, etc.). This is a copy, not live memory.

The slides and notes live in `../talk/` (concept deck: `../talk/slides/concept.html`).

## First-time setup on a new machine

1. Clone and open Claude Code in the repo root. The skill and subagent are picked
   up automatically from `.claude/`.

2. Reactivate the memory so Claude loads it every session. From the repo root:

   ```bash
   DEST=~/.claude/projects/$(pwd | sed 's#/#-#g')/memory
   mkdir -p "$DEST"
   cp .claude/memory/*.md "$DEST"/
   ```

   (Auto-memory is keyed to the folder path, so it can't travel in the repo — this
   copies the snapshot into the new machine's per-project memory location.)

3. Tools you'll need for the decks:
   - a browser (the concept deck is a single self-contained HTML file)
   - `presenterm` + Chrome, only if you want to run the terminal deck or re-bake
     the 4K slide PNGs
