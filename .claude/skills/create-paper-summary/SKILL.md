---
name: create-paper-summary
description: Create markdown summaries for PDF papers (creates BibTeX first if needed)
argument-hint: <path/to/pdf-or-directory>
disable-model-invocation: true
---

# Create Paper Summary Command

Create markdown summaries for academic PDFs.

## Input

$ARGUMENTS

## Reference

@.claude/reference/summary-format.md
@.claude/reference/bibtex-format.md

## Instructions

### Step 1: Determine Target Path

**If $ARGUMENTS empty:** Ask user for path (e.g., `lit_review/papers/00-background/file.pdf` or `lit_review/papers/`).

**If $ARGUMENTS provided:** Use path; resolve relative paths from project root.

---

### Step 2: Identify PDFs to Process

**Single file:** Verify exists and is `.pdf`; note subdirectory relative to `lit_review/papers/`.

**Directory:** Recursively find all `.pdf` files; note each file's subdirectory.

Build list with full path and relative subdirectory. Report count; if zero, inform user and stop.

---

### Step 3: Load Existing BibTeX Entries

1. Read `paper/main.bib`
2. Create lookup with normalized author+year → full entry data (key, title, authors, venue, year, DOI)

Report count of existing entries.

---

### Step 4: Verify BibTeX Entries Exist

For each PDF:

#### 4a. Parse Filename
Extract first author surname (normalized) and year from filename.

#### 4b. Find Match
Search main.bib for entry where normalized author+year matches.

#### 4c. Handle Missing
**If NO match:** Report "No BibTeX entry found for: {filename}". Run create-bibtex logic for this PDF (see create-bibtex.md Steps 5-6), reload main.bib, record new key.

**If match found:** Record BibTeX key.

---

### Step 5: Check for Existing Summaries

For each PDF:
1. Expected path: `lit_review/paper_summaries/{subdirectory}/{BibTeXKey}.md`
2. If exists → skip ("Summary already exists"); if not → process

Report counts: skipped, to process, BibTeX entries created in Step 4.

---

### Step 6: Create Summary for Each PDF

#### 6a. Extract PDF Content (Token-Efficient)

Use the pdf-extraction skill strategically:

1. **Start with first page** (contains title, authors, abstract):
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh first "{pdf_path}" 1
   ```

2. **Locate key sections by searching:**
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search-pages "{pdf_path}" "Method"
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search-pages "{pdf_path}" "Results"
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search-pages "{pdf_path}" "Limitation"
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search-pages "{pdf_path}" "Discussion"
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search-pages "{pdf_path}" "Conclusion"
   ```

3. **Extract only the pages containing those sections:**
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh page "{pdf_path}" {page_num}
   ```
   Or use range for consecutive pages:
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh range "{pdf_path}" {start} {end}
   ```

**Token Budget:** Aim for ~4-6 pages of content per paper maximum.

**For short papers (<8 pages):** May extract the whole thing:
```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh all "{pdf_path}"
```

**Never extract the full PDF for papers >8 pages.** Target specific sections.

Identify sections: Abstract, Introduction, Methods, Results, Discussion, Limitations, Conclusion.

#### 6b. Extract Metadata from BibTeX
From matching entry: Authors (comma-separated), Title, Year, Publication venue, DOI, BibTeX Key.

#### 6c. Generate Summary Sections

Per @.claude/reference/summary-format.md:

**Main Takeaways (max 5 bullets):**
- Focus on LLM/health relevance
- Prioritize empirical over theoretical
- Include significant statistics
- Be concise but specific

**Methodological Approach (max 4 bullets):**
- Study design
- Data sources/sample sizes
- Analysis methods
- Key tools/frameworks

**Limitations (max 4 bullets):**
- Check paper's limitations section first
- Sample size constraints
- Generalizability issues
- Temporal limitations

#### 6d. Format Summary
Use template from @.claude/reference/summary-format.md.

---

### Step 7: Create Output Directory

For each summary:
1. Target: `lit_review/paper_summaries/{subdirectory}/`
2. Create subdirectory if needed
3. Full path: `lit_review/paper_summaries/{subdirectory}/{BibTeXKey}.md`

| Source PDF | Summary |
|------------|---------|
| `lit_review/papers/00-background/Biswas - 2023 - Role.pdf` | `lit_review/paper_summaries/00-background/Biswas2023Role.md` |

---

### Step 8: Write Summary Files

For each summary:
1. Write formatted markdown (UTF-8)
2. Verify created successfully
3. **After every 5 summaries**, run:
   ```
   /compact Compacting after 5 paper summaries. PRESERVE: (1) Task: creating paper summaries using /create-paper-summary command, (2) papers processed with output paths, (3) papers remaining to process, (4) any warnings/errors, (5) BibTeX state. DISCARD: All extracted PDF text content. Replace PDF extractions with: "Summarized: [filename] → [output_path]".
   ```

---

### Step 9: Report Results

```
Paper Summary Creation Summary
==============================
PDFs found: {total}
Skipped (summary exists): {skipped}
New summaries created: {created}
BibTeX entries created: {bib_created}

New summaries:
- {path1}
- {path2}

Warnings (if any):
- {filename}: {warning}
```

---

## Edge Cases

### Unreadable PDF
Report error "Could not read PDF: {filename}", skip file, continue.

### Missing DOI
```markdown
- **DOI:** Not available
- **URL:** [{url}]({url})
```
If no URL either, just `- **DOI:** Not available`.

### Short Papers
If paper lacks distinct sections: describe general approach for methodology; note "Not explicitly discussed" for limitations and infer obvious ones.

### Non-Research Papers (Reports, White Papers)
Adapt headers: "Key Findings" → Main Takeaways; "Approach" → Methodology; "Caveats" → Limitations.

### Review Papers
Main takeaways = synthesis findings; Methodology = review protocol; Limitations = gaps in reviewed literature.

### BibTeX Key Mismatch
If filename doesn't match any entry after normalization: search by title keywords as fallback; if still no match, create entry first.
