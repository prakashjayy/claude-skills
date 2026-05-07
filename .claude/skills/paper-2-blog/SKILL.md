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

### Step 1 — Resolve paper ID and folder

Extract the paper ID from any arxiv URL format:
- `https://arxiv.org/abs/2301.07041` → `2301.07041`
- `https://arxiv.org/pdf/2301.07041v2` → `2301.07041v2`
- Bare ID `2301.07041` → use as-is

If folder name is missing, ask: *"Which folder should I save the paper and blog post to?"*

### Step 2 — Download paper and metadata

```bash
mkdir -p <folder>

# Download PDF
curl -L "https://arxiv.org/pdf/<paper-id>" -o "<folder>/<paper-id>.pdf"

# Fetch metadata (title, authors, abstract)
curl -s "https://export.arxiv.org/api/query?id_list=<paper-id>" -o "<folder>/metadata.xml"
```

### Step 3 — Extract metadata

Parse `metadata.xml` for: title, authors, published date, abstract. Use `grep` or read the XML directly.

### Step 4 — Read the paper

Use the Read tool on `<folder>/<paper-id>.pdf`. For papers > 10 pages read in sections: abstract + intro first, then methods, then results, then conclusion.

### Step 5 — Write the blog post

Follow the framework in [BLOG-FRAMEWORK.md](BLOG-FRAMEWORK.md) exactly. Save output to `<folder>/blog.md`.

### Step 6 — Confirm

Tell the user: paper saved at `<folder>/<paper-id>.pdf`, blog at `<folder>/blog.md`. Print the blog title and one-line hook.
