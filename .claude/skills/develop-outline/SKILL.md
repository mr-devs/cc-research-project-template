---
name: develop-outline
description: Iteratively develop an outline for academic writing
argument-hint: [any directions or context for the outline]
disable-model-invocation: true
---

# Develop Outline Command

Build or refine `paper/outline.md` through conversation.

## Input

$ARGUMENTS

## Reference

@paper/main.bib
@.claude/reference/outline-format.md

---

## Step 1: Detect Mode

Check if `paper/outline.md` exists.

**If exists:** Read file, summarize structure (sections, core claims, citations), ask "What would you like to refine or extend?" Then proceed to Step 3 or 4.

**If not exists:** Inform user "No existing outline found. Let's build one from scratch." Proceed to Step 2.

---

## Step 2: Context Gathering (New Outlines Only)

Ask open-ended questions. Do NOT assume a specific paper type.

1. "What is the main purpose or argument?"
2. "Who is the intended audience?"
3. "What key points or themes to cover?"
4. "Do you have a structure in mind?"
5. "Target venue (journal, conference, magazine)?"
6. "Any page or word limits?"

Skip questions already answered in $ARGUMENTS. Record venue and length for the outline header.

---

## Step 3: Document Leverage (Optional)

### Step 3a — Citation Pointers (for literature sections)

Ask: **"Would you like me to include citation pointers from the paper summaries and bibliography for Introduction and Discussion sections?"**

**If yes:** Scan `lit_review/paper_summaries/` and `paper/main.bib`. Suggest citations as you develop each section using format: `AuthorYearKey - [relevance note]`

**If no:** Proceed without citations.

### Step 3b — Artifact Pointers (for artifact sections)

Ask: **"Would you like to link code files, reports, or data artifacts to Results and Methods sections?"**

**If yes:** For each Results/Methods section during Step 5 development, prompt: "What files (reports, scripts, data) should I reference when writing this section? Use format: `[artifact: path - description]`"

**If no:** Proceed without artifact pointers (user can add them later).

---

## Step 4: Structure Proposal

1. Present draft section list with brief descriptions
2. Ask: "Does this capture your goals? What would you add, remove, or reorder?"
3. Iterate until approved

Follow format in @.claude/reference/outline-format.md.

---

## Step 5: Section-by-Section Development

For each section:

1. **Draft:** Core claim + key points + citations (if enabled)
2. **Present:** Show draft, ask "Does this capture what you want? Any adjustments?"
3. **Iterate** until approved
4. **Save** every 2-3 sections to `paper/outline.md`

---

## Step 6: Integration Review

After all sections drafted:

1. Check logical flow, gaps, redundancy
2. Present complete outline with any issues highlighted
3. Ask: "Would you like to adjust structure or refine sections?"
4. Iterate as needed

---

## Step 7: Final Save

Write to `paper/outline.md` following the format in @.claude/reference/outline-format.md.

Report: sections count, citations included, venue, constraints, file path, next steps.

---

## Principles

**Do NOT:** Assume paper type, number sections, force rigid templates, add citations without consent.

**DO:** Follow user's lead, ask clarifying questions, save incrementally, preserve existing structure when revising.

---

## Edge Cases

- **Detailed $ARGUMENTS:** Skip redundant questions, extract structure, confirm.
- **Start over:** Confirm replacement, backup to `paper/outline.backup.md`.
- **Long outline (>8 sections):** Offer to work in phases.
- **User stops:** Save current progress, inform how to resume with `/develop-outline`.
