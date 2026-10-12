---
name: statistical-reviewer
description: >-
  Multi-agent statistical review of an academic paper or manuscript: test selection and assumptions, power and multiple comparisons, effect sizes and statcheck-style p-value consistency, selective reporting, causal identification and causal-language overreach, plus an optional critique from a named statistician or school (Gelman, Pearl, Rubin, Imbens, Ioannidis, Bayesian, frequentist, replication-crisis, and more). Use this skill whenever the user asks to check the stats, methods, regressions, p-values, effect sizes, robustness, identification strategy, or causal claims in a paper draft (.tex, .qmd, .Rmd, .md), wants a methods-focused referee report, or asks how a particular statistician or journal reviewer would react, even if they don't name the skill. Not for argument and framing review (use top3-reviewer), auditing the analysis code itself (use review-paper-code), or prose editing (use writing-editor).
argument-hint: "[path/to/paper] [perspective|none] [journal] [review|diff|apply]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
metadata:
  version: 1.1.0
  source: https://github.com/SolomonMg/research-agent-skills
---

# Statistical Reviewer

Coordinate a multi-agent statistical review of an academic paper. Three core agents examine statistical methods, reporting quality, and causal inference in parallel; a fourth optionally critiques the paper through a named statistical tradition. The agents are read-only. You consolidate their findings into one report and, if asked, apply language-level fixes.

Splitting the review this way matters because each lens catches different failures: a paper can use the right test but misreport it, or report impeccably while making causal claims the design cannot support. The perspective agent adds the pointed, tradition-specific objection a real referee would raise, which generic checklists miss.

## Scope and related skills

This skill evaluates the statistics as described in the manuscript. It does not judge the argument or contribution, audit code line by line, or copy-edit prose. Point the user elsewhere for those:

- Argument architecture, framing, contribution → `top3-reviewer`
- Research code reproducibility and paper-code alignment → `review-paper-code`
- Abstract claims vs. body → `abstract-checker`
- Citations and bibliography → `bibliography-checker`
- Prose clarity → `writing-editor`; paragraph/section structure → `structural-editor`

## Reference files

- `references/perspectives.md` — perspective tokens (statisticians, schools, institutions) and recognized journals. Read during Phase 1 to parse arguments, and use it to fill the perspective description for Agent 4.
- `references/agents.md` — full prompts for Agents 1–4 and the fixer agent, with a placeholder table. Read before Phase 3.
- `references/report-template.md` — the report structure and statistical checklist. Read before Phase 5.

## Phase 1: Parse arguments

Scan the tokens of `$ARGUMENTS` left to right (all matching is case-insensitive):

1. A perspective token (statistician, school, or institution from `references/perspectives.md`) → `PERSPECTIVE`. The tokens `none` or `skip` disable the perspective agent.
2. A journal token from `references/perspectives.md` → `TARGET_JOURNAL`.
3. A fix-mode token (`review`, `diff`, `apply`) → `FIX_MODE`.
4. Remaining text → the file path.

Defaults: `PERSPECTIVE = gelman`, `TARGET_JOURNAL = top-field` (a leading field journal), `FIX_MODE = report`. If `$ARGUMENTS` is empty, use all defaults and auto-detect the paper.

### Fix modes

| Mode | Behavior |
|---|---|
| `report` (default) | Read-only. No files are modified; only the report is written. |
| `review` | Interactive line-by-line. For each fixable finding, open VS Code at the location (`code -g file:line`), show the issue and proposed fix, and ask the user to approve or skip. Only approved fixes are applied. |
| `diff` | Apply all auto-fixable changes, then open VS Code for review. If git-tracked, tell the user to use Source Control (Cmd+Shift+G) for per-hunk revert. If not, create a `.stat-review-backup` copy first and open `code -d backup file`. |
| `apply` | Apply all auto-fixable changes without opening VS Code — for headless or non-VS-Code environments. |

### Examples

```
/statistical-reviewer path/to/paper.tex                     # default Gelman perspective, no journal
/statistical-reviewer pearl APSR path/to/paper.tex          # Pearl's causal lens, targeting APSR
/statistical-reviewer replication Science path/to/paper.tex # replication-crisis school, Science
/statistical-reviewer stanford path/to/paper.tex            # Imbens/Athey perspective
/statistical-reviewer none path/to/paper.tex                # skip the perspective agent
/statistical-reviewer bayesian JASA path/to/paper.tex       # Bayesian school, stats journal
```

## Phase 2: Discover the paper

If a file path was given, use it. Otherwise auto-detect:

1. Glob `**/*.tex`, `**/*.qmd`, `**/*.Rmd`, `**/*.md` for candidates.
2. Identify the main document: the file containing `\documentclass`, `\begin{document}`, or YAML frontmatter with `title:`.
3. Follow `\input{}`, `\include{}`, and `\subfile{}` references to build the complete file list, and read every component.
4. Glob for data/results files (`**/*.csv`, `**/*.rds`, `**/*.json` in data directories).
5. Glob for analysis code (`**/*.R`, `**/*.py`, `**/*.do`, `**/*.sas`). Agents use these to check whether the paper's description matches what was actually run.

