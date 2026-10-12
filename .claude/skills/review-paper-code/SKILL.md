---
name: review-paper-code
description: >-
  Reviews the code behind a research paper for reproducibility, data integrity, analytical correctness, and paper-code alignment, producing an impact-tiered markdown report with optional fixes. Use this skill whenever the user wants to check replication code, analysis scripts, or a replication package against a paper; asks whether their code matches or reproduces the paper's tables, figures, or numbers; wants a pre-submission or pre-archive audit of Stata, R, Python, Julia, MATLAB, SAS, notebook, or shell analysis code; or worries about data leakage, bad merges, missing seeds, hardcoded paths, or magic numbers in empirical research code, even if they don't name the skill. Not for general software or pull-request review (use code-review) or for reviewing the paper's statistics from the text alone (use statistical-reviewer).
argument-hint: "[path/to/main.tex] [path/to/code_dir] [main|full] [econ|polisci|ml|biostats|general] [review|diff|apply]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
  - AskUserQuestion
metadata:
  version: 1.1.0
  source: https://github.com/SolomonMg/research-agent-skills
---

# Review Paper Code

Review a research project's paper and code together for reproducibility, data integrity, analytical correctness, and paper-code alignment. The point is to catch the problems a replicator, referee, or data editor would find — before they do.

Be constructive, concrete, and calibrated. Research code often looks odd for legitimate reasons the reviewer can't see, so treat gaps as items to verify, not accusations, and cite file and line wherever possible so the author can act quickly.

## Scope and related skills

In scope: whether the code runs and reproduces, whether its data handling and analytics are sound, and whether it implements what the paper says.

Out of scope, and where to send it:
- Statistical methods as described in the paper text → `statistical-reviewer`
- Argument, framing, and contribution → `top3-reviewer`
- Prose quality → `writing-editor`; paragraph and section structure → `structural-editor`
- Citations → `bibliography-checker`; abstract accuracy → `abstract-checker`
- General software engineering or PR review is not what this skill is for.

## Reference files

- `references/discovery.md` — globs, directory names, and exclusion lists for finding the paper, code, outputs, and docs. Read in Phase 2 unless the user gave explicit paths for everything.
- `references/agents.md` — full prompts for the three review agents and the fixer agent. Read in Phase 4 (and Phase 6 for `diff`/`apply`).
- `references/report-template.md` — the report structure and triage hierarchy. Read in Phase 7.

## Phase 1: Parse arguments

Parse `$ARGUMENTS` left to right; tokens are case-insensitive.

**Review depth**

| Token | Meaning |
|---|---|
| `main` | Prioritize master scripts and core outputs (default) |
| `full` | Inspect every detected code file |

**Domain** — steers Agent B's domain-specific checks.

| Token | Analytical focus |
|---|---|
| `econ` | Economics / finance: IV, RDD, DID, panel FE, clustering, Stata conventions |
| `polisci` | Political science: survey experiments, observational causal inference, text-as-data |
| `ml` | Machine learning: train/test splits, leakage taxonomy, cross-validation, metric selection |
| `biostats` | Biostatistics / epidemiology: survival analysis, propensity scores, multiple testing, E-values |
| `general` | General social science (default) |

**Fix mode**

| Token | Meaning |
|---|---|
| *(none)* → `report` | Default. Write the report with recommended fixes; modify no code. |
| `review` | Interactive line by line: open VS Code at each fixable finding, show issue and proposed fix, apply only what the user approves. |
| `diff` | Apply all auto-fixable changes, then open VS Code to review. Git-tracked files: point the user to Source Control (Cmd+Shift+G) for per-hunk revert. Untracked files: make a `.code-review-backup` copy first and open `code -d backup file`. |
| `apply` | Apply all auto-fixable changes without opening VS Code (headless environments). |

The skill is read-only unless a fix mode is explicitly requested, because researchers often need to keep code byte-identical to what produced published results.

**Paths:** a token ending in `.tex`, `.qmd`, `.Rmd`, or `.md` is `PAPER_FILE`; a directory token is `CODE_DIR`.

