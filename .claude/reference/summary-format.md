# Paper Summary Format Reference

## File Naming

- Filename = BibTeX key exactly: `{BibTeXKey}.md`
- BibTeX entry must exist in `paper/main.bib` first (run `/create-bibtex` if needed)

## Directory Structure

Summaries go in `lit_review/paper_summaries/`, mirroring PDF directory structure:

| Source PDF | Summary |
|------------|---------|
| `lit_review/papers/00-background/file.pdf` | `lit_review/paper_summaries/00-background/{key}.md` |
| `lit_review/papers/02-seeking_information/file.pdf` | `lit_review/paper_summaries/02-seeking_information/{key}.md` |

## Summary Template

```markdown
# {Paper Title}

## Metadata
- **Authors:** {Author1, Author2, Author3}
- **Year:** {YYYY}
- **Publication:** {Journal Name / Conference Name / arXiv [Preprint]}
- **DOI:** [{DOI}](https://doi.org/{DOI})
- **BibTeX Key:** `{AuthorYearKeyword}`

## Main Takeaways
- {Most important finding or contribution}
- {Second key finding}
- {Third key finding}
- {Fourth key finding - if applicable}
- {Fifth key finding - if applicable}

## Methodological Approach
- {Study design or primary method}
- {Data sources or sample}
- {Key analytical approach}
- {Additional methods - if applicable}

## Limitations
- {Primary limitation acknowledged by authors}
- {Second limitation}
- {Third limitation - if applicable}
- {Fourth limitation - if applicable}
```

## Section Guidelines

### Metadata
- **Authors**: Comma-separated; for >6 authors use first three + "et al."
- **DOI**: Clickable link if available; otherwise "Not available" + URL if exists
- **BibTeX Key**: Exact key from main.bib in backticks

### Main Takeaways (max 5 bullets)
Prioritize empirical findings over theoretical; include specific numbers when significant; be concise but specific. Focus on relevance to computational social science research questions.

Good: "ChatGPT achieved 85% accuracy on consumer health questions but only 54% on clinical questions."
Avoid: "The paper found interesting results about AI in healthcare." (too vague)

### Methodological Approach (max 4 bullets)
Describe study design, data sources/sample size, tools/frameworks, analysis methods.

Good: "Systematic review of 45 studies following PRISMA guidelines, January 2020–December 2024"

### Limitations (max 4 bullets)
Check paper's limitations section first; include sample size constraints, generalizability issues, methodological and temporal limitations.

Good: "ChatGPT version used (GPT-3.5) may not reflect current capabilities"

## Edge Cases

### Missing DOI
Use `- **DOI:** Not available` and add URL line if available.

### Short Papers/Reports
If paper lacks distinct sections: describe general approach for methodology; note "Not explicitly discussed" for limitations and infer obvious ones.

### Non-Research Papers (Reports, White Papers)
Adapt headers: "Key Findings" → Main Takeaways; "Approach" → Methodology; "Caveats" → Limitations.

### Review Papers
Main takeaways = synthesis findings; Methodology = review protocol (databases, criteria); Limitations = gaps in reviewed literature.

## Example Complete Summary

```markdown
# Evolving Health Information–Seeking Behavior in the Context of Google AI Overviews, ChatGPT, and Alexa

## Metadata
- **Authors:** Claire Wardle, Shaydanay Urbani, Eric Wang
- **Year:** 2025
- **Publication:** Journal of Medical Internet Research
- **DOI:** [10.2196/79961](https://doi.org/10.2196/79961)
- **BibTeX Key:** `Wardle2025Evolving`

## Main Takeaways
- Users employ different mental models when interacting with AI-powered health tools vs traditional search engines
- Trust calibration varies significantly across platforms, with ChatGPT receiving higher initial trust than warranted by accuracy
- Think-aloud protocols revealed users rarely verify AI-generated health information with additional sources
- Demographic factors (age, health literacy) significantly influenced information-seeking strategies

## Methodological Approach
- Qualitative interview study using think-aloud protocol
- 32 participants across diverse age groups and health literacy levels
- Participants completed standardized health information-seeking tasks across three platforms
- Thematic analysis of verbalized thought processes

## Limitations
- Small sample size limits generalizability of findings
- Participants were aware of being observed, potentially affecting natural behavior
- Study conducted in single geographic region (US Northeast)
- AI tool capabilities may have changed since data collection
```
