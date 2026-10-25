"""Render selected github/docs pages to plain markdown.

Usage: python3 -I render.py <docs_repo> <out_dir> <list_file>
list_file: one path per line, relative to content/copilot.
Resolves {% data reusables.* %} and {% data variables.* %}, rewrites
[AUTOTITLE](/copilot/...) links, keeps title/intro, adds a source URL.
"""
import os
import re
import sys

import yaml

repo, out_dir, list_file = sys.argv[1:4]
content_root = os.path.join(repo, "content", "copilot")
SNAPSHOT = os.environ.get("DOCS_SNAPSHOT", "unknown")
selected = [l.strip() for l in open(list_file) if l.strip() and not l.startswith("#")]
selected_set = set(selected)

# Map old URLs (redirect_from) to selected pages so links resolve locally.
redirects = {}
for rel in selected:
    p = os.path.join(content_root, rel)
    if not os.path.exists(p):
        continue
    head = open(p).read()
    if head.startswith("---"):
        meta = yaml.safe_load(head.split("---", 2)[1]) or {}
        for old in meta.get("redirect_from") or []:
            redirects[re.sub(r"^/(en/)?copilot/", "", old).strip("/")] = rel

_var_cache = {}


def lookup_var(dotted):
    parts = dotted.split(".")
    fname = parts[0]
    if fname not in _var_cache:
        p = os.path.join(repo, "data", "variables", fname + ".yml")
        _var_cache[fname] = yaml.safe_load(open(p)) if os.path.exists(p) else {}
    node = _var_cache[fname]
    for k in parts[1:]:
        if not isinstance(node, dict) or k not in node:
            return None
        node = node[k]
    return str(node) if not isinstance(node, dict) else None


DATA_RE = re.compile(r"\{%-?\s*data\s+([\w.\-/]+)\s*-?%\}")


def resolve(text, depth=0):
    def repl(m):
        ref = m.group(1)
        kind, _, rest = ref.partition(".")
        if kind == "variables":
            v = lookup_var(rest)
            return resolve(v, depth + 1) if v is not None else m.group(0)
        if kind == "reusables" and depth < 6:
            p = os.path.join(repo, "data", "reusables", *rest.split(".")) + ".md"
            if os.path.exists(p):
                return resolve(open(p).read().strip(), depth + 1)
        return m.group(0)

    return DATA_RE.sub(repl, text)


LINK_RE = re.compile(r"\]\((/(?:en/)?copilot/[^)#\s]*)(#[^)\s]*)?\)")


def rewrite_links(text, src_rel):
    def repl(m):
        path, anchor = m.group(1), m.group(2) or ""
        rel = re.sub(r"^/(en/)?copilot/", "", path).strip("/")
        for cand in (rel + ".md", rel + "/index.md", redirects.get(rel, "")):
            if cand in selected_set:
                target = os.path.relpath(cand, os.path.dirname(src_rel))
                return f"]({target}{anchor})"
        return f"](https://docs.github.com/en/copilot/{rel}{anchor})"

    return LINK_RE.sub(repl, text)


def clean(text):
    text = re.sub(r"\{%\s*octicon[^%]*%\}", "", text)
    text = re.sub(r"\{%\s*(raw|endraw)\s*%\}", "", text)
    text = re.sub(r"\{%\s*(note|tip|warning|important|caution)\s*%\}", r"> **\1:**", text)
    text = re.sub(r"\{%\s*end(note|tip|warning|important|caution)\s*%\}", "", text)
    text = re.sub(r"\{%\s*(rowheaders|endrowheaders)\s*%\}", "", text)
    text = re.sub(r"^>\s*\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]", lambda m: "> **" + m.group(1).lower() + ":**", text, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", text)


for rel in selected:
    src = os.path.join(content_root, rel)
    if not os.path.exists(src):
        print("MISSING", rel, file=sys.stderr)
        continue
    raw = open(src).read()
    fm, body = {}, raw
    if raw.startswith("---"):
        _, fm_text, body = raw.split("---", 2)
        fm = yaml.safe_load(fm_text) or {}
    title = resolve(str(fm.get("title", rel)))
    intro = resolve(str(fm.get("intro", ""))).strip()
    url_path = rel[:-3]
    if url_path.endswith("/index"):
        url_path = url_path[: -len("/index")]
    url = f"https://docs.github.com/en/copilot/{url_path}"
    body = clean(rewrite_links(resolve(body), rel))
    header = f"# {title}\n\n> Source: {url}\n> Snapshot: github/docs @ {SNAPSHOT}\n"
    if intro:
        header += f"\n_{intro}_\n"
    dst = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as f:
        f.write(header + "\n" + body.strip() + "\n")
    print("ok", rel)
