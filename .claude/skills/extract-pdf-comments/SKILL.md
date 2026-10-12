---
name: extract-pdf-comments
description: Use when the user wants to extract highlighted text and reviewer notes/comments from one or more annotated PDFs into markdown files organized by page.
allowed-tools: Bash(uv run *)
---

# Extract PDF Comments

Deterministically extracts every highlight annotation from a PDF — the
highlighted text plus its associated note — into a markdown file organized by
page. Extraction is coordinate-based via `pymupdf`, so always run the helper
script rather than reading/interpreting the PDF by hand.

Helper script (single PDF in → single markdown out):
`.claude/skills/extract-pdf-comments/scripts/extract_comments.py` (relative to the repository root)

## Instructions

1. **Resolve the input** from `$ARGUMENTS`, which may be a single PDF, several
   PDF paths, or a directory:
   - A directory → expand to the `*.pdf` files inside it (use `ls`/glob).
   - One or more PDF paths → use as-is.
   - **If `$ARGUMENTS` is empty**, use the AskUserQuestion tool to ask the user
     what to extract (a PDF path, several paths, or a folder) before running.

2. **Run the script once per PDF, in parallel.** Issue one Bash call per
   resolved PDF in a single message so they execute concurrently:

   ```
   uv run --with pymupdf python .claude/skills/extract-pdf-comments/scripts/extract_comments.py "<one-pdf>"
   ```

   Each run writes `<pdf-stem>-comments.md` next to its source PDF and prints a
   one-line summary (highlights + pages + output path) to stderr. The script
   only ever handles one PDF — this skill drives the fan-out across many.

3. `--with pymupdf` provides the dependency in an ephemeral environment, so no
   install step is needed. If the project's `pyproject.toml` already lists
   `pymupdf`, the flag is harmless.

4. **Report** the output file path(s) and the per-PDF highlight/page counts.

## Output format

Each generated markdown file looks like:

```
Page 1:

"Here is the highlighted text. It says some things."
- The note associated with it.

"Another highlighted text."
- The associated note.

Page 2:
...
```

Notes:
- Pages with no highlights are omitted; pages appear in ascending order.
- If a highlight has no associated note, the quoted text is still printed but
  the `-` bullet line is omitted.
- A highlight spanning multiple pages is attributed to the page where it first
  appears (it belongs to a single page's annotation list).
