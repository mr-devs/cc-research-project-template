# Paper Writing

Once your literature is summarized and organized, these skills help you build a structured argument and translate it into a LaTeX manuscript. Both work iteratively — through conversation and section-by-section review — so you stay in control of the argument at every stage.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/develop-outline [context]` | Builds or refines `paper/outline.md` through an interactive dialogue — asking about purpose, audience, structure, and venue for new outlines, or summarizing and proposing extensions to existing ones; optionally pulls citation pointers from `lit_review/paper_summaries/` and `paper/main.bib`. |
| `/write-paper [section]` | Reads `paper/outline.md` and loads section-appropriate context — paper summaries for literature-heavy sections (Introduction, Discussion), artifact files for empirical sections (Results, Methods) — drafts each section as LaTeX prose with natbib citations, presents each draft for your review before saving, and inserts approved sections into `paper/main.tex`; omit the section argument to write all sections, or target a single section by name. |

> **Note on writing style:** The sentence-level style guidance in [`.claude/reference/writing-style.md`](../../.claude/reference/writing-style.md) is derived from Gopen, G. D., & Swan, J. A. (1990). "The Science of Scientific Writing." *American Scientist*, journal of Sigma Xi. [[PDF]](https://www.usenix.org/sites/default/files/gopen_and_swan_science_of_scientific_writing.pdf)

## Reviewing and Revising the Manuscript

Once a full draft exists in `paper/main.tex`, these skills audit it from different angles before submission.
Each one runs as a review by default; most also accept `diff` or `apply` as a final argument to propose or make fixes.
They are scoped to avoid overlap, so run the ones that match the concern at hand.

| Command | Description |
|---------|-------------|
| `/top3-reviewer [paper] [journal]` | Referee-style review of the argument, coherence, and contribution, held to the standard of a top general-science journal (or a named venue). |
| `/statistical-reviewer [paper] [perspective] [journal]` | Multi-agent review of statistical methods, p-value consistency, effect sizes, causal identification, and causal-language overreach; optionally critiques from a named statistician or school. |
| `/review-paper-code [paper] [code_dir]` | Audits the analysis code in `code/` against the paper for reproducibility, data integrity, analytical correctness, and paper-code alignment. |
| `/abstract-checker [paper]` | Verifies every abstract claim against the body and checks that the body's key findings appear in the abstract; can rewrite the abstract. |
| `/bibliography-checker [paper] [style]` | Verifies via web search that each cited work exists and is described faithfully, flags claims that need citations, and identifies important missing literature; can fix `paper/main.bib`. |
| `/structural-editor [file] [genre]` | Diagnoses paragraph-level structure (lead sentences, unity, transitions) and document architecture (ordering, section handoffs, narrative arc) and produces a prioritized restructuring plan. |
| `/writing-editor [file]` | Multi-agent line editor that tightens prose, cuts jargon and filler, and removes AI-writing tells. |
| `/extract-pdf-comments <pdf or dir>` | Extracts highlighted text and attached notes from annotated PDFs (e.g., co-author or reviewer markups of a compiled draft) into a markdown file per PDF, organized by page. |
