# cc-research-project-template

A research project repository template, built for Claude Code.
Custom Claude code functions are included with reference files to streamline research workflows.
For example, a `/create-script` function is intended to create a Python script that follows structural best practices outlines in a reference script.
See the `.claude/command/` and `.claude/reference/` directories for the functions and reference files, respectively.

## Contents

- `.claude/`: Files related to Claude code are saved here
- `code/`: All source code including analysis scripts, data collection, cleaning, and utilities
- `data/`: Data files organized by processing stage (raw, interim, processed, external)
- `results/`: Output files generated from analysis (tables and figures)
- `workflow/`: Snakemake workflow files for data collection and analysis pipelines
- `lit_review/`: PDF papers and AI-generated summaries for the literature review phase
- `paper/`: LaTeX manuscript files (outline, bibliography, and main document)
- `CLAUDE.md`: Claude Code-specific instructions and context
