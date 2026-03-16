---
name: fetchbib
description: Fetch BibTeX citation from a DOI or paper title and add to .bib file. Use when user provides a DOI, DOI URL, or full paper title and needs a BibTeX entry added to their bibliography, especially when working on academic papers.
argument-hint: <DOI, https://doi.org/..., or "Full Paper Title">
---

# Fetch BibTeX

## Fetch BibTeX

```bash
fbib <DOI or "Full Paper Title">
```

Accepts bare DOIs (`10.1038/nature12373`), full DOI URLs, or quoted paper titles for free-text search.

## Workflow

1. Fetch the BibTeX entry
2. Find .bib file (check current dir, then parents; common names: `references.bib`, `main.bib`)
3. Show the entry and ask user: add to found file, specify different file, or just display
4. If adding: check for duplicate DOI first, then append
