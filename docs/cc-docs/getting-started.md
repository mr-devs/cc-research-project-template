# Getting Started

This repository is a starter template for computational social science research.
It combines a standardized project structure with Claude Code slash commands (skills) that automate common research tasks, including analysis and writing.

The high-level system is meant to work like this:

1. Create a blank project on Overleaf
2. Use the Overleaf Github integration to create a new, synced repository on Github ([learn more](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/github-synchronization))
3. Pull that repository down to your local machine
4. After cloning this repository, copy the files from this repository into your new project repository
5. Work in your new project repository (analyses, writing, etc.) syncing to Github/Overleaf as necessary

> **Note**: The Overleaf–GitHub integration requires starting from a new Overleaf project.
> Syncing an existing GitHub repository into Overleaf is not currently supported.
> If you are not using Overleaf, skip steps 1–2 and initialize a plain GitHub repository instead.

## Prerequisites

The following command-line tools are required:

| Tool | Purpose | Install |
| ------ | --------- | --------- |
| `uv` | Python environment management | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| `pdftotext` | Extract text from PDFs | `brew install poppler` |
| `fbib` (via [`fetchbib`](https://github.com/mr-devs/fetchbib)) | Fetch BibTeX from DOI or title | `uv tool install fetchbib` |
| `snakemake` *(optional)* | Workflow orchestration | `uv tool install snakemake` |

Set up the Python environment:

```bash
uv venv
source .venv/bin/activate
uv sync
```

Install the pipeline tools:

```bash
brew install poppler
uv tool install fetchbib  # installs the `fbib` command
```

Verify the pipeline tools are available before running:

```bash
pdftotext -v
fbib --help
```

## The Coding & Analysis Pipeline

1. **Set up the environment**: Run `uv venv && source .venv/bin/activate && uv sync`. Add packages with `uv add <package>` so dependencies are tracked in `pyproject.toml`.
2. **Create scripts**: `/create-script` — Guides you through creating a new script in the appropriate `code/` subdirectory, pre-populated with the project-standard header and a `main()` stub. Structure based on [`.claude/skills/create-script/reference-script.py`](../../.claude/skills/create-script/reference-script.py), alter for your own preferences.
3. **Run analyses**: Conduct your study/analyses and generate figures/tables for the paper. Save figures to `results/figures/`, generate LaTeX tables to `results/tables/`, and other statistical reports in `results/reports/`. For complex, multi-step pipelines, use the Snakemake workflows in `workflow/` to orchestrate execution.
4. **Integrate results into the paper**: Use `/write-paper` to draft sections from your outline, pointing it to the relevant scripts, reports, and figures.
5. **Prepare for publication**: `/generate-venv-report` — Documents all installed packages and versions to ensure the environment is reproducible.

## The Paper-Writing Pipeline

> **Warning**: This pipeline is designed for researchers who have **already read the input PDFs**.
> AI-generated writing will contain mistakes; familiarity with the source material is essential for catching them.

The pipeline takes a folder of PDFs and:

1. Generates proper BibTeX entries for a LaTeX `.bib` file
2. Extracts and summarizes key details into structured markdown files that are easier for an AI to read

After that, you work iteratively with the AI to develop a rough outline, which is then used to write individual sections of the paper.
The system is designed to let you focus on one section at a time and review each draft before it is saved.
BibTeX keys are embedded in the generated summaries so that `\cite` commands are accurate throughout.

The following steps take you from raw PDF files to a compiled LaTeX manuscript:

1. **Add PDFs**: Drop paper files into `lit_review/papers/` in the appropriate subdirectory. Use the naming convention `Author - YYYY - Title.pdf`.
2. **Clean filenames**: `/cleanup-pdf-names lit_review/papers/` — Renames PDFs to use underscores and standard hyphens, preventing filesystem issues in later steps.
3. **Build the bibliography**: `/create-bibtex lit_review/papers/` — Fetches BibTeX entries for each PDF (via DOI or title) and appends them to `paper/main.bib`.
4. **Summarize papers**: `/create-paper-summary lit_review/papers/` — Generates structured markdown summaries for each paper and saves them to `lit_review/paper_summaries/`.
5. **Develop the outline**: `/develop-outline` — Walks through an interactive conversation to build or refine `paper/outline.md`, optionally pulling in citation pointers from your summaries.
6. **Write the paper**: `/write-paper` — Drafts LaTeX sections from the outline and presents each draft for your review before saving to `paper/main.tex`.
   - For Introduction and Discussion sections, uses paper summaries for citation context.
   - For Results and Methods sections, reads artifact files listed in the outline (reports, scripts, data); if none are listed, prompts you to provide them.
   - Writing style is governed by three reference files:
     - [`.claude/reference/venue-info.md`](../../.claude/reference/venue-info.md) — venue structure and section guidance
     - [`.claude/reference/writing-style.md`](../../.claude/reference/writing-style.md) — sentence-level style, derived from [Gopen & Swan, 1990](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf)
     - [`.claude/reference/latex-rules.md`](../../.claude/reference/latex-rules.md) — LaTeX formatting rules

## Where to Go Next

- [Repository & Code Management](repository-and-code-management.md) — Skills for creating scripts, maintaining READMEs, and managing your Python environment.
- [Literature Review](literature-review.md) — Skills for the full PDF → bibliography → summary workflow.
- [Paper Writing](paper-writing.md) — Skills for building outlines and writing LaTeX sections.
