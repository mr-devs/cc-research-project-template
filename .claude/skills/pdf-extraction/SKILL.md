---
name: pdf-extraction
description: Extract text from PDF documents efficiently using poppler's pdftotext. Use when reading academic papers, extracting metadata, or searching PDF content.
allowed-tools: Bash, Read
user-invocable: false
---

# PDF Extraction Skill

Extract text from PDF documents efficiently using poppler's `pdftotext` utility.

## Available Script

Use the extraction script at `.claude/skills/pdf-extraction/scripts/pdf_extract.sh`

## Commands

### Extract First N Pages (Default Strategy)

For metadata extraction (title, authors, abstract, venue info):

```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh first "{pdf_path}" 3
```

### Extract Specific Page

```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh page "{pdf_path}" {page_num}
```

### Extract Page Range

```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh range "{pdf_path}" {start} {end}
```

### Search for Text

Returns matching lines with line numbers:

```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh search "{pdf_path}" "query"
```

### Find Pages Containing Query

Identifies which pages contain specific content:

```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh search-pages "{pdf_path}" "Method"
```

### Extract Entire PDF (Use Sparingly)

Only for short papers (<8 pages):

```bash
.claude/skills/pdf-extraction/scripts/pdf_extract.sh all "{pdf_path}"
```

## Strategic Extraction Patterns

### For BibTeX Metadata
1. Extract first 2-3 pages (contains title, authors, abstract, venue)
2. If DOI/venue not found, search for specific terms
3. Only extract additional pages if critical info missing

### For Paper Summaries
1. Extract first 3 pages for abstract + introduction
2. Use `search-pages` to locate key sections (Methods, Results, Limitations, Discussion, Conclusion)
3. Extract only the pages containing those sections
4. Target ~4-6 pages of content maximum

## Token Efficiency Guidelines

- **Never** read entire PDFs for papers >8 pages
- Start with minimal extraction, expand only if needed
- Use search commands to locate specific content before extracting pages
- For batch processing: compact context after every 5 papers
