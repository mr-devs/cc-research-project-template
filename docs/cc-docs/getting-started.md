# Getting Started

This repository is a starter template for computational social science research.
It combines a standardized project structure with Claude Code slash commands (skills) that automate common research tasks — from organizing literature through writing a LaTeX manuscript.

The high-level system is meant to work like this:
1. Create a project on Overleaf
2. Use the Overleaf Github integration to create a new, synced repository on Github ([learn more](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/github-synchronization))
3. Pull that repository down to your local machine
4. After cloning this repository, copy the files from this repository into your new project repository
5. Work in your new project repository (analyses, writing, etc.) syncing to Github/Overleaf as necessary

> **Note**: As of writing this, there is no way of syncing an existing repository from Github into Overleaf.
> If that changes, _please_ let me know, as the above could be simplified quite a bit.

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

The idea behind this pipeline is that a researcher can drop a set of PDF documents that they are **already familiar with** and then the pipeline will:

1. Generate proper bib items for a LaTeX `.bib` file
2. Extact and summary key details in a markdown file that is easier for an AI to read

After that, the researcher works iteratively with an AI to develop a rough outline, which can then be leveraged to actually write the paper.
The system is designed to allow the user to work on specific sections of the paper, as opposed to the entire thing at once, and will ask the user to review new edits before making changes.
Critical to this system is the presence of the bib keys within the generated paper summaries, ensuring that LaTeX `\cite` commands get citations correct

> **Warning**: This pipeline will likely not be perfect.
> As stated above, this system is meant to be leveraged by someone who has _already read the input PDFs_, which should allow them to catch obvious mistakes in AI generated writing.

The following steps take you from raw PDF files to a compiled LaTeX manuscript:

1. **Add PDFs**: Drop paper files into `lit_review/papers/` in the appropriate subdirectory. Use the naming convention `Author - YYYY - Title.pdf`.
2. **Clean filenames**: `/cleanup-pdf-names lit_review/papers/` — Renames PDFs to use underscores and standard hyphens, preventing filesystem issues in later steps.
3. **Build the bibliography**: `/create-bibtex lit_review/papers/` — Fetches BibTeX entries for each PDF (via DOI or title) and appends them to `paper/main.bib`.
4. **Summarize papers**: `/create-paper-summary lit_review/papers/` — Generates structured markdown summaries for each paper and saves them to `lit_review/paper_summaries/`.
5. **Develop the outline**: `/develop-outline` — Walks through an interactive conversation to build or refine `paper/outline.md`, optionally pulling in citation pointers from your summaries.
6. **Write the paper**: `/write-paper` — Drafts LaTeX sections from the outline. For Introduction and Discussion, uses paper summaries for citation context. For Results and Methods, reads the artifact files listed in the outline (reports, scripts, data); if none are listed, prompts you to provide them. Presents each draft for your review before saving to `paper/main.tex`. (**Note**: The writing style will be based on `.claude/reference/venue-info.md` (venue structure and PNAS section guidance), `.claude/reference/writing-style.md` (sentence-level writing style, derived from [Gopen & Swan, 1990](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf)), and `.claude/reference/latex-rules.md` (LaTeX formatting rules).)



## Where to Go Next

- [Repository & Code Management](repository-and-code-management.md) — Skills for creating scripts, maintaining READMEs, and managing your Python environment.
- [Literature Review](literature-review.md) — Skills for the full PDF → bibliography → summary workflow.
- [Paper Writing](paper-writing.md) — Skills for building outlines and writing LaTeX sections.
