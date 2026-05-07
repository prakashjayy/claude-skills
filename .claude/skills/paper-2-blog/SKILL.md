---
name: paper-2-blog
description: Downloads an arxiv paper by URL or paper ID, reads it, and writes an accessible blog post explaining it from first principles as if to a curious 5-year-old — using analogies, plain language, and a clear story arc. Use when user mentions arxiv, a paper URL, a paper ID (e.g. 2301.07041), "explain this paper", "paper to blog", or "summarize research paper".
---

# Paper 2 Blog

Turns an arxiv paper into a first-principles blog post anyone can understand.

## Required inputs

- **arxiv URL or paper ID** — e.g. `https://arxiv.org/abs/2301.07041` or `2301.07041`
- **folder name** — where to save the PDF and blog. If not provided, **ask the user before proceeding**.

## Workflow

### Step 1 — Resolve paper ID and folder name

Extract the paper ID from any arxiv URL format:
- `https://arxiv.org/abs/2301.07041` → `2301.07041`
- `https://arxiv.org/pdf/2301.07041v2` → `2301.07041v2`
- Bare ID `2301.07041` → use as-is

If folder name is missing, ask: *"Which folder should I save the paper and blog post to?"*

### Step 2 — Check uv and pypdf in the current working directory

```bash
# 1. Is uv available?
uv --version 2>/dev/null || NEED_UV=1

# 2. Is there already a uv project here?
[ -f pyproject.toml ] && echo "uv project exists" || NEED_INIT=1

# 3. Is pypdf already installed?
uv run python -c "import pypdf" 2>/dev/null || NEED_PYPDF=1
```

- If uv is missing OR no `pyproject.toml` exists → invoke the **setup-uv skill** (`uv init .` in the current working directory, no `--torch`). Do NOT create a new folder for this.
- If `pypdf` is missing → run `uv add pypdf` from the current working directory.
- If everything is already in place → skip to Step 3.

The uv environment lives at the **root level where the skill is invoked**, shared across all papers.

### Step 3 — Create paper folder and download PDF

```bash
mkdir -p <folder>
curl -L "https://arxiv.org/pdf/<paper-id>" -o "<folder>/<paper-id>.pdf"
```

The folder is just a plain directory — no separate uv project inside it.

### Step 4 — Extract text from the PDF

Run from the **current working directory** (where the uv project lives), referencing the PDF by its path:

```bash
uv run python - <<'EOF'
import pypdf

path = "<folder>/<paper-id>.pdf"
r = pypdf.PdfReader(path)
total = len(r.pages)

chunks = list(range(min(6, total)))
middle = list(range(total//2 - 1, min(total//2 + 2, total)))
tail   = list(range(max(0, total - 3), total))
seen = set()
for i in chunks + middle + tail:
    if i not in seen:
        seen.add(i)
        print(f"\n--- PAGE {i+1} ---")
        print(r.pages[i].extract_text())
EOF
```

Title and authors appear on page 1. Abstract, intro, methods, results, and conclusion are the key sections.

### Step 5 — Write the blog post

Follow the framework in [BLOG-FRAMEWORK.md](BLOG-FRAMEWORK.md) exactly. Save output to `<folder>/blog.md`.

### Step 6 — Confirm

Tell the user: PDF at `<folder>/<paper-id>.pdf`, blog at `<folder>/blog.md`. Print the blog title and one-line hook.
