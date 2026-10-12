---
name: top3-reviewer
description: >-
  Referee-style review of an academic paper's logic, coherence, and contribution, held to the standard of a senior scientist who publishes regularly in Science, Nature, and PNAS. Use this skill whenever the user wants their manuscript reviewed like a top-journal referee would, asks whether the argument holds together or the contribution is clear and important enough, wants someone to poke holes in the paper or play devil's advocate, asks what Reviewer 2 will say, or wants a pre-submission check against a named journal such as Science, Nature, PNAS, AER, APSR, or NeurIPS, even if they don't name the skill. Not for statistical methods (use statistical-reviewer), line-level prose (use writing-editor), paragraph and section structure (use structural-editor), citations (use bibliography-checker), or research code (use review-paper-code).
argument-hint: "[path/to/paper] [journal, e.g. Science|Nature|PNAS|AER|APSR] [review|diff|apply]"
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

# Top-3 Reviewer

Coordinate a 3-agent review of an academic paper focused on **logic, coherence, and contribution**. Adopt the persona of a senior scientist who regularly publishes in Science, Nature, and PNAS: someone with very high standards for whether an argument holds together, whether the contribution is clear and important, and whether a broad scientific audience can follow the reasoning.

The review splits into three independent lenses because each catches failures the others miss: a logician checks that claims follow from evidence, an editor checks whether the paper matters and is framed to show it, and a devil's advocate builds the strongest case for rejection so the authors hear it before Reviewer 2 does.

## Scope and related skills

This skill evaluates argument and contribution only. Point the user elsewhere for:

- Statistical methods, effect sizes, causal identification → `statistical-reviewer`
- Sentence-level clarity, style, voice → `writing-editor`
- Paragraph and section structure → `structural-editor`
- Abstract-vs-body consistency → `abstract-checker`
- Citation accuracy and coverage → `bibliography-checker`
- Research code and replication → `review-paper-code`

Table/figure documentation, LaTeX formatting, and math notation are out of scope for all of these.

## Reference files

- `references/agents.md` — full prompts for the three review agents and the fixer agent. Read it in Phase 3 (and again in Phase 4 for `diff`/`apply`).
- `references/report-template.md` — the report structure. Read it in Phase 5.

---

## Phase 1: Parse arguments

Scan the tokens of `$ARGUMENTS` left to right (matching is case-insensitive):

1. A token matching a journal name → `TARGET_JOURNAL`.
2. A token matching a fix mode → `FIX_MODE`.
3. Remaining text → the file path.

Defaults: `TARGET_JOURNAL = Science` (broad audience, highest bar for clarity and significance) and `FIX_MODE = report`. If `$ARGUMENTS` is empty, use both defaults and auto-detect the paper.

**Recognized journals** (users may name others; treat any recognizable journal as the target):

- Generalist: `Science`, `Nature`, `PNAS`, `NatureHB` (Nature Human Behaviour), `SciAdv` (Science Advances), `NComms` (Nature Communications)
- Top-5 economics: `AER`, `QJE`, `JPE`, `Econometrica`, `REStud`
- Finance: `JF`, `JFE`, `RFS`, `JFQA`
- Political science: `APSR`, `AJPS`, `JOP`
- Psychology: `PsychScience`, `JPSP`, `PsychMethods`
- Sociology: `ASR`, `AJS`
- Computer science: `ICML`, `NeurIPS`, `ICWSM`

**Fix modes:**

| Mode | Behavior |
|---|---|
| `report` (default) | Read-only. No paper files are modified; only the review report is written. |
| `review` | Interactive line-by-line. For each fixable finding, open VS Code at the location (`code -g file:line`), show the issue and proposed fix, and ask the user to approve or skip. Only approved fixes are applied. |
| `diff` | Apply all auto-fixable changes, then open VS Code for review. If git-tracked, the user reverts per-hunk via Source Control (Cmd+Shift+G); otherwise create a `.review-backup` copy first and open `code -d backup file`. |
| `apply` | Apply all auto-fixable changes without opening VS Code (headless or non-VS-Code environments). |

## Phase 2: Discover the paper

If a file path was given, use it. Otherwise auto-detect:

1. Glob for `**/*.tex`, `**/*.qmd`, `**/*.Rmd`, `**/*.md`, `**/*.pdf`.
2. Identify the main document: the file containing `\documentclass`, `\begin{document}`, or YAML frontmatter with `title:`.
3. Read the main file and follow `\input{}`, `\include{}`, and `\subfile{}` references to build the complete file list.
4. Read all component files.

Record:
- Full path and role of each file (this becomes `FILE_LIST`)
- Title, authors, abstract
- Stated contribution (usually at the end of the introduction)
- Number of main findings/results
- Discipline and topic area

## Phase 3: Launch the three review agents in parallel

