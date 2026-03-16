---
name: write-paper
description: Write LaTeX paper sections based on outline.md using citations from main.bib
argument-hint: [section-name | "all"] (optional)
disable-model-invocation: true
---

# Write Paper Command

Iteratively transform outline into LaTeX. Each section is drafted, reviewed, and saved before proceeding.

## Input

$ARGUMENTS

## Reference

@paper/main.bib
@paper/outline.md
@.claude/reference/writing-style.md
@.claude/reference/latex-rules.md
@.claude/reference/latex-template.md

---

## Step 1: Validate Prerequisites

**outline.md:** If missing, error "No outline found. Run /develop-outline first." and stop.

**main.bib:** If missing, warn "No bibliography. Using (CITATION NEEDED) markers." If exists, load keys and report count.

---

## Step 2: Parse Outline

Extract from `paper/outline.md`:

- Section titles (`##` lines)
- Core claims (`**Core claim:**`)
- Key points (bullet lists)
- Citation pointers (`AuthorYearKey - ...`)

---

## Step 3: Determine Scope

**If $ARGUMENTS empty or "all":** Process all sections.

**If section name:** Fuzzy match against titles (case-insensitive, partial matches, keywords). If no match, list available sections and stop.

---

## Step 4: Check main.tex

**If exists:** Read and preserve preamble, title, authors, abstract, back matter. Identify insertion points.

**If missing:** Create from @.claude/reference/latex-template.md. Inform user.

---

## Step 5: Load Section Context

Classify the current section:
- **literature**: Introduction, Related Work, Background, Discussion
- **artifact**: Results, Materials and Methods
- **other**: Abstract, Conclusion, Significance Statement

### For `literature` sections:
- Extract citation keys (`AuthorYearKey` entries) from the outline section
- For each key: check `lit_review/paper_summaries/**/{Key}.md`; if found, load for context; if not, use BibTeX metadata only
- For Discussion specifically: `main.tex` (loaded in Step 4) contains previously written sections — reference this already-written content when discussing results; do NOT load artifact files

### For `artifact` sections:
- Extract `[artifact: path - description]` entries from the outline section
- **If artifact pointers found:** Read each referenced file; use content as primary context for writing
- **If NO artifact pointers found:** Use `AskUserQuestion`:
  > "The [Section Name] section has no artifact pointers in the outline. To write this section accurately, I need your actual results or methods details. Please:
  > 1. Provide file paths to relevant reports, scripts, or data files (e.g., `results/reports/stats.txt`, `code/analysis/model.py`)
  > 2. Paste relevant content directly into the chat
  > 3. Type 'write anyway' to proceed with outline guidance only (accuracy not guaranteed)"
  - If option 1: read the provided files and use as context
  - If option 2: use pasted content as context
  - If option 3: proceed with outline only; add a warning comment `% NOTE: written without artifact context — verify accuracy` at the section start

### For `other` sections:
- No special loading; use outline content only

---

## Step 6: Iterative Section Writing

For each section:

### 6a. Generate Draft

Write section header with label:

```latex
\section*{Section Title}
\label{sec:concise_name}
```

Generate prose following both @.claude/reference/writing-style.md (structure, tone, and PNAS section guidance) and @.claude/reference/latex-rules.md (citation mechanics and LaTeX formatting) for:

- Section structure and tone appropriate for PNAS Research Articles
- Hedged language guidelines
- Citation format (natbib)
- Paragraph structure

### 6b. Review

Present draft with citations list. Ask: **"Does this look good? Any changes before I save?"**

### 6c. Iterate

Revise based on feedback until approved.

### 6d. Save

Insert/update in `paper/main.tex`:

- New sections: before back matter
- Existing: replace between `\section*{Title}` and next section
- Preserve `% KEEP:` marked content

Confirm save, proceed to next section.

---

## Step 7: Final Report

```
Sections written: {count} - {list}
Citations used: {count} - {keys with counts}
Warnings: (CITATION NEEDED) count, sections without citations
Output: paper/main.tex
Next: compile command, review markers, /write-paper [section] to revise
```

---

## Edge Cases

- **Section in main.tex but not outline:** Preserve, don't overwrite.
- **Very long section:** Suggest subsections.
- **Missing summaries:** Use BibTeX only, note in report.
- **Conflicting content:** Ask "Replace, merge, or skip?"
- **User stops mid-iteration:** Previous sections already saved. List remaining, explain resume with `/write-paper [section]`.
- **Compile check:** Suggest `cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
