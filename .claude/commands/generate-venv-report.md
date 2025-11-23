---
description: Generate a concise VENV_REPORT.md and minimal requirements.txt in the root directory, focused only on software needed to run the core replication pipeline. $ARGUMENTS
argument-hint:
  [Specify constraints and extra goals for this environment report.]
---

# Task

You are a computational social science research assistant focused on rigorous, reproducible code.
Create two files in the **project root**:

1. **VENV_REPORT.md** – a concise report following the reference template that summarizes software needed to run the core replication pipeline and next steps for the maintainer.
2. **requirements.txt** – a **minimal** list of third-party Python packages used only in the core pipeline (not tests, notebooks, or one-off utilities).

## Specific Instructions

> $ARGUMENTS

## Guidance

1. **Setup: Reference files**

   - Read:
     - `@.claude/reference/reference-venv-report.md` (structure/template).
     - `@CLAUDE.md` (project standards).
   - Create a scratch file `temp-software.txt` in the project root to jot down:
     - Core pipeline entry points.
     - Third-party Python packages used by the pipeline.
     - Local packages.
     - Other required software.

2. **Identify the core pipeline**

   - Determine how replication is meant to be run (from raw data to final outputs) by looking for:
     - Pipeline shell scripts in the `code/` directory.
     - Snakemake workflows (`Snakefile`) in the `workflow/` directory.
   - In `temp-software.txt` under **High-level pipeline**, list:
     - Main entry scripts/workflows.
     - Typical invocation commands (e.g., `snakemake -j`, `bash run_all.sh`).
   - Only code reachable from these entry points is considered **in-scope** for `requirements.txt`.

3. **Inspect the active Python environment (for versions)**

   - Assume the active Python environment is the reference.
   - Use `pip list` or `pip freeze` to see package versions.
   - Note the Python version and key libraries in `temp-software.txt` under **Python version / env**.

4. **Trace Python imports for pipeline code**

   - Starting from the pipeline entry scripts, follow imports through local modules to find third-party dependencies.
   - Use tools like `grep -r "import " .` to help, but focus on code reachable from the core pipeline.
   - In `temp-software.txt` under **Third-party Python (pipeline)**, list only third-party packages actually used by the pipeline.
   - Distinguish:
     - Standard library vs third-party.
     - Local modules vs external packages.

5. **Identify local packages and other software**

   - Note any **local project packages** (e.g., installed via `-e .`, `toolkit/`, `src/`, layout, or `setup.py`/`pyproject.toml`).
   - From pipeline scripts/workflows, identify other required software (e.g., Snakemake CLI, R, `ffmpeg`, `graphviz`, LaTeX).
   - Record in `temp-software.txt`:
     - Local packages under **Local packages** .
     - Other tools under **Other required software**.

6. **Create a minimal `requirements.txt`**

   - In the project root, create **`requirements.txt`**.
   - For each third-party Python package in **Third-party Python (pipeline)**:
     - Look up its version from the active environment.
     - Add a line `package_name==version`.
   - Do **not** include:
     - Packages used only in tests, dev tooling, docs, or exploratory notebooks.
     - Packages installed but unused by the core pipeline.

7. **Create `VENV_REPORT.md`**

   - In the project root, create **`VENV_REPORT.md`** following the section structure in:
     - `@.claude/reference/reference-venv-report.md`
   - Fill in the template using information from `temp-software.txt` and `requirements.txt`:
     - Add 3–5 short **high-level next steps** bullets at the top.
     - Under **Python version**, insert the actual Python version and a brief next-step note.
     - Under **Python `requirements.txt` file**, list only the third-party pipeline packages (matching `requirements.txt`) and their versions.
     - Under **Local project repository packages**, list local packages used in the pipeline.
     - Under **Other required software**, list non-Python tools needed for the pipeline.
   - Keep all text concise and action-oriented.

8. **Finalize**

   - Verify:
     - `requirements.txt` contains only pipeline runtime dependencies.
     - `VENV_REPORT.md` is consistent with `requirements.txt` and remains concise.
   - Leave `temp-software.txt` as an internal scratch record unless project standards say otherwise.