Store `PAPER_FILE`, `CODE_DIR`, `REVIEW_DEPTH`, `DOMAIN`, `FIX_MODE`.

## Phase 2: Discover the project

Follow `references/discovery.md` to resolve, in order: `PAPER_FILE`, `CODE_DIR`, `CODE_FILES_ALL` / `CODE_FILES_REVIEWED` / `LANGUAGES` (respecting `REVIEW_DEPTH`; `main` caps the set at ~15 files), `OUTPUT_FILES`, and `SUPPORT_FILES`.

Continue if you found a paper and at least some code, even if discovery is imperfect — a partial review is more useful than none. Stop only if there is no main paper file or no relevant code; then tell the user what was missing and which paths they can pass explicitly.

Before moving on, tell the user: the paper file chosen, the code directory, code files detected vs. selected, languages, output artifacts (counts by type), depth and domain, and any ambiguity worth noting. This lets them correct a wrong guess before the expensive part starts.

## Phase 3: Read the paper

Read `PAPER_FILE` and everything it pulls in via `\input{}`, `\include{}`, `\subfile{}`, or Quarto `{{< include >}}`. Build `PAPER_SUMMARY`, going deeper than headline claims, because the agents need specifics to cross-check against code:

- **Metadata:** title, authors, abstract.
- **Research design:** research question; main data sources (name, time period, level of observation); sample restrictions and filters (stated N, exclusion criteria); main dependent variables (name and definition); main explanatory variables or treatments (name and definition); estimation methods (OLS, IV, DID, RDD, ML model, etc.); fixed effects and clustering; control variables if enumerated.
- **Quantitative claims (up to 20):** for each main table and figure referenced in the results, record its number and description, key coefficients or statistics cited in prose (magnitude, direction, significance), the stated sample size, and footnote caveats (sample restrictions, variable definitions, SE type).
- **Robustness and supplementary claims:** every explicit robustness claim ("robust to X"), appendix analyses referenced in the main text, subgroup analyses, and placebo or falsification tests.
- **Hardcoded numbers:** grep the paper source for numbers in prose that are not pulled in by `\input{}` of a table file. These were likely transcribed by hand from code output, so they are high-priority verification targets. Keep this list separately as `HARDCODED_NUMBERS` too.

## Phase 4: Launch the three review agents

Read `references/agents.md`. In a single message, launch Agents A, B, and C with the Agent tool (`subagent_type: "general-purpose"`) so they run in parallel. For each, pass the full prompt text with every placeholder filled — including complete file lists, `PAPER_SUMMARY`, and the resolved `DOMAIN` — since the subagents can't read the skill directory. All three are read-only.

| Agent | Focus | Store output as |
|---|---|---|
| A | Reproducibility and execution feasibility | `REPRODUCIBILITY_SUMMARY` |
| B | Data integrity and analytical logic | `ANALYSIS_SUMMARY` |
| C | Paper-to-code mapping and results verification | `MAPPING_SUMMARY` |

## Phase 5: Synthesize

Synthesize the three outputs yourself. Launch another agent only if the repo is unusually complex and a second pass is truly necessary.

1. **Cross-reference.** Merge overlapping findings — e.g., Agent A's missing seed plus Agent B's unseeded stochastic procedure become one finding. Where Agent C reports NOT FOUND but Agent A shows the script exists outside the review scope, say so.
2. **Resolve tensions.** If Agent B calls a method SOUND but Agent C shows the paper describes a different method, the discrepancy wins. If Agent A reports an execution FAIL while Agent C reports a HIGH design match, note that the design may be right but the code may not run.
3. **Assign impact tiers** to each unique finding:
   - **CRITICAL** — blocks reproducibility or may invalidate main claims: data integrity failures (Agent B CONCERN on merges, filters, or leakage affecting main results); execution blockers (Agent A FAIL); paper-code discrepancies on main specifications (Agent C Likely Discrepancies on core design); missing code for main tables or figures (Agent C NOT FOUND on key outputs).
   - **MAJOR** — likely to be raised in review: reproducibility gaps (Agent A VERIFY or MISSING on seeds, dependencies, run order); analytical concerns on secondary specifications (Agent B CONCERN not affecting main results); hardcoded numbers at risk; robustness checks claimed in the paper but missing from code; LOW-confidence matches on important elements (Agent C).
   - **MINOR** — improves quality: code style and structure (Agent A NOTE); documentation gaps (Agent A MISSING README details); minor analytical notes (Agent B VERIFY); robustness checks in code but not in the paper (Agent C).
