---
name: writing-editor
description: >-
  Multi-agent line editor that makes prose clearer, tighter, and more human: three read-only analysts
  (structure and flow, clarity and AI-writing pathologies, voice and accessibility) feed one editor agent
  that applies every fix, with VS Code diff, interactive, or headless review. Use this skill whenever the
  user asks to edit, tighten, polish, copy-edit, or line-edit a draft, make writing clearer or more
  readable, cut jargon or filler, fix flow, or make text sound less AI-generated or robotic, for academic
  papers, grant proposals, op-eds, blog posts, technical docs, or general prose, even if they never name
  the skill. Not for reorganizing paragraphs and sections (use structural-editor) or judging the
  argument and contribution (use top3-reviewer).
argument-hint: "[academic|op-ed|blog|technical|grant|general] [diff|review|apply] [path/to/file]"
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
  version: 2.3.0
  source: https://github.com/SolomonMg/research-agent-skills
---

# Writing Editor

Coordinate a multi-agent line edit. Three analyst agents read the text in parallel and return findings with concrete rewrites; you merge them into one edit plan; then a single editor agent applies the plan. Analysts only read and only the editor writes, so there are never conflicting edits to the same file, and every change traces back to a specific finding the user can review.

The goal is prose that is clear, logically ordered, original in expression, and accessible: what a person with expertise sounds like talking to a curious colleague.

## Scope and related skills

This skill works at the sentence and paragraph level: clarity, filler, AI-writing pathologies, voice, rhythm, jargon, and claim discipline. It touches all prose in the document, including appendices, footnotes, and figure/table captions. For other jobs, point the user to:

- **structural-editor**: paragraph ordering, section architecture, heading hierarchy, narrative arc
- **top3-reviewer**: argument logic, contribution, and framing
- **abstract-checker**: whether the abstract matches and highlights the body
- **bibliography-checker**: citation existence, accuracy, and coverage
- **statistical-reviewer**: statistical methods and reporting
- **review-paper-code**: research code and paper-code alignment

## Reference files

Read these when you reach the phase that needs them:

| File | Read in | Contains |
|---|---|---|
| `references/agents.md` | Phase 2 | Prompts for the three analyst agents, plus placeholder definitions |
| `references/pathology-catalog.md` | Phase 2 | The P0/P1/P2 pathology catalog and C1–C6 clarity issues; paste into Agent 2's prompt |
| `references/editor-agent.md` | Phase 5 | The editor agent's prompt, knowledge base, editing process, and long-text handling |

Subagents cannot see this skill's directory, so always paste the full prompt text (with placeholders filled) into each Agent call rather than pointing the agent at a file.

## Phase 1: Parse arguments and discover the text

Parse `$ARGUMENTS` into three values. Tokens can appear in any order and are case-insensitive.

**Writing context** (`WRITING_CONTEXT`, default `general`):

| Token | Use for |
|---|---|
| `academic` | Research papers, journal articles, dissertations |
| `op-ed` | Opinion pieces, essays, commentary |
| `blog` | Blog posts, newsletters |
| `technical` | Documentation, technical reports, READMEs |
| `grant` | Grant proposals, funding applications |
| `general` | Anything else |

**Review mode** (`REVIEW_MODE`, default `diff`). Unlike the other skills in this family, which default to a read-only report, this skill edits by default, because the user asked for an edit. `diff` keeps that safe by making every change visible and individually revertible.

| Token | Behavior |
|---|---|
| `diff` (default) | Editor applies all edits in place; then open a VS Code diff so the user can revert individual hunks. |
| `review` | No editor agent. Walk the user through each finding in VS Code (`code -g file:line`); apply only the ones they approve. |
| `apply` | Editor applies all edits; no VS Code. For headless or non-VS-Code environments. |

**File path**: whatever text remains. If there is none, use AskUserQuestion to ask which file to edit or whether they'll paste text. If they paste, save it to a temporary file so the agents can read it, and remember that it was pasted (the editor writes pasted text to `edited_output.md` instead of editing in place).

If the user's request (rather than `$ARGUMENTS`) makes the context obvious, such as "polish my grant aims page", use that context.

Read the source file(s) and record:
- Full file path(s)
- Approximate word count
- Section boundaries (headings, chapter breaks), which the editor needs for long-text chunking

Select the matching row of the context adaptation table; every agent receives it.

**Context adaptation table**

| Context | Pathology strictness | Voice | Jargon tolerance | Structure |
|---|---|---|---|---|
| academic | Standard (but apply all tiers) | Restrained, reactive | Moderate (define on first use) | Formal sections |
| op-ed | Strict | Strong personality | Low | Narrative flow |
| blog | Strict | Conversational | Low | Short sections |
| technical | Standard | Neutral-clear | High (known audience) | Reference structure |
| grant | Strict | Direct, urgent | Moderate | Prescribed format |
| general | Strict | Author's natural voice | Low | Flexible |

## Phase 2: Launch the three analyst agents in parallel

Read `references/agents.md` and `references/pathology-catalog.md`. For each of the three agents, fill the placeholders (file paths, writing context, context row; for Agent 2, paste in the full pathology catalog) and launch it with the Agent tool, `subagent_type: "general-purpose"`. Send all three Agent calls in a single message so they run concurrently.

