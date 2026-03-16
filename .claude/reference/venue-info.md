# Venue Information Reference

## Target Venue

PNAS (Proceedings of the National Academy of Sciences)

## Audience

Broad scientific community — not just domain specialists. Define all acronyms on first use. Avoid excessive jargon; when technical terms are necessary, briefly explain them.

## Article Type

**Research Article** — original empirical work. Not a Perspective, Commentary, or Review.

## Standard Section Structure

1. **Title** — concise, informative, accessible to non-specialists
2. **Significance Statement** (≤120 words, required) — non-technical; written for a general scientific audience; conveys why this work matters to someone outside your field
3. **Abstract** (≤250 words) — summarizes purpose, methods, findings, and implications
4. **Introduction** — 3–5 paragraphs; contextualize for broad audience; end with a clear statement of the contribution and paper structure
5. **Results** — empirical findings; use subheadings; present findings before interpretation; name figures/tables inline
6. **Discussion** — open with main finding; situate relative to prior work; address limitations; close with broader implications
7. **Materials and Methods** — reproducibility-focused; detail computational methods, data sources, and code availability
8. **Acknowledgments / Data Availability**

## Length

~6 pages (~5,000–6,500 words including references)

## Tone and Voice

- Precise, direct, and accessible
- Active voice preferred
- Minimize hedging where evidence is strong; hedge appropriately where it is not
- Avoid unnecessary qualifiers and filler phrases

## Section-Specific Guidance

### Significance Statement

- Written for a non-specialist reader
- Conveys "why does this matter to someone outside your field?"
- No citations; no jargon without explanation
- ≤120 words

### Introduction

- 3–5 paragraphs
- Open by contextualizing the broader problem for a general scientific audience
- Summarize relevant prior work concisely
- End with a clear statement of the contribution and an overview of the paper structure

### Results

- Present findings objectively; defer interpretation to Discussion
- Use descriptive subheadings
- Reference figures and tables inline (e.g., "Fig. 1A shows...")
- Report effect sizes, confidence intervals, and significance levels as appropriate

### Discussion

- Open with the main finding restated in plain language
- Situate findings relative to prior literature
- Address limitations honestly
- Close with broader implications for the field or society

### Materials and Methods

- Sufficient detail to allow independent reproduction
- Specify software, packages, and versions
- Include data availability and code availability statements

### Rules

- Never introduce an acronym without first defining it. Only do that once.
- Always use tilde (`~`) before `\cite{}` for non-breaking space
- Place citations before punctuation: `claim~\cite{Key}.`
- Use `\citet{}` when author is grammatical subject: `\citet{Key} demonstrated...`
- For missing citations, insert: `(CITATION NEEDED)`

## Hedged Language

Use hedged language unless causal relationships are clearly established.

| Instead of          | Use                        |
| ------------------- | -------------------------- |
| "influences"        | "may influence"            |
| "proves that"       | "suggests that"            |
| "supports"          | "can support"              |
| "causes"            | "is often associated with" |
| "shows"             | "indicates"                |
| "is" (strong claim) | "appears to be"            |

## Common Patterns

### Introducing evidence

```latex
Recent work suggests that...~\cite{Key}.
Empirical studies indicate...~\cite{Key1,Key2}.
\citet{Key} found that...
```

### Acknowledging uncertainty

```latex
While evidence remains limited, initial findings suggest...
These results should be interpreted cautiously, as...
Further research is needed to establish...
```

### Synthesizing multiple sources

```latex
Across multiple studies~\cite{Key1,Key2,Key3}, a consistent pattern emerges...
Several lines of evidence converge on...~\cite{Key1,Key2}.
```
