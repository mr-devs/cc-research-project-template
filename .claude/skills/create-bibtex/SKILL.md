---
name: create-bibtex
description: Create BibTeX entries from PDF papers and add to main.bib
argument-hint: <path/to/pdf-or-directory>
disable-model-invocation: false
---

# Create BibTeX Entry Command

Create BibTeX entries for academic PDFs and add to the main bibliography.

**Preferred method:** Extract DOI from PDF and use the fetchbib skill to fetch accurate BibTeX directly from doi.org. Falls back to title-based search, then manual PDF extraction only when both fail.

## Input

$ARGUMENTS

## Reference

@.claude/reference/bibtex-format.md

## Instructions

### Step 1: Determine Target Path

**If $ARGUMENTS empty:** Ask user for path (e.g., `lit_review/papers/00-background/file.pdf` or `lit_review/papers/`).

**If $ARGUMENTS provided:** Use path; resolve relative paths from project root.

---

### Step 2: Identify PDFs to Process

**Single file:** Verify exists and is `.pdf`; report error and stop if not.

**Directory:** Recursively find all `.pdf` files using `{path}/**/*.pdf`.

Build list of PDF paths. Report count; if zero, inform user and stop.

---

### Step 3: Load Existing BibTeX Entries

1. Read `paper/main.bib`
2. Extract from each entry: BibTeX key, first author surname (normalized), year
3. Create lookup set for duplicate checking

Report count of existing entries.

---

### Step 4: Check Each PDF Against Existing Entries

Parse each filename for author and year:

**Filename formats:**
- `Author et al. - YYYY - Title.pdf`
- `Author and Author2 - YYYY - Title.pdf`
- `Author - YYYY - Title.pdf`

**Extraction:**
1. First author surname: text before ` et al.`, ` and `, or first ` - `
2. Year: 4-digit number after first ` - `
3. Normalize surname: remove accents, remove hyphens

**Check for match:** If normalized author+year exists in main.bib → skip ("Entry already exists"); otherwise → process.

Report counts: skipped (existing) and to process (new).

---

### Step 5: Process Each New PDF

#### 5a. Try DOI-Based Fetch First (Preferred Method)

**Always attempt DOI extraction first** - this yields the most accurate BibTeX:

1. **Search for DOI in the PDF:**
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search "{pdf_path}" "doi"
   ```

2. **If DOI found, use fbib:**
   ```bash
   fbib "{extracted_doi}"
   ```

3. **If fbib returns valid BibTeX:** Use it directly, but regenerate the BibTeX key per Step 5c below to match project conventions.

4. **If DOI not found or fetch fails:** Try title-based search (Step 5a-ii) before falling back to manual extraction (Step 5b).

#### 5a-ii. Title-Based Search Fallback

If no DOI was found or `fbib` fetch failed:

1. **Extract first page to get the paper title:**
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh first "{pdf_path}" 1
   ```

2. **Run a title-based search:**
   ```bash
   fbib "Full Paper Title"
   ```

3. **If fbib returns valid BibTeX:** Use it directly, but regenerate the BibTeX key per Step 5c below to match project conventions.

4. **If title search also fails:** Fall through to full manual extraction (Step 5b).

#### 5b. Fallback: Extract PDF Metadata Manually

Only use this if both DOI-based fetch and title-based search fail. Use the pdf-extraction skill for minimal token usage:

1. **Extract first page** (contains title, authors, abstract, venue info):
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh first "{pdf_path}" 1
   ```

2. **If venue not found, search for it:**
   ```bash
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search "{pdf_path}" "journal"
   .claude/skills/pdf-extraction/scripts/pdf_extract.sh search "{pdf_path}" "conference"
   ```

3. **Only extract additional pages if critical info still missing**

**Never read the entire PDF.** Extract minimally, verify you have: title, authors, year, venue.

#### 5b. Determine Entry Type

| Indicators | Entry Type |
|------------|------------|
| Journal name, volume/issue | `@article` |
| "Proceedings of", conference | `@inproceedings` |
| arXiv URL, "preprint" | `@misc` |
| Technical/institutional report | `@techreport` |
| ISBN, book publisher | `@book` |
| Dissertation, thesis | `@phdthesis` |

#### 5c. Generate BibTeX Key

Per @.claude/reference/bibtex-format.md:
1. First author surname (normalized)
2. 4-digit year
3. First significant title word (skip "The", "A", "An", "On", "Using")

Format: `{Author}{Year}{Keyword}` (e.g., `FernandezPichel2025Evaluating`)

If key exists: append lowercase letter (`a`, `b`, `c`...).

#### 5d. Format Entry

Per @.claude/reference/bibtex-format.md:
- Tab indentation
- Title in double braces `{{...}}`
- Authors as `Lastname, Firstname and Lastname2, Firstname2`
- 3-letter lowercase month
- Trailing comma after last field

**URL priority:** DOI URL first (`https://doi.org/{DOI}`); else other reliable URL; else omit.

**arXiv:** Use `howpublished = {arXiv [Preprint]}` (not `publisher` or `note`).

---

### Step 6: Append to main.bib

1. Read current `paper/main.bib`
2. Append each new entry (blank line before each)
3. Write updated content

Verify file written successfully.

---

### Step 7: Report Results

```
BibTeX Creation Summary
=======================
PDFs found: {total}
Skipped (entry exists): {skipped}
New entries created: {created}
  - Via fbib (DOI): {doi_count}
  - Via fbib (title search): {title_count}
  - Via manual extraction: {manual_count}

New entries:
- {Key1} ({filename1}) [fbib-doi]
- {Key2} ({filename2}) [fbib-title]
- {Key3} ({filename3}) [manual]

Warnings (if any):
- {filename}: {warning}
```

**Possible warnings:** "DOI fetch failed, used manual extraction", "Could not extract DOI", "Non-standard filename", "Could not determine venue", "Month not available"

---

### Step 7.5: Auto-Compact (After Every 5 Papers)

After processing every 5 PDFs, run:
```
/compact Compacting after processing 5 papers. PRESERVE: (1) Task: creating BibTeX entries using /create-bibtex command, (2) files processed with BibTeX keys created, (3) files remaining to process, (4) any warnings/errors. DISCARD: All extracted PDF text content. Replace PDF extractions with: "Processed: [filename] → [BibTeX key created]".
```

---

## Edge Cases

### Non-standard Filename
For files not matching `Author - Year - Title` format: read PDF to extract metadata; use organization name if author is organization; report warning.

### Missing Information

| Missing | Action |
|---------|--------|
| DOI | Omit field; use alternate URL if available |
| Month | Omit field |
| Pages | Omit field |
| Volume/Issue | Omit fields |
| Venue | Use `@misc`; add note |

### Accented Characters
- **Keys:** Remove accents (é→e, ü→u, ñ→n)
- **Author names:** Preserve as-is
- **Titles:** Preserve; wrap in double braces

### Unreadable PDF
Report error "Could not read PDF: {filename}", skip file, continue.