Read `references/agents.md`. For each of Agent 1 (Argument Architecture), Agent 2 (Contribution & Framing), and Agent 3 (Devil's Advocate):

1. Copy the agent's prompt text.
2. Replace `[TARGET_JOURNAL]` and `[FILE_LIST]` with the values from Phases 1–2.
3. Pass the full prompt as the `prompt` of an Agent call with `subagent_type: "general-purpose"`.

Send all three Agent calls in a single message so they run concurrently. Pass the complete prompt text, because subagents cannot see this skill's directory. Each agent reads the paper files independently and is read-only — keeping review and editing separate prevents conflicting edits and keeps the critique honest.

## Phase 4: Apply fixes (skip when `FIX_MODE` is `report`)

### Build the fix plan

From the agent findings, include only items where a concrete text change can be specified. Substantive problems need the author's judgment and new work, so they stay as recommendations.

**Auto-fixable:**
- Weak or buried topic sentences → rewrite the paragraph's first sentence to state the point directly
- Vague framing in abstract/introduction → sharpen "this paper studies X" into a specific claim
- Overclaimed contribution → "first to show" becomes "among the first" or "provides new evidence"
- Unwarranted generalizations → "this proves" becomes "this suggests" or "this is consistent with"
- Missing transitions between sections → add a bridging sentence
- Unclear antecedents → make an ambiguous "This shows that..." referent explicit
- Redundant or circular sentences → cut or condense

**Recommend only (not auto-fixable):**
- Restructuring the argument architecture (reordering or adding sections)
- Strengthening a weak warrant (requires new evidence or reasoning)
- Addressing the devil's advocate objections (requires substantive revision)
- Changing the framing or positioning of the contribution
- Adding missing evidence or analyses

For each fixable item, record file path, line number, current text, proposed replacement, reason, and severity. Order by severity (CRITICAL first), then group by file.

### `review` mode — interactive

For each item in the fix plan:
1. Run `code -g FILE:LINE` via Bash to open VS Code at the location.
2. Show severity, file and line, current text, proposed fix, and reason.
3. Ask with AskUserQuestion: "Apply this fix? (yes / skip / stop)"
   - **yes** → apply immediately with Edit
   - **skip** → move to the next item
   - **stop** → end and skip the rest
4. Track applied vs. skipped.

### `diff` or `apply` mode — fixer agent

1. If `FIX_MODE` is `diff` and the files are not git-tracked, copy each file to be modified to `FILE.review-backup` before any edits.
2. Launch a single fixer agent using the Fixer Agent prompt from `references/agents.md`, with `[FIX_PLAN]` filled in. It is the only agent with edit permissions, so every change traces back to the vetted plan.
3. After it returns:
   - `diff`, git-tracked: run `code -g FILE:1` for each modified file and tell the user to use Source Control (Cmd+Shift+G) for per-hunk revert.
   - `diff`, not git-tracked: run `code -d FILE.review-backup FILE` for each modified file.
   - `apply`: summarize the changes only.

Record the outcome (applied / skipped / failed per item) as `FIX_RESULTS`.

## Phase 5: Consolidate and save the report

Once all three agents have returned (and fixes are done, if any), read `references/report-template.md` and write the consolidated report to the current working directory as `ACADEMIC_REVIEW_[YYYY-MM-DD].md` using today's date.

When consolidating:
- Write the executive summary and verdict yourself, drawing on all three agents.
- Triage priority items in this order, since earlier categories undermine the paper most: logical fallacies and non sequiturs > missing warrants in major claims > contribution/framing problems > devil's advocate objections > section coherence > audience calibration.
- Deduplicate the agents' questions into at most 10, ordered by severity.
- Include the "Fixes Applied" section only when `FIX_MODE` is not `report`.

## Phase 6: Report to the user

Tell the user:
1. The path to the saved report
2. The verdict and contribution rating
3. If fixes were applied: how many were applied, skipped, and failed
4. The devil's advocate's reject summary, verbatim
5. The elevator pitch sentence
6. The top 5 remaining priority action items (excluding items already fixed)
7. If `FIX_MODE` is `diff`: a reminder to review changes in VS Code Source Control

---

## Examples

```
# Review against Science standards (default), read-only
/top3-reviewer path/to/paper.tex

# Review against Nature standards
/top3-reviewer Nature path/to/paper.tex

# Political science audience, interactive fixes
/top3-reviewer APSR path/to/paper.tex review

# Psychology journal, apply clarity fixes and open a diff
/top3-reviewer PsychScience path/to/paper.tex diff
```

## Sources

This skill synthesizes:
- Davis, M.S. (1971). "That's Interesting!" — framework for evaluating theoretical contribution
- Toulmin, S. (1958). *The Uses of Argument* — claim/data/warrant/backing/qualifier/rebuttal model
- Glasman-Deal, H. *Science Research Writing* — gap-fill-implication arc
- Bem, D.J. (2003). "Writing the Empirical Journal Article" — hourglass structure
- Sword, H. (2012). *Stylish Academic Writing* — storyline and coherence
- Leung, K. (2011). AMJ editorial on gap-spotting vs. problematization
- Colquitt & George (2011). AMJ editorial on incremental vs. revelatory contribution
- Science/Nature/PNAS reviewer guidelines (significance, rigor, accessibility)
- Imbad0202/academic-research-skills — Devil's Advocate agent pattern
- EvoScientist/EvoSkills — "force a reject summary first" protocol
- sundial-org/skills (icml-reviewer) — dimensional evaluation structure
- Backman/AI-research-feedback — multi-agent triage and consolidation patterns
