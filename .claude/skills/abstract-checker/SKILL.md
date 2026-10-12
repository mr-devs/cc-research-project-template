---
name: abstract-checker
description: >-
  Checks an academic paper's abstract in both directions: every abstract claim
  is verified against the manuscript body (numbers, direction, strength,
  scope, novelty), and the body's most important findings are checked for
  coverage and emphasis in the abstract; can also rewrite the abstract. Use
  this skill whenever the user wants to check, audit, verify, tighten, or
  rewrite an abstract, asks whether the abstract matches the results or
  overclaims, wants to make sure the key findings are in the abstract, or is
  preparing a manuscript (.tex, .qmd, .Rmd) for submission, even if they
  don't name the skill. Not for whole-paper argument review (use
  top3-reviewer) or sentence-level prose editing (use writing-editor).
argument-hint: "[path/to/paper.tex] [review|diff|apply]"
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

# Abstract Checker

Verify an academic paper's abstract in two directions:

1. **Abstract → body.** Does every claim in the abstract have support in the manuscript, with matching numbers, direction, strength, and scope?
2. **Body → abstract.** Does the abstract highlight the manuscript's most important findings, with emphasis proportional to their importance?

Both directions matter because the abstract is often the only part of a paper people read. An abstract that overclaims misleads readers; one that buries the main result undersells the work. Checking only one direction misses half the problems.

Be concrete and cite specific locations (file, line, section, table). Treat gaps as items to verify rather than accusations — a "missing" result may sit in an appendix the agents didn't read.

## Scope and related skills

This skill covers the abstract only: its fidelity to the body and its coverage of the key findings. For other concerns, point the user to:

- **top3-reviewer** — argument logic, contribution, and framing of the whole paper
- **statistical-reviewer** — whether the statistical methods support the results in the first place
- **writing-editor** — sentence-level clarity and prose style
- **structural-editor** — paragraph and section organization
- **bibliography-checker** — citations and references
- **review-paper-code** — whether code reproduces the reported numbers

## Reference files

- `references/agents.md` — full prompts for the two analysis agents. Read it in Phase 3 before launching them.
- `references/report-template.md` — the report structure. Read it in Phase 6 before writing the report.

## Phase 1: Parse arguments

Parse `$ARGUMENTS` left to right:

1. A token matching a fix mode (`review`, `diff`, `apply`) sets `FIX_MODE`.
2. Remaining text is the file path.
3. If no fix mode is given, set `FIX_MODE` to `report`.
4. If `$ARGUMENTS` is empty, auto-detect the paper and use `report`.

| Mode | Behavior |
|---|---|
| `report` (default) | Read-only. No files are modified; the report includes a recommended revised abstract. |
| `review` | Interactive, sentence by sentence. For each proposed change, open VS Code at the location (`code -g file:line`), show the current and proposed text, and ask the user to approve or skip. Only approved edits are applied. |
| `diff` | Rewrite the abstract with all recommended changes, then open VS Code for review. If git-tracked, the user reviews via Source Control (Cmd+Shift+G) with per-hunk revert. If not, create a `.abstract-backup` copy and open `code -d backup file`. |
| `apply` | Rewrite the abstract with all recommended changes without opening VS Code — for headless or non-VS-Code environments. |

Read-only is the default because the abstract is the most carefully worded paragraph in a paper; the author should opt in to edits.

## Phase 2: Discover and read the paper

### Find the paper

If a file path was provided, use it. Otherwise auto-detect:

1. Glob for `**/*.tex`, `**/*.qmd`, `**/*.Rmd`, excluding `_minted-*`, `build/`, `output/`, `.git/`, `node_modules/`, `__pycache__/`, `.quarto/`, `_site/`.
2. Identify the main document: a `.tex` file containing `\documentclass` or `\begin{document}`, or a `.qmd`/`.Rmd` with YAML frontmatter containing `title:`.
3. If there are several candidates, prefer one in `Writing/`, `Paper/`, `Draft/`, or the root; then the one with the most `\input{}`/`\include{}` references.

Record it as `PAPER_FILE`. Read it and every file it pulls in via `\input{}`, `\include{}`, `\subfile{}`, or Quarto `{{< include >}}`. Record all paths as `PAPER_FILES`.

### Extract the abstract

Look for `\begin{abstract}...\end{abstract}`, `\abstract{...}`, a YAML `abstract:` field, or a section titled "Abstract" near the top. Extract it verbatim as `ABSTRACT_TEXT` and record its file and line range as `ABSTRACT_LOCATION`.

If no abstract is found, use AskUserQuestion to ask where it is or whether the user wants to paste it.

### Build the inventories

**`ABSTRACT_CLAIMS`** (ordered list). Split the abstract into claim-bearing sentences. For each, record:
- the sentence, verbatim
- the claim type: empirical finding, methodological claim, data description, scope/framing, contribution/novelty, or implication/policy
- any specific numbers, statistics, or magnitudes
- the direction of the effect (positive / negative / null / comparative), if any

**`BODY_FINDINGS`** (ranked list). From the results, discussion, and conclusion, extract each distinct empirical finding with:
- its location (section, paragraph, table/figure)
- supporting evidence (coefficient, p-value, CI, effect size, descriptive statistic)
- the author's emphasis signals (see below)
- whether it is presented as a main result or a robustness/supplementary check

Rank findings by importance using the author's own signals, since the abstract should reflect what the authors themselves treat as central:

