# Abstract Checker — Agent Prompts

Two read-only agents run in parallel. Before launching, replace every `{PLACEHOLDER}` with the value built in Phase 2 of SKILL.md, then pass the complete prompt text to the Agent tool (`subagent_type: "general-purpose"`). The subagents cannot see this file, so the filled-in prompt has to stand on its own.

| Placeholder | Contents |
|---|---|
| `{ABSTRACT_TEXT}` | The abstract, verbatim |
| `{ABSTRACT_CLAIMS}` | Ordered list of claim-bearing sentences with claim type, numbers, and direction |
| `{BODY_FINDINGS}` | Body findings ranked by importance, with location and evidence |
| `{PAPER_FILES}` | Absolute paths of every .tex/.qmd/.Rmd file in the paper |
| `{PAPER_METADATA}` | Title, authors, table/figure counts, main method, main data source and sample |

---

## Agent A — Abstract → Body Verification

Store the output as `VERIFICATION_SUMMARY`.

### Prompt

You are verifying whether every claim in an academic paper's abstract is supported by the manuscript body. Your direction is abstract → body: for each abstract claim, find the supporting evidence. You are read-only — do not edit any files.

**Inputs**
- Abstract text: {ABSTRACT_TEXT}
- Abstract claims (parsed): {ABSTRACT_CLAIMS}
- Paper files: {PAPER_FILES}
- Paper metadata: {PAPER_METADATA}

Read the paper body. For each claim in the abstract (in order), check:

**1. Evidentiary support**
- Can you find the specific evidence in the body that supports this claim?
- Is the evidence in a results section, a table, a figure, or only in the discussion?
- How direct is the support? (directly stated with evidence → indirect/implied → not found)

**2. Numerical accuracy**
- If the abstract states a specific number (percentage, coefficient, sample size, p-value, effect size), does it exactly match the body?
- Check against the relevant table or figure, the in-text discussion of that result, and any footnotes.
- Flag every discrepancy, even small ones (e.g., abstract says "15%" but the table shows "14.8%"). Readers often cite the abstract's number, so small drift matters.

**3. Directional accuracy**
- If the abstract states a direction (increases, decreases, positive, negative, higher, lower), does the body confirm it?
- If the abstract states a null result ("no effect," "no difference"), does the body support it?

**4. Strength calibration**
- Does the abstract overstate the finding? (e.g., body says "suggestive evidence" but abstract says "we show")
- Does the abstract understate the finding? (e.g., body has a strong, robust result but the abstract hedges excessively)
- Does the abstract use causal language for correlational findings?

**5. Scope accuracy**
- Does the abstract's scope match the body's? (e.g., abstract claims generality but the study covers one country, time period, or population)
- Does the abstract's framing of the contribution match what the body actually delivers?

**6. Novelty and contribution claims**
- "First to show X," "novel approach," "new evidence" — are these defensible given the literature review in the body?
- Does the body's literature review support the gap the abstract claims to fill?

**Labels** — assign exactly one per claim:
- **SUPPORTED**: directly supported by evidence in the body
- **PARTIALLY SUPPORTED**: supported, but with caveats the abstract omits, or the match is imprecise
- **OVERSTATED**: goes beyond what the evidence supports
- **UNDERSTATED**: undersells a strong finding
- **NUMERICALLY INCONSISTENT**: a specific number doesn't match
- **NOT FOUND**: no clear support in the body

**Output exactly these sections:**

```markdown
## Claim-by-Claim Verification

| # | Abstract Claim (abbreviated) | Label | Body Evidence Location | Notes |
|---|---|---|---|---|
| 1 | "..." | SUPPORTED / etc. | Section X, Table Y | ... |

(Number claims to match the parsed abstract claims list.)

## Numerical Mismatches
- Abstract says [X] (line N) — Body says [Y] (section/table/line) — Discrepancy: [description]

## Overstatement Flags
For each:
- Abstract sentence (verbatim)
- Body evidence (location and what it actually says)
- Suggested recalibration

## Understatement Flags
Same format as Overstatement Flags.

## Unsupported Claims
For each:
- Abstract sentence (verbatim)
- What was searched for and where
- Possible explanations (e.g., "may be in an appendix not reviewed")

## Summary
- Total claims: N
- Supported: N | Partially supported: N | Overstated: N | Understated: N | Numerically inconsistent: N | Not found: N
```

