# Literature Review

During the literature review phase, you collect PDFs, build a bibliography, and generate structured summaries of each paper. These skills handle the full workflow from raw files to citable, summarized sources ready to feed into the outline and writing steps.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/cleanup-pdf-names <path>` | Renames all PDFs in a directory (recursively) to replace spaces, em dashes, en dashes, and special characters with underscores and standard hyphens; run this before any other pipeline step to ensure consistent filenames that won't cause issues downstream. |
| `/fetchbib <DOI or "Title">` | Fetches a single BibTeX entry by DOI or paper title and appends it to `paper/main.bib`; use this when you need to add one paper at a time rather than processing a whole directory. |
| `/create-bibtex <path>` | Processes one PDF or an entire directory of PDFs and creates BibTeX entries for each by extracting the DOI (preferred), falling back to a title search via OpenAlex, then manual metadata extraction; appends all new entries to `paper/main.bib`, skipping papers that already have entries. |
| `/create-paper-summary <path>` | Generates a structured markdown summary (main takeaways, methodology, limitations) for each PDF, automatically creating a BibTeX entry first if one doesn't exist; saves summaries to `lit_review/paper_summaries/` mirroring the `papers/` subdirectory structure, named by BibTeX key. |
| `pdf-extraction` _(internal)_ | A utility skill called automatically by `/create-bibtex` and `/create-paper-summary` to extract targeted text from PDFs using `pdftotext`; it is not user-invocable but handles all PDF reading in the pipeline, using targeted page extraction to minimize token usage. |
