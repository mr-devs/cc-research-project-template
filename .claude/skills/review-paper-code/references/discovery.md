# Project Discovery Reference

Read this during Phase 2 (Discover the project) when the user did not pass explicit paths, or when you need the exact globs and exclusion lists.

Exclude build and cache folders everywhere: `_minted-*`, `build/`, `output/` (for paper search only), `.git/`, `node_modules/`, `__pycache__/`, `.quarto/`, `_site/`.

## 1. Find the paper

Glob for candidates, in this order:

1. `**/*.tex`
2. `**/*.qmd`
3. `**/*.Rmd`

A file is a main paper file if:
- `.tex`: contains `\documentclass` or `\begin{document}`
- `.qmd` / `.Rmd`: has YAML frontmatter with `title:`

If several qualify, prefer:
1. A path explicitly provided in the arguments
2. A file in `Writing/`, `writing/`, `Paper/`, `paper/`, `Draft/`, `draft/`, or the repo root
3. The file that pulls in the most component files via `\input{}` / `\include{}` / `\subfile{}`

Record as `PAPER_FILE`.

## 2. Find the code directory

If `CODE_DIR` was not provided, look for likely code roots in this order:
- `Code/`, `code/`, `Analysis/`, `analysis/`, `scripts/`, `Scripts/`
- `src/`, `programs/`, `Programs/`, `replication/`, `Replication/`
- `do/`, `R/`, `python/`, `stata/`

If no single directory is clearly best, use the repo root. Record as `CODE_DIR`.

## 3. Find code files

Within `CODE_DIR` and its subdirectories:

| Pattern | Language |
|---|---|
| `**/*.do` | Stata |
| `**/*.R`, `**/*.r` | R |
| `**/*.py` | Python |
| `**/*.jl` | Julia |
| `**/*.m` | MATLAB |
| `**/*.sas` | SAS |
| `**/*.ipynb` | Jupyter notebook |
| `**/*.Rmd`, `**/*.qmd` | RMarkdown / Quarto (analysis notebooks) |
| `**/*.sh`, `**/*.bash` | Shell (pipeline orchestration) |

Exclude: `__pycache__/`, `.ipynb_checkpoints/`, `renv/`, `venv/`, `.venv/`, `env/`, `node_modules/`, `.git/`.

**If `REVIEW_DEPTH = main`**, prioritize:
- Master scripts: `main.*`, `master.*`, `run_all.*`, `run.*`, `Makefile`, `makefile`, `_targets.R`
- Files referenced or called by master scripts
- Files whose names suggest they produce tables or figures (`table_*.R`, `fig_*.py`, `*_results.*`)
- Cap the initial review set at ~15 files; note the remainder as out of scope

**If `REVIEW_DEPTH = full`**, include all detected code files.

Record `CODE_FILES_ALL` (every code file found), `CODE_FILES_REVIEWED` (files selected), and `LANGUAGES` (languages present).

## 4. Find output artifacts

- Data: `**/*.csv`, `**/*.dta`, `**/*.rds`, `**/*.parquet`, `**/*.arrow` in data/output directories
- Figures: `**/*.pdf`, `**/*.png`, `**/*.eps`, `**/*.svg` in `figures/`, `Figures/`, `output/`, `results/`, or root
- Tables: `**/*.tex`, `**/*.csv`, `**/*.html` in `tables/`, `Tables/`, `output/`, `results/`
- Logs: `**/*.log`, `**/*.txt` in `log/`, `logs/`, `output/`

Record as `OUTPUT_FILES`.

## 5. Find supporting documentation

- `README.md`, `README.txt`, `readme.md`, `README`
- `requirements.txt`, `environment.yml`, `pyproject.toml`, `setup.py`, `setup.cfg`
- `renv.lock`, `DESCRIPTION`, `pkg.lock`
- `Makefile`, `Dockerfile`, `docker-compose.yml`
- `.env.example`, `config.yml`, `config.json`

Record as `SUPPORT_FILES`.
