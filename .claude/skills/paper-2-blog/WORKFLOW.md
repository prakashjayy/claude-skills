# Detailed Workflow

## Step 1 — Resolve paper ID and folder name

Extract the paper ID from any URL format:
- `https://arxiv.org/abs/2301.07041` → `2301.07041`
- `https://arxiv.org/pdf/2301.07041v2` → `2301.07041v2`
- Bare ID `2301.07041` → use as-is
- Non-arxiv URL (e.g. direct PDF link) → derive a slug from the filename

If folder name is missing, ask: *"Which folder should I save the paper and blog post to?"*

## Step 2 — Check uv and pypdf

```bash
uv --version 2>/dev/null || NEED_UV=1
[ -f pyproject.toml ] && echo "uv project exists" || NEED_INIT=1
uv run python -c "import pypdf" 2>/dev/null || NEED_PYPDF=1
```

- If uv is missing OR no `pyproject.toml` → invoke the **setup-uv skill** (`uv init .` in the current working directory, no `--torch`).
- If `pypdf` is missing → `uv add pypdf`.
- The uv environment lives at the root level, shared across all papers.

## Step 3 — Create folder and download PDF

```bash
mkdir -p <folder>
curl -L "<paper-url>" -o "<folder>/<paper-id>.pdf"
```

For arxiv papers the URL is `https://arxiv.org/pdf/<paper-id>`.

## Step 4 — Extract key pages

```bash
uv run python scripts/extract_pages.py <folder>/<paper-id>.pdf
```

This prints pages 1–6 (title, abstract, intro, methods start), middle 3 pages, and last 3 pages (results, conclusion, references). Title and authors appear on page 1.

## Step 5 — Identify math concepts, visual opportunities, and terminology mismatches

Build three lists from the extracted text:

**Math concepts** — every equation or formula a non-expert would not recognise:
- Name (e.g. "KL divergence", "softmax")
- Equation/section number where it appears

**Visual opportunities** — anything easier to grasp as a picture:
- What it shows (e.g. "training pipeline", "encoder-decoder architecture")
- Where in the paper it is described

**Terminology mismatches** — terms the paper uses in a way that diverges from their standard meaning in the broader ML/CS/statistics community:
- The term as used in the paper
- The standard definition a reader is likely to know
- How the paper actually uses it
- Where it first appears

Common mismatch patterns to look for:
- Supervised-learning term applied to an unsupervised setting (e.g. "concept drift" for P(X) shift, not P(Y|X) shift)
- Term borrowed from another field with a shifted meaning (e.g. "energy" in physics vs. energy-based models)
- Term with conflicting definitions across subfields (e.g. "regularisation", "attention", "inference")

## Step 6 — Create diagram PNGs

Ensure matplotlib is available:
```bash
uv run python -c "import matplotlib" 2>/dev/null || uv add matplotlib
```

For each visual opportunity, write and run a self-contained Python script using matplotlib. Save to `<folder>/<snake_case_name>.png`.

Diagram guidelines:
- Clear label on every box, arrow, and axis — no unexplained symbols
- 2–3 colours max
- Left-to-right flow for pipelines; top-to-bottom for hierarchies
- `bbox_inches='tight'`, `dpi=150`
- Verify each PNG exists before proceeding

## Step 7 — Write the blog post

Follow [BLOG-FRAMEWORK.md](BLOG-FRAMEWORK.md) for structure and writing rules.

**Terminology warnings:** For every mismatch from Step 5, insert a blockquote immediately after the term's first use. Format:
```markdown
> **⚠️ Terminology warning:** The paper uses **[term]** to mean [paper's meaning].
> In most [ML / statistics / CS] literature, **[term]** means [standard definition] — [concrete example of the distinction].
> The paper's usage is common in [subfield] but will mislead readers from [other context].
```

**Worked examples** (only if `--use-simple-examples` was passed): after applying BLOG-FRAMEWORK.md, add a concrete worked example for every technical concept, immediately after it is introduced, following [SIMPLE-EXAMPLES.md](SIMPLE-EXAMPLES.md).

**Diagrams:** embed with relative paths immediately after the step they illustrate:
```markdown
![One-sentence description of what the diagram shows](./diagram_name.png)
```

Save output to `<folder>/blog.md`.

## Step 8 — Confirm

Report:
- PDF path
- Blog path
- Each PNG created (name + one-line description)
- Blog title and one-line hook
