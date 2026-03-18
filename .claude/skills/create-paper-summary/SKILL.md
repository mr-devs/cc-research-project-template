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

**If $ARGUMENTS empty:** Ask user for path that contains the PDFs(e.g., `lit_review/papers/`).

**If $ARGUMENTS provided:** Use path; resolve relative paths from project root.

---

### Step 2: Identify PDFs to Process

**Single file:** Verify exists and is `.pdf`; note subdirectory relative to `lit_review/papers/`.

**Directory:** Recursively find all `.pdf` files; note each file's subdirectory.

Build list with full path and relative subdirectory. Report count; if zero, inform user and stop.

---

### Step 3: Build Work List

1. Read `paper/main.bib`; create lookup with normalized author+year → full entry data (key, title, authors, venue, year, DOI). Report count of existing entries.
2. For each PDF:
   - Parse filename → first author surname (normalized) and year
   - Search main.bib for matching entry; if missing, use the `fetchbib` skill to create one, then reload main.bib. Record BibTeX key.
   - Check if `lit_review/paper_summaries/{subdirectory}/{BibTeXKey}.md` already exists → mark as **skip** or **process**
3. Report counts: to process, skipped (summary exists), BibTeX entries created.

---

### Step 4: Create Summaries

For each PDF marked **process**:

#### 4a. Extract PDF Content (Token-Efficient)

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

#### 4b. Extract Metadata from BibTeX
From matching entry: Authors (comma-separated), Title, Year, Publication venue, DOI, BibTeX Key.

#### 4c. Generate Summary Sections

Per @.claude/reference/summary-format.md:

**Main Takeaways (max 5 bullets):**
- Focus on the paper's core contributions and findings
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
- Common types: sample size constraints, generalizability issues, temporal limitations, methodological trade-offs

#### 4d. Write Summary File
1. Create output directory if needed: `lit_review/paper_summaries/{subdirectory}/`
2. Write formatted markdown to `lit_review/paper_summaries/{subdirectory}/{BibTeXKey}.md` using the template from @.claude/reference/summary-format.md
3. Verify file created successfully
4. **After every 5 summaries**, run:
   ```
   /compact Compacting after 5 paper summaries. PRESERVE: (1) Task: creating paper summaries using /create-paper-summary command, (2) papers processed with output paths, (3) papers remaining to process, (4) any warnings/errors, (5) BibTeX state. DISCARD: All extracted PDF text content. Replace PDF extractions with: "Summarized: [filename] → [output_path]".
   ```

---

### Step 5: Report Results

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
Highlight that this work has not been peer-reviewed. Consider this fact when summarizing main takeaways and limitations.

### Review Papers
Main takeaways = synthesis findings; Methodology = review protocol; Limitations = gaps in reviewed literature.

### BibTeX Key Mismatch
If filename doesn't match any entry after normalization: search by title keywords as fallback; if still no match, create entry first.
