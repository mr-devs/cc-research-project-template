---
name: structural-editor
description: >-
  Structural editor for academic manuscripts, grant proposals, theses, and technical reports that diagnoses and fixes paragraph-level structure (lead sentences, paragraph unity, given-new flow, transitions) and document architecture (paragraph ordering, heading hierarchy, section handoffs, narrative arc, misplaced content), producing a prioritized restructuring plan. Use this skill whenever the user says a draft feels disorganized, doesn't flow, buries the point, has weak topic sentences, needs reorganizing or a reverse outline, or asks to restructure a paper, chapter, or section, even if they don't name the skill. Not for sentence-level prose polish or AI-tell cleanup (use writing-editor), argument and contribution critique (use top3-reviewer), or citation checks (use bibliography-checker).
argument-hint: "[path/to/file] [academic|grant|thesis|technical|general] [review|diff|apply]"
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

# Structural Editor

Coordinate a two-agent structural edit of a manuscript. One analyst examines paragraph-level structure; the other examines section and document architecture. You merge their findings into a single prioritized restructuring plan and, if the user asked for a fix mode, apply the safe subset of fixes.

Why two agents: paragraph-level problems (a buried lead, a broken given-new chain) and document-level problems (results leaking into the discussion, a reverse outline with gaps) need different reading strategies — one close, one zoomed out. Running them in parallel and reconciling afterward catches both without either drowning the other.

## Scope and related skills

This skill restructures; it does not copy-edit. Grammar, spelling, word choice, and sentence-level clarity are out of scope, as is citation formatting. Point the user elsewhere for those:

- **writing-editor** — line-level prose quality, clarity, voice
- **top3-reviewer** — whether the argument and contribution hold up
- **bibliography-checker** — citation accuracy and coverage
- **abstract-checker** — whether the abstract matches the body

## Reference files

- `references/agents.md` — full prompts for Agent A (paragraph level), Agent B (document level), and the fixer agent. Read it in Phase 2, and again in Phase 4 if a fixer is needed.
- `references/report-template.md` — the restructuring-plan format (Phase 3) and the final report template (Phase 5).

## Phase 1: Parse arguments and discover the text

Scan `$ARGUMENTS` left to right (case-insensitive):

| Token | Sets | Meaning |
|---|---|---|
| `academic` (default) | `WRITING_CONTEXT` | Research papers, journal articles, dissertations |
| `grant` | `WRITING_CONTEXT` | Grant proposals, funding applications |
| `thesis` | `WRITING_CONTEXT` | Dissertations, book-length manuscripts |
| `technical` | `WRITING_CONTEXT` | Documentation, technical reports |
| `general` | `WRITING_CONTEXT` | Anything else |
| `review` | `FIX_MODE` | Interactive: open each fix in VS Code (`code -g file:line`), show the issue and proposed change, and ask the user to approve or skip |
| `diff` | `FIX_MODE` | Apply all auto-fixable changes, then open VS Code for review (Source Control if git-tracked; otherwise a backup diff) |
| `apply` | `FIX_MODE` | Apply all auto-fixable changes without opening VS Code (headless) |

Any remaining text is the file path. Defaults: `WRITING_CONTEXT = academic`, `FIX_MODE = report`. Report mode is read-only — no files are modified except the saved report.

If no file path was given, auto-detect the document:

1. Glob for `**/*.tex`, `**/*.qmd`, `**/*.Rmd`, `**/*.md`.
2. The main document is the file containing `\documentclass`, `\begin{document}`, or YAML frontmatter with `title:`.
3. Read it and follow `\input{}`, `\include{}`, and `\subfile{}` references to build the complete file list.
4. Read all component files.

If several candidates remain plausible, ask the user which one to use rather than guessing.

Record: full file path(s), writing context, approximate word count, section boundaries (`\section{}`, `##`, etc.), and paragraphs per section.

### Context adaptation table

Each agent gets the row matching `WRITING_CONTEXT`, because structural norms differ by genre — a 9-sentence paragraph is fine in a thesis but too long in a grant.

| Context | Expected structure | Paragraph norms | Heading expectations |
|---|---|---|---|
| academic | IMRAD or discipline-specific sections | 3–8 sentences; one idea per paragraph; lead sentence states the point | Informative headings that form a readable outline |
| grant | Significance → Innovation → Approach → Timeline | Short paragraphs (2–5 sentences); emphasis on "why this matters" early | Agency-prescribed headings; parallel structure |
| thesis | Chapters with subsections; literature review chapter | Longer paragraphs acceptable; topic sentences critical | Numbered hierarchy; consistent depth |
| technical | Problem → Approach → Implementation → Evaluation | Short paragraphs; one concept each; frequent subheadings | Descriptive headings; consistent granularity |
| general | Flexible | Varies | Flexible |

## Phase 2: Launch the two analyst agents in parallel

Read `references/agents.md`. Fill in `{{FILES}}`, `{{WRITING_CONTEXT}}`, and `{{CONTEXT_ROW}}` for Agent A and Agent B, then launch both with the Agent tool (`subagent_type: "general-purpose"`) in a single message so they run concurrently. Pass the complete filled-in prompt text — the subagents cannot see this skill directory.

Both agents are read-only. Keeping analysis and editing separate avoids conflicting edits and lets you reconcile their findings before anything touches the file.

- **Agent A — Paragraph-Level Structure**: lead sentence audit, paragraph unity, given-new flow, paragraph-to-paragraph transitions, length and density.
- **Agent B — Section & Document Architecture**: heading hierarchy, reverse outline, paragraph ordering within sections, section handoffs, narrative arc, information placement.

