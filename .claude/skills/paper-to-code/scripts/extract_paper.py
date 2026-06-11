#!/usr/bin/env python3
"""
Extract method-relevant sections from a research paper PDF.

Prints: abstract, introduction end, method/approach section,
training/implementation details, experiments/results start,
algorithm blocks, and any page containing a hyperparameter table.

Usage:
    uv run python scripts/extract_paper.py <pdf-path>
    uv run python scripts/extract_paper.py <pdf-path> --full
"""

import sys
import re
import pypdf


SECTION_KEYWORDS = [
    # method section headers
    r'\b(approach|method|model|architecture|framework|formulation|proposed)\b',
    # training/implementation
    r'\b(training|implementation detail|training detail|experimental setup|setup)\b',
    # results
    r'\b(experiment|result|evaluation|ablation|comparison)\b',
    # algorithm blocks
    r'(algorithm\s+\d|pseudocode|pytorch\s+pseudo)',
]

TABLE_KEYWORDS = [
    r'\b(epoch|batch.?size|learning.?rate|weight.?decay|temperature|momentum)\b',
    r'\b(optimizer|scheduler|augmentation|dropout|warmup)\b',
    r'\b(dim|depth|heads|patch.?size|hidden)\b',
]

IMPORTANCE = {
    'abstract': 3,
    'introduction': 2,
    'method': 3,
    'approach': 3,
    'architecture': 3,
    'training': 3,
    'implementation': 3,
    'experiment': 2,
    'ablation': 2,
    'result': 2,
    'conclusion': 1,
}


def score_page(text: str) -> int:
    text_lower = text.lower()
    score = 0
    for kw, points in IMPORTANCE.items():
        if kw in text_lower:
            score += points
    for pattern in SECTION_KEYWORDS:
        if re.search(pattern, text_lower):
            score += 2
    for pattern in TABLE_KEYWORDS:
        if re.search(pattern, text_lower):
            score += 1
    # algorithm pseudocode is always high value
    if re.search(r'(for .* in|\.backward\(\)|\.params\s*=|def )', text_lower):
        score += 5
    return score


def extract_key_pages(path: str, full: bool = False):
    r = pypdf.PdfReader(path)
    total = len(r.pages)
    print(f"Total pages: {total}", file=sys.stderr)

    pages = [(i, r.pages[i].extract_text() or "") for i in range(total)]

    if full:
        selected = list(range(total))
    else:
        # Always include: first 3 (title/abstract/intro), last 2 (conclusion/refs)
        always = set(range(min(3, total))) | set(range(max(0, total - 2), total))

        # Score all pages and take top N by score
        scored = sorted(enumerate(pages), key=lambda x: score_page(x[1][1]), reverse=True)
        top_n = min(10, total)
        high_score = {i for i, _ in scored[:top_n]}

        selected = sorted(always | high_score)

    seen = set()
    for i in selected:
        if i in seen:
            continue
        seen.add(i)
        text = pages[i][1]
        if not text.strip():
            continue
        print(f"\n{'=' * 60}")
        print(f"PAGE {i + 1} / {total}")
        print('=' * 60)
        print(text)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_paper.py <pdf-path> [--full]", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    full = "--full" in sys.argv
    extract_key_pages(path, full=full)


if __name__ == "__main__":
    main()
