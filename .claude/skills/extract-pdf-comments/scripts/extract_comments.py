#!/usr/bin/env python3
"""Extract highlighted text + associated notes from ONE PDF, grouped by page.

Usage:
    extract_comments.py <input.pdf> [output.md]

Writes a markdown file listing each highlighted quote followed by its note,
organized by page. If no output path is given, writes <pdf-stem>-comments.md
next to the source PDF.

This script intentionally handles a single PDF. Batch/directory processing is
driven by the extract-pdf-comments skill, which runs this once per PDF.
"""

import os
import re
import sys

try:
    import fitz  # pymupdf
except ImportError:
    sys.exit(
        "Error: pymupdf is not installed. Run with:\n    uv run --with pymupdf python <this script> <pdf>"
    )


def normalize(text: str) -> str:
    """Collapse whitespace/newlines so a multi-line span reads as one line."""
    return re.sub(r"\s+", " ", text).strip()


def highlight_text(page, annot) -> str:
    """Recover the underlying page text under a highlight's QuadPoints."""
    verts = annot.vertices or []
    fragments = []
    # vertices come in groups of 4 points (one quad per highlighted line)
    for i in range(0, len(verts), 4):
        quad = verts[i : i + 4]
        if len(quad) < 4:
            continue
        rect = fitz.Quad(quad).rect
        fragments.append(page.get_textbox(rect))
    return normalize(" ".join(fragments))


def extract(pdf_path: str, out_path: str) -> tuple[int, int]:
    """Extract highlights from pdf_path into out_path. Returns (count, pages)."""
    doc = fitz.open(pdf_path)
    by_page = {}
    total = 0
    for pno in range(doc.page_count):
        page = doc[pno]
        for annot in page.annots() or []:
            if annot.type[1] != "Highlight":
                continue
            text = highlight_text(page, annot)
            note = (annot.info.get("content") or "").strip()
            by_page.setdefault(pno + 1, []).append((text, note))
            total += 1

    lines = []
    for page_num in sorted(by_page):
        lines.append(f"Page {page_num}:")
        lines.append("")
        for text, note in by_page[page_num]:
            lines.append(f'"{text}"')
            if note:
                lines.append(f"- {normalize(note)}")
            lines.append("")
    lines.append("")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))

    return total, len(by_page)


def main(argv):
    if len(argv) < 2:
        sys.exit(
            "Usage: extract_comments.py <input.pdf> [output.md]\n"
            "Extracts highlighted text + notes from a single PDF into markdown."
        )

    pdf_path = argv[1]
    if not os.path.isfile(pdf_path):
        sys.exit(f"Error: PDF not found: {pdf_path}")

    if len(argv) >= 3:
        out_path = argv[2]
    else:
        stem = os.path.splitext(pdf_path)[0]
        out_path = f"{stem}-comments.md"

    total, pages = extract(pdf_path, out_path)
    print(
        f"Extracted {total} highlights across {pages} pages -> {out_path}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main(sys.argv)