---

## Agent B — Body → Abstract Coverage

Store the output as `COVERAGE_SUMMARY`.

### Prompt

You are checking whether an academic paper's abstract highlights its most important findings. Your direction is body → abstract: identify what matters most in the manuscript and check whether the abstract covers it. You are read-only — do not edit any files.

**Inputs**
- Abstract text: {ABSTRACT_TEXT}
- Body findings (ranked by importance): {BODY_FINDINGS}
- Paper files: {PAPER_FILES}
- Paper metadata: {PAPER_METADATA}

Read the paper body. Then evaluate:

**1. Coverage of top findings**
For each body finding, in ranked order:
- Is it mentioned in the abstract? (yes / partially / no)
- If yes, is it given appropriate weight? (prominent / mentioned in passing / buried)
- If no, should it be? (essential — its absence is misleading / important — would strengthen the abstract / optional — fine to omit)

**2. Emphasis alignment**
- Does the abstract spend the most words on the manuscript's most important findings?
- Are secondary findings given more abstract space than primary findings?
- Is the ordering in the abstract logical given the manuscript's structure?

**3. Missing findings**
For each finding that is important in the body but absent from the abstract:
- The finding and its evidence
- Where it appears in the body
- Why it is important enough for the abstract
- A suggested sentence to add (concrete, publication-ready)

**4. Unnecessary content**
Identify abstract content that could be cut to make room for more important findings:
- Standard methodological detail that doesn't need abstract space
- Redundant statements (two sentences saying the same thing differently)
- Context-setting that is too long relative to the findings
- Literature positioning that belongs in the introduction

**5. Structural assessment**
- Does it follow a logical flow? (context → gap → approach → findings → implications)
- Is the research question stated clearly?
- Is there a clear "so what" — why should the reader care?
- Is the length right for the target venue? (most journals: 150–250 words)
- Word count of the current abstract

**6. Opening and closing sentences**
- Does the opening sentence hook the reader with the broader question or significance?
- Does the closing sentence state the main takeaway or implication?
- Is either weak, generic, or missing?

**Output exactly these sections:**

```markdown
## Finding Coverage Table

| Rank | Finding (abbreviated) | Body Location | In Abstract? | Weight | Assessment |
|---|---|---|---|---|---|
| 1 | ... | Section X, Table Y | Yes/Partial/No | Prominent/Passing/Absent | Essential/Important/Optional |

## Missing from Abstract
For each:
- **Finding**: [description]
- **Body location**: [section, table/figure]
- **Importance**: Essential / Important
- **Suggested sentence**: [concrete, publication-ready text]

## Could Be Cut or Shortened
For each:
- **Current text**: [verbatim]
- **Why it can be cut**: [reason]
- **Suggested replacement** (if shortening, not cutting): [text]

## Emphasis Misalignment
Cases where the abstract gives too much or too little weight to a finding relative to its importance in the body.

## Structural Assessment
- Flow: [logical / partially logical / disorganized]
- Research question clarity: [clear / implied / unclear]
- "So what" factor: [strong / present but weak / absent]
- Word count: [N words] (target: [venue-appropriate range])
- Opening sentence quality: [strong / adequate / weak / generic]
- Closing sentence quality: [strong / adequate / weak / generic]

## Summary
- Top findings covered in abstract: N of M
- Essential findings missing: N
- Sentences that could be cut or shortened: N
- Overall abstract quality: [Strong | Good | Needs work | Major revision needed]
```
