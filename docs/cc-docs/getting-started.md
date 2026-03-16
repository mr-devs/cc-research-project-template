# Getting Started

This repository is a starter template for computational social science research. It combines a standardized project structure with Claude Code slash commands (skills) that automate common research tasks — from organizing literature through writing a LaTeX manuscript. Clone it for any new project and adapt the structure to your needs.

## Prerequisites

The paper-writing pipeline requires two command-line tools:

| Tool | Purpose | Install |
|------|---------|---------|
| `pdftotext` | Extract text from PDFs | `brew install poppler` |
| `fbib` (via [`fetchbib`](https://github.com/mr-devs/fetchbib)) | Fetch BibTeX from DOI or title | `pip install fetchbib` |

Python environments are managed with [uv](https://docs.astral.sh/uv/):

```bash
# Initialize and activate the environment
uv venv
source .venv/bin/activate
uv sync
```

Verify the pipeline tools are available before running:

```bash
pdftotext -v
fbib --help
```

## The Paper-Writing Pipeline

The following steps take you from raw PDF files to a compiled LaTeX manuscript:

1. **Add PDFs** — Drop paper files into `lit_review/papers/` in the appropriate subdirectory. Use the naming convention `Author - YYYY - Title.pdf`.

2. **Clean filenames** — `/cleanup-pdf-names lit_review/papers/` — Renames PDFs to use underscores and standard hyphens, preventing filesystem issues in later steps.

3. **Build the bibliography** — `/create-bibtex lit_review/papers/` — Fetches BibTeX entries for each PDF (via DOI or title) and appends them to `paper/main.bib`.

4. **Summarize papers** — `/create-paper-summary lit_review/papers/` — Generates structured markdown summaries for each paper and saves them to `lit_review/paper_summaries/`.

5. **Develop the outline** — `/develop-outline` — Walks through an interactive conversation to build or refine `paper/outline.md`, optionally pulling in citation pointers from your summaries.

6. **Write the paper** — `/write-paper` — Drafts LaTeX sections from the outline and saves them to `paper/main.tex`, one section at a time with your review between each.

7. **Compile** —
   ```bash
   cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
   ```

## Where to Go Next

- [Repository & Code Management](repository-and-code-management.md) — Skills for creating scripts, maintaining READMEs, and managing your Python environment.
- [Literature Review](literature-review.md) — Skills for the full PDF → bibliography → summary workflow.
- [Paper Writing](paper-writing.md) — Skills for building outlines and writing LaTeX sections.