| Agent | Focus | Returns |
|---|---|---|
| 1 — Structure & Flow | Reverse outline, paragraph coherence, buried leads, transitions, claim-evidence alignment | `S`-numbered structural issues |
| 2 — Clarity & Pathology | P0/P1/P2 pathologies, C1–C6 clarity issues, document-wide P2 sweep, rewrite-from-scratch flags | `L`-numbered line edits with rewrites, per paragraph |
| 3 — Voice & Accessibility | Soulless passages, verbal tics, jargon, rhythm, missing concrete anchors, claim discipline | Voice notes (`V`) and claim-discipline items (`D`) |

Agents return findings in their reply and write no files.

## Phase 3: Build the edit plan

Once all three agents return, merge their findings yourself into one edit plan. The plan is the bridge between analysis and editing, so keep it terse, location-specific, and actionable.

1. **Deduplicate.** If two agents flag the same passage (e.g., a vague attribution that is also soulless), keep the finding with the more specific fix and note the overlap.
2. **Resolve conflicts by sequencing.** If Agent 1 says "move paragraph 5 before paragraph 3" and Agent 2 says "rewrite paragraph 5 from scratch," rewrite first, then move.
3. **Order by impact, but keep every tier.** Order the plan: P0 pathologies > structural issues > P1 > clarity issues > voice/accessibility > P2 > claim discipline. This order decides what gets applied first, not what gets skipped. Every finding from every tier goes into the plan with its analyst-provided rewrite, and the editor must apply or explicitly decline each one. P2 items are not optional polish; they are much of the difference between good writing and great writing.
4. **Write the plan** in this format:

```
## EDIT PLAN

### Writing context: [WRITING_CONTEXT]
### Pathology strictness: [from context adaptation table]

### STRUCTURAL EDITS (from Agent 1)
S1. [ISSUE_TYPE]: [location] | [description] | Severity: [must-fix / should-fix / consider]
S2. ...

### LINE EDITS BY PARAGRAPH (from Agent 2)
#### Para [N] (density: [count] flags — [PATCH / REWRITE_FROM_SCRATCH])
L1. [ID] "[quoted text]" → [replacement] | [severity]
L2. ...

### VOICE & ACCESSIBILITY NOTES (from Agent 3)
V1. [location]: [issue] | [suggestion]
V2. ...

### CLAIM DISCIPLINE (from Agent 3, if applicable)
D1. [location]: [issue] | [suggestion]
D2. ...
```

## Phase 4: Route by review mode

### `review` mode: interactive, finding by finding

Skip the editor agent; you apply edits directly. For each finding in the plan, must-fix first:

1. Run `code -g FILE:LINE` via Bash to open VS Code at the finding.
2. Show in the terminal: issue type, severity, quoted text, and suggested replacement.
3. Ask with AskUserQuestion: "Apply this edit? (yes / skip / stop)"
   - **yes**: apply it now with the Edit tool.
   - **skip**: move to the next finding.
   - **stop**: end the review and skip all remaining findings.
4. Track applied vs. skipped, then go to Phase 6.

### `diff` and `apply` modes: prepare for in-place editing

The editor edits the original file in place, so make sure the original is recoverable before it starts:

- **`diff`, git-tracked file** (check with `git ls-files --error-unmatch FILE`): git already holds the original; no backup needed.
- **`diff`, not git-tracked**: create the backup now, before launching the editor: `cp FILE FILE.writing-editor-backup`.
- **`apply`**: no VS Code step. If the file is not git-tracked, still make the backup above so the user can revert.

Then continue to Phase 5.

## Phase 5: Launch the editor agent (`diff` and `apply` only)

Read `references/editor-agent.md`, fill its placeholders (file paths, pasted-text flag, writing context, context row, and the complete edit plan from Phase 3), and launch a single editor agent with `subagent_type: "general-purpose"`. This is the only agent that writes files.

The editor applies structural edits first, then line edits, voice notes, claim discipline, a P2 sweep, and a self-audit. It handles texts over ~5,000 words section by section, sequentially, to keep the voice consistent. It returns a changes summary that accounts for every plan item as applied or declined with a reason.

After the editor returns:
- **`diff`, git-tracked**: run `code -g FILE:1`.
- **`diff`, not git-tracked**: run `code -d FILE.writing-editor-backup FILE`.
- **`apply`**: no VS Code interaction.

## Phase 6: Present results

Tell the user:

1. **Edited file location**: the path edited in place, or `edited_output.md` for pasted text.
2. **Structural notes**: high-level organization changes (paragraphs moved, split, merged).
3. **Changes summary**: from the editor's report (or your applied/skipped tally in `review` mode), grouped by category.
4. **Remaining issues**: anything the editor flagged as still imperfect, with reasoning.
5. **How to review** (`diff` mode):
   - Git-tracked: "Open Source Control (Cmd+Shift+G / Ctrl+Shift+G) and click the file in the changes list to see the diff. Use the ↩ buttons in the gutter to revert individual hunks. To revert everything: `git checkout -- FILE`."
   - Not git-tracked: "The VS Code diff view is open: original on the left, edited on the right. When satisfied: `rm FILE.writing-editor-backup`. To revert: `cp FILE.writing-editor-backup FILE`."

Substitute the real file name for `FILE` in these messages.

## Sources

This skill synthesizes guidance from:
- Severity-tier methodology from Conor Bronsdon's writing pathology system
- Economics writing principles from Cochrane, McCloskey, Shapiro, and Bellemare
- Common AI writing pathologies documented by [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup)
- Paragraph-level clarity checks and reverse outlining from research paper writing methodology
- The verbal tic test from journalism editing practice
