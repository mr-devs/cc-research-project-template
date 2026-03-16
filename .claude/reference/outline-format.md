# Outline Format Reference

## File Location

`paper/outline.md`

## Structure

```markdown
# [Document Title]

**Target venue:** [Journal/Conference name or "Not specified"]
**Length constraints:** [Word/page limit or "None specified"]

---

## Section Title

**Core claim:**
[One sentence thesis for this section]

### Key dynamics / points

- Point 1
  - AuthorYearKey - [One sentence on relevance]
- Point 2
  - AuthorYearKey - [One sentence on relevance]
- Point 3

## Next Section Title

**Core claim:**
[One sentence thesis]

### Key dynamics / points

- Point 1
- Point 2
```

## Guidelines

### Header Metadata

- **Target venue:** Journal, conference, or magazine name if known
- **Length constraints:** Word count, page limit, or format requirements

### Section Titles

- Use descriptive titles only (no numbering)
- Follow standard academic headers when appropriate (Introduction, Methods, Results, Discussion, Conclusion)

### Core Claims

- One sentence thesis per section
- Should directly support the document's main argument

### Key Points

- Bullet list of main arguments, dynamics, or evidence
- Keep concise but specific

### Citation Pointers (Optional)

- Format: `AuthorYearKey - [Brief relevance note]`
- Nested under the point they support
- Keys must match entries in `paper/main.bib`

## Example

```markdown
# AI and the Health Information Journey

**Target venue:** Nature Medicine (Perspective)
**Length constraints:** 3000 words

---

## The AI-Transformed Health Information Ecosystem

**Core claim:**
Generative AI has reconfigured how health information is produced, distributed, interpreted, and acted upon.

### Key dynamics / points

- Shift from retrieval to mediation
  - FernandezPichel2025Evaluating - LLMs now synthesize rather than just retrieve
  - Hopkins2023AIChatbots - Paradigm shift in cancer patient information access
- From episodic to continuous interaction
  - Wardle2025Evolving - Blurs boundaries between care stages
- Authority becoming distributed
  - Sun2024TrustingSearch - Trust dynamics shifting to AI intermediaries
```
