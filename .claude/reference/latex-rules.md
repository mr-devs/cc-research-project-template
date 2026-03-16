# LaTeX Rules Reference

## LaTeX Section Structure

```latex
\section*{Section Title}
\label{sec:concise_name}

Opening paragraph establishing the section's focus and core claim~\cite{Key1}.

Development paragraphs expand on specific points with supporting evidence~\cite{Key2,Key3}.

Concluding paragraph synthesizes and transitions to next section.
```

## Citation Format (natbib)

| Type          | Syntax              | Output            |
| ------------- | ------------------- | ----------------- |
| Parenthetical | `~\cite{Key}`       | [1]               |
| Narrative     | `\citet{Key}`       | Author et al. [1] |
| Multiple      | `~\cite{Key1,Key2}` | [1,2]             |

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

## Paragraph Guidelines

- **Topic sentence:** Connect to section's core claim
- **Development:** 3-5 sentences expanding with evidence
- **Citations:** 1-2 per paragraph typical; avoid 5+ unless surveying literature
- **Transitions:** Final sentence should bridge to next paragraph

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
