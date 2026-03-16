# Paper Writing

Once your literature is summarized and organized, these skills help you build a structured argument and translate it into a LaTeX manuscript. Both work iteratively — through conversation and section-by-section review — so you stay in control of the argument at every stage.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/develop-outline [context]` | Builds or refines `paper/outline.md` through an interactive dialogue — asking about purpose, audience, structure, and venue for new outlines, or summarizing and proposing extensions to existing ones; optionally pulls citation pointers from `lit_review/paper_summaries/` and `paper/main.bib`. |
| `/write-paper [section]` | Reads `paper/outline.md` and the relevant paper summaries, drafts each section as LaTeX prose with natbib citations, presents each draft for your review before saving, and inserts approved sections into `paper/main.tex`; omit the section argument to write all sections, or target a single section by name. |
