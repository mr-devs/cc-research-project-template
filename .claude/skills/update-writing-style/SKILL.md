---
name: update-writing-style
description: Use when updating or replacing the writing style configuration for the paper-writing pipeline, targeting a new venue, audience, or style preferences.
disable-model-invocation: true
argument-hint: "[description of desired writing style or target venue]"
allowed-tools: Read, Write, AskUserQuestion
---

# Update Writing Style

Interactively update `.claude/reference/writing-style.md` for a target venue or writing preference.

## Input

$ARGUMENTS

---

## Step 1: Parse Arguments

Extract any of the following from $ARGUMENTS if present:
- Target venue and article type
- Audience description
- Length/page constraints
- Tone preferences
- Section structure preferences

---

## Step 2: Check Existing File

Check if `.claude/reference/writing-style.md` exists.

**If exists:** Read it, summarize current settings (venue, audience, article type, length, tone). Then ask:

> "I found an existing writing style file. Would you like to replace it entirely, or update specific sections?"
> Options: Replace entirely / Update specific sections / Let Claude decide

**If not exists:** Inform user "No existing writing style found. Let's build one from scratch." Proceed to Step 3.

---

## Step 3: Gather Missing Information

For each piece of information NOT found in $ARGUMENTS, use `AskUserQuestion`. Always include "Let Claude decide" as an option.

**Target venue** (if missing):
> "What is the target venue and article type?"
> Options: PNAS Research Article / Nature Communications / Science / PNAS Perspective / Nature Commentary / Other (specify) / Let Claude decide

**Audience** (if missing):
> "Who is the primary audience?"
> Options: Broad scientific community (non-specialist friendly) / Domain specialists only / Mixed / Let Claude decide

**Length constraints** (if missing):
> "What are the length constraints?"
> Options: ~6 pages / ~10 pages / No limit / Let Claude decide based on venue

**Tone** (if missing):
> "What tone and voice style?"
> Options: Precise and direct (minimize hedging) / Balanced hedging / Conservative/heavily hedged / Let Claude decide based on venue

**Section structure** (if missing):
> "Should I derive section structure from the target venue's standard format?"
> Options: Yes, use standard structure for [venue] / Let me describe custom structure / Let Claude decide

---

## Step 4: Generate Draft

Produce a draft `writing-style.md` with the following sections:

- **Target Venue**
- **Audience**
- **Article Type**
- **Standard Section Structure** — numbered list with word-limit notes per section
- **Length** — approximate page and word count
- **Tone and Voice** — voice, hedging, qualifiers
- **Section-Specific Guidance** — per section: Significance Statement, Abstract, Introduction, Results, Discussion, Materials and Methods

**Do NOT include** LaTeX citation rules, natbib syntax, or hedged language tables — those belong in `latex-rules.md`.

---

## Step 5: Review Loop

Present the full draft to the user. Ask:

> "Does this look right?"
> Options: Looks good, save it / I have changes (describe them) / Start over

If changes requested: apply them and re-present. Repeat until approved.

If "Start over": return to Step 3 and re-gather information.

---

## Step 6: Save

Write the approved content to `.claude/reference/writing-style.md`.

Confirm: "Saved to `.claude/reference/writing-style.md`. `/write-paper` will now use this updated style."

---

## Principles

**Do NOT:** Include LaTeX citation syntax, natbib commands, or hedged language substitution tables — those belong in `.claude/reference/latex-rules.md`.

**DO:** Ask `AskUserQuestion` for missing information, always including "Let Claude decide" as an option. Skip questions already answered in $ARGUMENTS.