Record the full path and role of each file; the paper title, authors, and abstract; the statistical methods mentioned (regression, t-test, ANOVA, Bayesian, etc.); and the software mentioned (R, Stata, Python, Stan, etc.).

## Phase 3: Launch review agents in parallel

Read `references/agents.md`, fill its placeholders (file list, paper metadata, target journal, and — for Agent 4 — the perspective name and full description row), and launch the agents in a single message with the Agent tool (`subagent_type: "general-purpose"`) so they run concurrently. Pass each agent its complete prompt text; subagents cannot see this skill's directory.

- Always launch Agents 1–3 (Methods & Assumptions; Effect Sizes & Reporting Quality; Causal Inference & Research Design).
- Launch Agent 4 (Perspective Reviewer) unless `PERSPECTIVE` is none.

## Phase 4: Fix-mode gate

Skip this phase if `FIX_MODE` is `report`; go straight to Phase 5.

Build a fix plan from the agent findings, including only items where a concrete text change can be specified. Statistical substance (methods, analyses, design) cannot be fixed by editing prose, so those items stay as recommendations.

**Auto-fixable:**
- Overclaimed causal language: "X causes Y" → "X is associated with Y" (when the design is correlational)
- Informal significance language: "significant effect" → "statistically significant" or "large", as appropriate
- Missing hedging: unqualified assertions → add "suggestive," "consistent with," or appropriate caveats
- Notation inconsistencies: the same quantity written differently across sections → standardize
- Numerical inconsistencies: text says "p < 0.01" but the table shows "p = 0.03" → fix the text to match the table
- Missing reporting elements: insert placeholders such as "[EFFECT SIZE NEEDED]" for missing effect sizes, CIs, or sample sizes
- P-value / test-statistic formatting: inconsistent decimals, missing degrees of freedom → standardize

**Recommend only (not auto-fixable):**
- Changing the statistical method (wrong test, wrong model specification)
- Adding power or sensitivity analyses (requires computation)
- Restructuring the causal identification strategy
- Adding missing robustness checks
- Changing the research design or data collection approach

For each fixable item record: file path, line number, current text, proposed replacement, reason, and severity. Order by severity (CRITICAL first), then group by file.

### `review` mode

For each item in the fix plan:

1. Run `code -g FILE:LINE` via Bash to open VS Code at the location.
2. Show severity, file and line, current text, proposed fix, and reason.
3. Ask with AskUserQuestion: "Apply this fix? (yes / skip / stop)". On **yes**, apply immediately with Edit; on **skip**, move on; on **stop**, end and skip the rest.
4. Track applied vs. skipped.

### `diff` and `apply` modes

If `FIX_MODE` is `diff` and the files are not git-tracked, create backups (`cp FILE FILE.stat-review-backup`) before any edits so the user has something to diff against.

Launch a single fixer agent (`subagent_type: "general-purpose"`) with the Fixer Agent prompt from `references/agents.md`, filled with the fix plan. Using one agent for all edits avoids conflicting concurrent writes.

After it returns:
- `diff`, git-tracked: run `code -g FILE:1` for each modified file and tell the user to use Source Control for per-hunk revert.
- `diff`, not git-tracked: run `code -d FILE.stat-review-backup FILE` for each modified file.
- `apply`: report the change summary only.

Record results as `FIX_RESULTS`.

## Phase 5: Consolidate and save

After all agents return (and fixes are applied, if any), read `references/report-template.md` and write the consolidated report to `STATISTICAL_REVIEW_[YYYY-MM-DD].md` in the current working directory. Rank priority action items with the template's triage hierarchy: causal identification failures outrank numerical inconsistencies, which outrank methods/assumption violations, which outrank perspective-specific concerns — because an unidentified causal claim undermines the paper regardless of how well everything else is done.

## Phase 6: Report to the user

Tell the user:

1. The path to the saved report
2. The statistical rigor assessment
3. If fixes were applied: how many were applied, skipped, and failed
4. The top 5 remaining priority action items (excluding items already fixed)
5. The perspective reviewer's primary objection (if Agent 4 ran)
6. Counts of issues by severity across all agents
7. If `FIX_MODE` is `diff`: a reminder to review changes in VS Code Source Control

## Sources

This skill synthesizes:
- Statcheck methodology for APA statistical reporting verification
- CONSORT, STROBE, and PRISMA reporting guidelines
- Gelman & Hill, *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- Angrist & Pischke, *Mostly Harmless Econometrics* (design-based identification)
- Pearl, *Causality* (structural causal models and DAGs)
- Imbens & Rubin, *Causal Inference for Statistics, Social, and Biomedical Sciences*
- Greenland, "Invited commentary: The need for cognitive science in methodology" (bias analysis)
- Ioannidis, "Why most published research findings are false" (replication and power)
- Simmons, Nelson & Simonsohn, "False-positive psychology" (p-hacking and researcher degrees of freedom)
- K-Dense-AI/claude-scientific-skills statistical analysis framework
- Imbad0202/academic-research-skills multi-agent peer review architecture
