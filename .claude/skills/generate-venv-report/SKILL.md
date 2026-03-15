---
name: generate-venv-report
description: Generate a VENV_REPORT.md in the project root summarizing the software environment needed to run the core replication pipeline. Uses pyproject.toml and uv.lock as the source of truth. $ARGUMENTS
argument-hint:
  [Specify constraints and extra goals for this environment report.]
disable-model-invocation: true
---

# Task

You are a computational social science research assistant focused on rigorous, reproducible code.
Create **`VENV_REPORT.md`** in the project root: a concise report following the reference template that summarizes the software environment needed to run the core replication pipeline and provides next steps for the maintainer.

`pyproject.toml` and `uv.lock` are the source of truth for Python dependencies — do **not** generate a `requirements.txt`.

## Specific Instructions

> $ARGUMENTS

## Guidance

### Step 1 — Setup: Read reference files and check prerequisites

- Read `@.claude/skills/generate-venv-report/reference-venv-report.md` (structure/template).
- Read `@CLAUDE.md` (project standards).
- Check prerequisites and **halt** with clear guidance if not met:
  - **`.venv/` missing** → stop and tell the user: "Virtual environment not found. Run `uv venv && uv sync` to create and populate it."
  - **`pyproject.toml` missing** → stop and tell the user: "No `pyproject.toml` found. Run `uv init` to initialize the project, then `uv add <package>` to add dependencies."
  - **`uv.lock` missing** → do not halt, but record a warning to include prominently in the report.

### Step 2 — Identify the core pipeline

- Look for pipeline entry points in:
  - Snakemake workflows (`Snakefile`) under `workflow/`
  - Shell scripts under `code/`
- Note main entry scripts/workflows and their typical invocation commands (e.g., `snakemake -j`, `bash run_all.sh`).
- Only code reachable from these entry points is **in-scope** for the report.

### Step 3 — Inspect the virtual environment without activation

- Record the Python version: run `.venv/bin/python --version`
- List installed packages: run `uv pip list --python .venv/bin/python`
  - Fallback: `.venv/bin/python -m pip list`

### Step 4 — Read `pyproject.toml` and `uv.lock`

- Extract direct dependencies from `[project.dependencies]` in `pyproject.toml`.
- Extract pinned versions from `uv.lock`.
- Cross-reference declared deps against installed packages from Step 3 to catch any discrepancies.

### Step 5 — Trace Python imports for pipeline code

- Starting from the pipeline entry scripts, search `import` / `from ... import` statements in pipeline-reachable files.
- Classify each import:
  - **stdlib** — exclude from the report.
  - **local module** — note separately.
  - **third-party** — include in the report.
- **Flag** any third-party package used by the pipeline but **not declared** in `pyproject.toml` — include this as a warning in the report.

### Step 6 — Identify local packages and other software

- **Local packages**: look for `toolkit/`, `src/`, editable installs (`-e .`), or `[tool.uv.sources]` entries pointing to local paths.
- **Other software**: scan pipeline scripts/workflows for non-Python tools (e.g., Snakemake CLI, R, LaTeX, `ffmpeg`, `graphviz`).

### Step 7 — Check for existing `VENV_REPORT.md` and generate the updated report

- If `VENV_REPORT.md` already exists:
  - Read the current file.
  - Summarize the key changes to the user before overwriting (e.g., "Python version updated X→Y, 2 packages added, 1 removed").
- Write `VENV_REPORT.md` in the project root using the structure from `reference-venv-report.md`:
  - Fill in actual Python version, dependency list with pinned versions, local packages, and other tools.
  - If `uv.lock` is missing, include a prominent warning under **Python dependencies**.
  - If any pipeline imports are undeclared in `pyproject.toml`, include a warning listing the offending packages.
- Keep all text concise and action-oriented.

### Step 8 — Finalize and summarize

- Confirm `VENV_REPORT.md` was created or updated.
- Report any warnings to the user:
  - Missing `uv.lock`
  - Undeclared pipeline dependencies
- Provide a brief summary: Python version, number of declared dependencies, local packages found, other tools found.