4. **Compile:** `TOP_ACTIONS` (5–10 concrete next steps, ordered by tier then specificity), `MATCHED_ITEMS`, `VERIFY_ITEMS`, `DISCREPANCY_ITEMS`, and `OVERALL_ASSESSMENT` (3–5 sentences, leading with strengths).

## Phase 6: Apply fixes (skip in `report` mode)

In `report` mode, go straight to Phase 7.

Build a **fix plan** containing only findings where a concrete code change can be specified safely.

**Auto-fixable:**
- Hardcoded absolute paths → relative paths
- Missing random seeds → seed-setting calls before stochastic procedures
- Missing imports → import statements
- Missing output directories → `os.makedirs` / `dir.create` / `mkdir` guards
- Variable names inconsistent between paper and code → rename to match the paper
- Missing merge diagnostics → assertion or logging after the merge
- Missing dependency files → generate `requirements.txt` from imports, or `renv::init()`
- Missing or incomplete README sections → draft reproducibility documentation

**Recommend only** (these need the author's domain judgment and could change results):
- Statistical method changes (wrong test, wrong clustering level)
- Data-leakage restructuring (moving preprocessing after the split)
- Sample-restriction discrepancies between paper and code
- Missing robustness checks
- Analytical logic concerns (magic numbers, outlier treatment)

For each fixable item record: file path and line, exact current code, proposed replacement, reason, and severity tier. Order by severity (CRITICAL first), grouping edits to the same file together.

**`review` mode** — handle fixes yourself; don't launch the fixer agent. For each item:
1. Run `code -g FILE:LINE` via Bash to open VS Code at the location.
2. Show severity, file and line, current code, proposed fix, and reason.
3. Ask with AskUserQuestion: "Apply this fix? (yes / skip / stop)". **yes** → apply now with Edit; **skip** → next item; **stop** → skip all remaining.
4. Track applied vs. skipped.

**`diff` or `apply` mode** — launch a single fixer agent (`subagent_type: "general-purpose"`) using the Fixer Agent prompt in `references/agents.md`, filled with the fix plan and file list. It is the only agent that edits files, which keeps changes auditable.
- `diff`, git-tracked: afterwards run `code -g FILE:1` for each modified file and tell the user: "Open Source Control (Cmd+Shift+G) and click the changed file to see a side-by-side diff. Use the ↩ gutter buttons to revert any individual hunk."
- `diff`, not git-tracked: *before* launching the fixer, back up each file (`cp FILE FILE.code-review-backup`); afterwards run `code -d FILE.code-review-backup FILE` for each, and tell the user to delete the backups when satisfied.
- `apply`: no VS Code interaction; just summarize the changes.

Record applied, skipped, and failed fixes as `FIX_RESULTS`.

## Phase 7: Write the report

Read `references/report-template.md` and write the report to the current working directory as `code_review_report_[YYYY-MM-DD].md` (today's date). Include the Fixes Applied section only when a fix mode ran, and append the raw agent outputs and `PAPER_SUMMARY` in the appendix so the user can audit the synthesis.

## Phase 8: Tell the user

Report:
- That the code review is complete, and the path to the saved report
- The Overall Assessment (3–5 sentences)
- If fixes ran: how many were applied, skipped, and failed
- The top 5 remaining priority actions (excluding anything already fixed)
- Counts of CRITICAL, MAJOR, and MINOR items, and how many were auto-fixed
- Coverage caveats (files not reviewed, languages not fully covered, etc.)
- In `diff` mode: a reminder to review the changes in VS Code Source Control