## Phase 3: Build the restructuring plan

When both agents return, consolidate their findings:

1. **Deduplicate.** If Agent A flags a transition problem and Agent B flags the same location as an ordering issue, merge them and keep the finding with the more specific fix.
2. **Resolve conflicts.** If Agent A says "split paragraph 5" and Agent B says "move paragraph 5 before paragraph 3," work out the right sequence — split first, then move the relevant piece.
3. **Classify by impact tier**, so the author fixes what most affects readers first:

   **CRITICAL** — breaks the reader's ability to follow the argument:
   - Information in the wrong section (misplaced methods, results, discussion)
   - Major gaps in the reverse outline (missing logical steps)
   - Disconnected or incoherent section handoffs
   - Multi-idea paragraphs that confuse distinct claims

   **MAJOR** — weakens clarity or buries important content:
   - Buried leads (key finding not stated first)
   - Paragraph ordering problems within sections
   - Non-forecasting lead sentences on important paragraphs
   - Missing transitions between paragraphs
   - Heading hierarchy issues (skipped levels, orphan headings)

   **MINOR** — polish that improves the reading experience:
   - Mechanical transitions ("Additionally," "Furthermore")
   - Given-new flow breaks within paragraphs
   - Paragraph length flags
   - Heading informativeness or parallelism
   - Redundant paragraphs that could be tightened

4. **Write the plan** in the restructuring-plan format from `references/report-template.md`.

## Phase 4: Apply fixes (fix modes only)

Skip this phase when `FIX_MODE` is `report` and go to Phase 5.

Build a **fix plan** from the restructuring plan, containing only items where a concrete text change can be specified. Each item records: file path, line number, current text, proposed replacement, reason, severity. Order by severity (CRITICAL first), then by position in the document (top first).

**Auto-fixable** — local changes that preserve the author's words:
- Lead sentence rewrites (THROAT-CLEARING or TOPIC-ONLY → the proposed FORECASTING version)
- Mechanical transition replacement ("Additionally," / "Furthermore," / "Moreover," → the proposed logical connector or bridging sentence)
- Paragraph splits at the identified split point
- Orphan sentence moves to the identified target paragraph
- Heading rewrites (vague → the proposed informative version)
- Redundant sentence cuts (GIVEN-GIVEN redundancy)
- Bridging sentence insertions where a transition was MISSING

**Recommend only** — these need the author's judgment or risk breaking the document, so list them in the report instead of applying them:
- Reordering paragraphs across sections (high risk of breaking cross-references)
- Moving content between sections (misplaced information)
- Merging paragraphs (requires judgment about what to keep)
- Restructuring the narrative arc
- Adding new content to fill reverse-outline gaps
- Changing heading hierarchy depth

### `review` mode (interactive)

For each fix plan item:
1. Run `code -g FILE:LINE` via Bash to open VS Code at the location.
2. Show severity, file and line, current text, proposed fix, and reason.
3. Ask with AskUserQuestion: "Apply this fix? (yes / skip / stop)". **yes** → apply immediately with Edit; **skip** → next item; **stop** → end and skip the rest.
4. Track applied vs. skipped.

### `diff` and `apply` modes

1. If `FIX_MODE` is `diff` and the file is not git-tracked, first copy it to `FILE.structural-editor-backup` so the user has something to diff against.
2. Launch a single fixer agent (`subagent_type: "general-purpose"`) using the Fixer Agent prompt from `references/agents.md`, with `{{FIX_PLAN}}` filled in. Use one fixer, not several, so edits never collide.
3. After it returns:
   - `diff`, git-tracked: run `code -g FILE:1` and tell the user to open Source Control (Cmd+Shift+G) to review and revert individual hunks.
   - `diff`, not git-tracked: run `code -d FILE.structural-editor-backup FILE`.
   - `apply`: summarize the changes only.

Record the outcome (applied / skipped / failed per item) as `FIX_RESULTS`.

## Phase 5: Save the report and tell the user

Save the report to `STRUCTURAL_EDIT_[YYYY-MM-DD].md` in the current working directory using the final report template in `references/report-template.md`. Include the "Fixes Applied" section only when a fix mode ran.

Then tell the user:
1. The path to the saved report
2. The executive summary (verbatim)
3. If fixes ran: how many were applied, skipped, and failed
4. The structural health summary table
5. The top 3 recommended next steps
6. In `diff` mode: a reminder to review the changes in VS Code Source Control (or the backup diff)

## Examples

```
/structural-editor                                   # report mode, academic, auto-detect paper
/structural-editor path/to/paper.tex                 # report on a specific file
/structural-editor review path/to/paper.tex          # interactive fix review
/structural-editor grant apply path/to/proposal.tex  # apply fixes to a grant proposal
/structural-editor thesis diff path/to/chapter3.tex  # diff mode for a thesis chapter
```

## Sources

This skill draws on:
- Williams, J.M. & Bizup, J. *Style: Lessons in Clarity and Grace* — given-new contract, coherence, cohesion
- Sword, H. (2012). *Stylish Academic Writing* — paragraph structure, storyline
- Bean, J.C. (2011). *Engaging Ideas* — paragraph unity, topic sentences, transitions
- Glasman-Deal, H. *Science Research Writing* — IMRAD structure, section roles
- Reverse outlining methodology from composition pedagogy
- Dane (1990) — thematic progression patterns (constant theme, linear theme, split theme)
- AJE three-phase manuscript editing workflow
- Bem, D.J. (2003). "Writing the Empirical Journal Article" — hourglass structure
- Structure & flow analysis patterns from the writing-editor skill
