#!/usr/bin/env python3
"""Extract key pages from a PDF: first 6, middle 3, last 3."""
import sys
import pypdf

def extract_key_pages(path):
    r = pypdf.PdfReader(path)
    total = len(r.pages)
    print(f"Total pages: {total}", file=sys.stderr)

    chunks = list(range(min(6, total)))
    middle = list(range(total // 2 - 1, min(total // 2 + 2, total)))
    tail   = list(range(max(0, total - 3), total))

    seen = set()
    for i in chunks + middle + tail:
        if i not in seen:
            seen.add(i)
            print(f"\n--- PAGE {i+1} ---")
            print(r.pages[i].extract_text())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: extract_pages.py <pdf-path>", file=sys.stderr)
        sys.exit(1)
    extract_key_pages(sys.argv[1])
