"""Build docs/INDEX.md (per-page summary + headings) and changelog-by-topic.md.

Usage: python3 -I build_index.py <knowledge_dir>
"""
import os
import re
import sys

kdir = sys.argv[1]
docs = os.path.join(kdir, "docs")

# ---- docs index ----
groups = {}
for root, _, files in os.walk(docs):
    for f in sorted(files):
        if not f.endswith(".md") or f == "INDEX.md":
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, docs)
        text = open(p).read()
        title = text.splitlines()[0].lstrip("# ").strip()
        m = re.search(r"^_(.+)_$", text, re.M)
        intro = m.group(1) if m else ""
        heads = [h.strip() for h in re.findall(r"^## (.+)$", text, re.M)]
        words = len(text.split())
        groups.setdefault(os.path.dirname(rel), []).append((rel, title, intro, heads, words))

out = ["# Copilot CLI docs index", "",
       f"Official docs.github.com pages rendered to markdown (github/docs @ {os.environ.get('DOCS_SNAPSHOT', 'unknown')}).",
       "Each entry: title, one-line intro, word count, and its `##` sections. Grep this file to find the right page.", ""]
for d in sorted(groups):
    out.append(f"## {d}/")
    out.append("")
    for rel, title, intro, heads, words in groups[d]:
        out.append(f"- **[{title}]({rel})** ({words} words): {intro}")
        if heads:
            out.append("  - Sections: " + " · ".join(heads))
    out.append("")
open(os.path.join(docs, "INDEX.md"), "w").write("\n".join(out))

# ---- changelog by topic ----
cl = open(os.path.join(kdir, "copilot-cli", "changelog.md")).read()
entries = []
version = None
for line in cl.splitlines():
    m = re.match(r"^## (\S+) - (\S+)", line)
    if m:
        version = f"{m.group(1)} ({m.group(2)})"
        continue
    if line.startswith("- ") and version:
        entries.append((version, line[2:].strip()))

topics = [
    ("Sandbox", r"sandbox"),
    ("Permissions, approvals, allow/deny", r"permission|approv|allow-all|--allow|--deny|yolo|deny rule|allowed ?url|trusted folder|trust"),
    ("Assisted permissions / auto-approval judge", r"assisted|judge|auto-approv"),
    ("Hooks", r"\bhook"),
    ("Modes: Plan, Autopilot, Interactive", r"autopilot|plan mode|\bplan\b|shift\+tab|interactive mode"),
    ("Custom instructions (AGENTS.md, copilot-instructions)", r"instruction|agents\.md|claude\.md"),
    ("Skills", r"\bskill"),
    ("Custom agents and subagents", r"custom agent|subagent|sub-agent|/agent\b"),
    ("MCP", r"\bmcp\b"),
    ("Plugins and marketplaces", r"plugin|marketplace"),
    ("Enterprise, organization and managed policy", r"enterprise|organization|admin|managed|policy|policies"),
    ("Content exclusion", r"exclu"),
    ("Worktrees and parallel sessions", r"worktree|/fleet|fleet|parallel"),
    ("Undo, rewind, checkpoints", r"rewind|undo|checkpoint|roll ?back|snapshot"),
    ("Pull requests, review, diff", r"/pr\b|pull request|/review|/diff|code review"),
    ("Delegation and cloud agent", r"delegate|cloud agent|coding agent|remote"),
    ("Dynamic workflows", r"workflow"),
    ("Secrets and credentials", r"secret|token|credential|redact"),
]
cout = ["# Changelog by topic", "",
        "Every bullet from `copilot-cli/changelog.md` (188 releases, newest first, up to 1.0.103 on 2026-10-22), grouped by keyword.",
        "A bullet can appear under more than one topic. Keyword matching is crude: always read the bullet before quoting it.", ""]
cout.append("Topics: " + " · ".join(f"[{t}](#{re.sub(r'[^a-z0-9 -]', '', t.lower()).replace(' ', '-')})" for t, _ in topics))
cout.append("")
for name, pat in topics:
    rx = re.compile(pat, re.I)
    hits = [(v, e) for v, e in entries if rx.search(e)]
    cout.append(f"## {name}")
    cout.append("")
    cout.append(f"{len(hits)} entries.")
    cout.append("")
    for v, e in hits:
        cout.append(f"- `{v}` {e}")
    cout.append("")
open(os.path.join(kdir, "changelog-by-topic.md"), "w").write("\n".join(cout))
print(sum(len(v) for v in groups.values()), "pages;", len(entries), "changelog bullets")
