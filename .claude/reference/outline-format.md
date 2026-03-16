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

### Artifact Pointers (Optional)

For Results and Methods sections, link to project files that ground the writing in actual outputs:

- Format: `[artifact: path/to/file - brief description]`
- Nested under the point they support
- Paths relative to project root

Example:
- Distribution of low-credibility sharing is heavily right-skewed
  - [artifact: results/reports/sharing_stats.txt - descriptive statistics]
  - [artifact: code/analysis/distribution_analysis.py - analysis code]

## Example

```markdown
# Partisan Asymmetries in Online Misinformation Sharing: Evidence from a Large-Scale Observational Study

**Target venue:** PNAS Research Article
**Length constraints:** ~6 pages (~5,500 words)

---

## Introduction

**Core claim:**
Despite growing concern about misinformation, the relationship between political identity and susceptibility to sharing low-credibility content remains empirically contested.

### Key dynamics / points

- Prior work has produced conflicting estimates of partisan asymmetry
  - Guess2019LessMainstream - Survey evidence suggesting limited asymmetry in news consumption
  - Grinberg2019FakeNews - Twitter data showing concentrated sharing among a small subset of users
- Gap between lab-based and observational evidence
  - Pennycook2021Shifting - Attention-based interventions reduce sharing intentions in experiments
- Contribution: large-scale behavioral data linking sharing behavior to credibility ratings
  - Benkler2018NetworkPropaganda - Structural asymmetry argument requiring behavioral test

## Results

**Core claim:**
Users sharing low-credibility URLs are concentrated on the political right, but the effect is driven by a small, highly active subset of accounts.

### Key dynamics / points

- Distribution of low-credibility sharing is heavily right-skewed
  - [artifact: results/reports/sharing_stats.txt - descriptive statistics on sharing distribution]
  - [artifact: code/analysis/distribution_analysis.py - analysis code]
- Partisan gap persists after controlling for account age and follower count
  - Vosoughi2018SpreadTrue - Falsehoods spread faster; baseline comparison needed
  - [artifact: results/reports/regression_results.txt - regression table]
- Bot activity does not account for the observed asymmetry

## Discussion

**Core claim:**
Findings support a structurally asymmetric but narrowly concentrated pattern of misinformation sharing with implications for platform intervention design.

### Key dynamics / points

- Consistency with network propaganda hypothesis
- Limitations: platform-specific, cross-sectional design
- Implications for targeted versus broad interventions

## Materials and Methods

**Core claim:**
Observational design using a matched sample of Twitter users with credibility ratings from independent fact-checkers.

### Key dynamics / points

- Data source and collection window
  - [artifact: code/data_collection/collect_tweets.py - data collection script]
  - [artifact: data/processed/user_sample.csv - final matched sample]
- Credibility rating methodology
  - Pennycook2019LazyNot - Reliance on intuition vs. analytical thinking as confound
- Statistical modeling approach
  - [artifact: code/analysis/model.py - statistical modeling code]
```