| Signal | Importance |
|---|---|
| Mentioned in both results and conclusion | High |
| Has its own subsection or extended discussion | High |
| Appears in the first or most prominent table/figure | High |
| Described as "main," "key," "central," "primary," or "important" | High |
| Mentioned briefly without elaboration | Medium |
| Appears only in robustness checks or the appendix | Low |

**`PAPER_METADATA`**: title, authors, number of tables and figures, main estimation method, main data source and sample.

Before continuing, tell the user: the paper file found, the abstract location (file and lines), the number of claim-bearing sentences, the number of body findings extracted, and the fix mode.

## Phase 3: Launch the two agents in parallel

Read `references/agents.md`. Fill in its placeholders (`{ABSTRACT_TEXT}`, `{ABSTRACT_CLAIMS}`, `{BODY_FINDINGS}`, `{PAPER_FILES}`, `{PAPER_METADATA}`) and pass the full prompt text for each agent to its own Agent call with `subagent_type: "general-purpose"`. Send both calls in a single message so they run in parallel. The subagents can't see the skill directory, so the prompt you send has to contain everything they need.

| Agent | Direction | Store output as |
|---|---|---|
| A — Abstract → Body Verification | Each abstract claim checked against the body | `VERIFICATION_SUMMARY` |
| B — Body → Abstract Coverage | Each key finding checked for presence and weight in the abstract | `COVERAGE_SUMMARY` |

Both agents are read-only.

## Phase 4: Synthesize

After both agents return, synthesize the results yourself.

1. **Cross-reference.** If Agent A marks a claim NOT FOUND and Agent B finds no corresponding finding in the body, merge them into a single "unsupported claim" item. If Agent A marks a claim OVERSTATED and Agent B flags emphasis misalignment on the same finding, combine them. The user should see one issue per underlying problem, not two.

2. **Assign each abstract sentence a disposition:**
   - **Keep as-is** — SUPPORTED (Agent A) and given adequate weight (Agent B)
   - **Revise** — PARTIALLY SUPPORTED, OVERSTATED, UNDERSTATED, or NUMERICALLY INCONSISTENT
   - **Cut** — Agent B marks it unnecessary or low-priority
   - **Add** — Agent B identifies a missing essential finding; draft a new sentence

3. **Draft the revised abstract** (`REVISED_ABSTRACT`). Do this in every mode: in `report` mode it becomes the "Recommended Abstract" in the report; in the other modes it is what gets applied. The revision should:
   - fix every numerical mismatch
   - recalibrate overstated and understated claims
   - add sentences for essential missing findings
   - cut or shorten unnecessary content
   - preserve the author's voice and style
   - keep a venue-appropriate length
   - follow a logical flow: context → gap → approach → findings → implications

4. **Compile findings:**
   - `OVERALL_ASSESSMENT` — 3–5 sentences on abstract quality
   - `CRITICAL_ISSUES` — unsupported claims, numerical mismatches, missing essential findings (the abstract misrepresents the paper)
   - `MAJOR_ISSUES` — overstated claims, emphasis misalignment, structural problems
   - `MINOR_ISSUES` — minor wording, unnecessary detail, understatement

## Phase 5: Apply fixes (skip in `report` mode)

In `report` mode, skip to Phase 6 — nothing is modified.

### `review` mode — interactive, sentence by sentence

For each sentence with a disposition of **Revise**, **Cut**, or **Add**:

1. Run `code -g ABSTRACT_FILE:LINE` via Bash to open VS Code at the sentence.
2. Show the disposition, the current sentence, the proposed replacement or deletion, the reason (which agent findings support it), and the severity. For **Add**, show the proposed sentence and where it would go in the abstract.
3. Ask with AskUserQuestion: "Apply this change? (yes / skip / stop)"
   - **yes** — apply it immediately with Edit
   - **skip** — move to the next item
   - **stop** — end and skip the rest
4. Track which changes were applied and which were skipped.

### `diff` and `apply` modes

Replace the entire abstract in the source file with `REVISED_ABSTRACT` using Edit.

- **`diff`, git-tracked:** run `code -g ABSTRACT_FILE:ABSTRACT_LINE` and tell the user: "Open Source Control (Cmd+Shift+G) and click the file to see the abstract diff. Use the revert buttons to reject any changes."
- **`diff`, not git-tracked:** first back up the file (`cp FILE FILE.abstract-backup`), apply the revision, then run `code -d FILE.abstract-backup FILE`. The backup is the user's only way to recover the original wording without version control, so create it before editing.
- **`apply`:** apply the revision and summarize the changes.

Record what happened as `FIX_RESULTS`.

## Phase 6: Write the report

Read `references/report-template.md` and write the report to the current working directory as `abstract_check_[YYYY-MM-DD].md` (today's date). Include the conditional sections that match `FIX_MODE` as described in the template, and paste both agent outputs into the appendix.

## Phase 7: Tell the user

After writing the report, tell the user:

- that the abstract check is complete, and the path to the report
- the overall assessment (3–5 sentences)
- the claim verification summary (N of M supported, etc.)
- the coverage summary (N of M top findings covered, N essential missing)
- if fixes were applied: how many were applied and skipped
- the top 3 priority action items
- in `report` mode: that a recommended revised abstract is in the report
- in `diff` mode: a reminder to review the changes in VS Code Source Control (or the diff view if not git-tracked)
