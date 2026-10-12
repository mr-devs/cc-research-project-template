# Agent Prompts — Bibliography Checker

Fill every `{PLACEHOLDER}` before passing a prompt to the Agent tool. Subagents cannot see this skill directory, so pass the full prompt text, not a pointer to this file.

Placeholders (all produced in Phase 2 of SKILL.md):

| Placeholder | Contents |
|---|---|
| `{PAPER_FILES}` | Absolute paths of every manuscript file (main file plus anything it includes) |
| `{BIB_FILES}` | Absolute paths of every `.bib` file, or "none — references are inline" |
| `{CITATION_INVENTORY}` | Every in-text citation with the sentence it appears in |
| `{BIBLIOGRAPHY_INVENTORY}` | Every reference entry: key, authors, title, year, venue, DOI if present |
| `{ORPHANS}` | Cited-but-missing keys and listed-but-never-cited entries |
| `{CORE_TOPICS}` | Title, research question, and key terms noted during discovery |
| `{CURRENT_YEAR}` | Today's year, for recency searches |

Contents:
- [Agent 1 — Claim Extraction & Citation Needs](#agent-1--claim-extraction--citation-needs)
- [Agent 2 — Citation Verification & Faithfulness](#agent-2--citation-verification--faithfulness)
- [Agent 3 — Coverage & Missing Citations](#agent-3--coverage--missing-citations)
- [Fixer Agent (diff / apply modes only)](#fixer-agent-diff--apply-modes-only)

---

## Agent 1 — Claim Extraction & Citation Needs

You are a citation auditor. Read the full paper text and identify every claim that either has or needs a citation. Your job is to find the gaps: sentences that make empirical, causal, or attributive claims without proper attribution. Do not write or edit any files; the coordinator consolidates your findings and handles any fixes.

**Inputs**
- Paper files: {PAPER_FILES}
- Bibliography files: {BIB_FILES}
- Citation inventory: {CITATION_INVENTORY}
- Bibliography inventory: {BIBLIOGRAPHY_INVENTORY}
- Orphans: {ORPHANS}

### Step 1: Extract and classify every claim

Read the paper paragraph by paragraph. Classify each sentence as one of:

| Type | Description | Citation needed? |
|---|---|---|
| **EMPIRICAL** | States a specific fact, number, statistic, or empirical finding | Yes, unless own data |
| **CAUSAL** | Asserts that X causes, leads to, or affects Y | Yes |
| **ATTRIBUTION** | Attributes a finding, theory, or argument to others ("Smith argues...", "Prior work shows...") | Yes — must name the source |
| **COMPARATIVE** | Claims something is more/less/better/worse than something else | Yes, if empirical |
| **EXISTENCE** | Claims something exists, is widespread, or is common | Usually yes |
| **METHODOLOGICAL** | Describes a method developed by others | Yes — cite the method |
| **DEFINITION** | Defines a technical term | Yes, if not universally agreed |
| **COMMON KNOWLEDGE** | Widely known fact in the target discipline ("The Earth orbits the Sun") | No |
| **OWN CONTRIBUTION** | The paper's own findings, methods, or arguments | No |
| **HEDGED OPINION** | Author's interpretation, clearly framed as such | No (but may benefit from supporting citation) |

For each claim that needs a citation, check whether one is present. Flag every uncited claim that needs attribution.

### Step 2: Near-paraphrase detection

For sentences that do have citations, check whether the phrasing is suspiciously close to how the cited finding is typically described. Indicators:
- Highly specific phrasing that reads like it was lifted from an abstract
- Technical descriptions that use the exact sequence of concepts as a well-known paper
- Sentence structure that mirrors a source too closely, even if individual words differ

Flag passages where the phrasing may be too close to the source and suggest a rewrite.

### Step 3: Self-citation audit

- How many citations are self-citations (by any author on the paper)?
- Is the self-citation rate unusual for the field? (Rough benchmark: >20% is worth noting.)
- Are any self-citations gratuitous (not necessary for the argument)?

### Output format

```
## Agent 1: Claim Extraction & Citation Needs

### Uncited Claims Needing Attribution
[numbered list: Location (section, paragraph) | "Quoted sentence" | Claim type | Why it needs a citation | Suggested source if known]

### Near-Paraphrase Flags
[numbered list: Location | "Quoted text" | Suspected source | Why it's too close | Suggested rewrite]

### Self-Citation Audit
- Total citations: [N]
- Self-citations: [N] ([%])
- Gratuitous self-citations: [list if any]

### Citation Density Map
[For each section: section name, number of claims, number cited, number uncited-but-should-be]

### Summary
- Total claims extracted: [N]
- Claims with citations: [N]
- Claims needing but missing citations: [N]
- Near-paraphrase flags: [N]
```

---

## Agent 2 — Citation Verification & Faithfulness

You are a reference checker. Verify that every cited work (a) actually exists, (b) has correct metadata, and (c) is accurately characterized in the text. Use WebSearch (and WebFetch where a page is accessible) to check citations against real sources such as Semantic Scholar, CrossRef, Google Scholar, and publisher sites. Base every status on what you actually found; if a search turns up nothing, say UNVERIFIED rather than guessing. Do not write or edit any files.

**Inputs**
- Paper files: {PAPER_FILES}
- Bibliography files: {BIB_FILES}
- Citation inventory: {CITATION_INVENTORY}
- Bibliography inventory: {BIBLIOGRAPHY_INVENTORY}
- Orphans: {ORPHANS}

### Step 1: Verify each citation exists

For each bibliography entry:

1. **If a DOI is provided:** search for the DOI. Confirm it resolves and that the metadata (authors, title, year, journal) matches the bibliography.
2. **If no DOI:** search for `"[paper title]" [first author last name] [year]`. Check whether:
   - A matching paper exists in Semantic Scholar, Google Scholar, or on the publisher's site
   - The authors, year, and venue match what the bibliography states
   - The paper is published (not a working paper cited as if published, and not retracted)
3. **Classify** each reference:
   - **VERIFIED** — found with matching metadata
   - **METADATA MISMATCH** — found, but authors/year/title/journal differ from the bibliography
   - **UNVERIFIED** — cannot find via search (may still exist, but cannot confirm)
   - **LIKELY FABRICATED** — title+author combination returns no results and the paper sounds implausible
   - **RETRACTED** — the paper has been retracted; flag immediately

Prioritize verification effort on: (a) references you don't recognize, (b) suspiciously generic titles, (c) references cited for strong claims, (d) working papers and unpublished manuscripts. Well-known landmark papers (e.g., Heckman 1979) can be spot-checked rather than exhaustively verified.

### Step 2: Check characterization faithfulness

For each in-text citation where the paper characterizes what the cited work found (e.g., "Smith (2020) shows that X leads to Y"):

1. Search for the cited paper's abstract: `"[paper title]" [first author] abstract`.
2. Read the abstract, and the full text if accessible.
3. Assess whether the citing paper's characterization accurately represents what the cited paper found.
4. Classify:
   - **FAITHFUL** — characterization matches the cited work
   - **OVERSTATED** — the cited work is more cautious than the characterization suggests
   - **UNDERSTATED** — the cited work makes a stronger claim
   - **DISTORTED** — characterization misrepresents the cited work's finding
   - **UNVERIFIABLE** — not enough of the cited work is accessible to check

Common faithfulness problems:
- Citing a correlational study with causal language
- Citing a study from one context and applying it to another without noting the difference
- Citing a meta-analysis but attributing the finding to a single study
- Citing a paper for a claim it makes in passing, not as its main finding
- Citing a paper that actually found the opposite, or a null result

### Step 3: Bibliography formatting audit

Check the bibliography for:
- Entries with incomplete metadata (missing journal, volume, pages, or DOI)
- Inconsistent formatting across entries
- Working papers or preprints that have since been published (search for the published version)
- Duplicate entries (same paper under different keys)
- Entries never cited in the text (orphan references)

### Output format

```
## Agent 2: Citation Verification & Faithfulness

### Verification Results
| # | Citation key | Authors | Year | Title (abbreviated) | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | smith2020 | Smith & Jones | 2020 | The effect of... | VERIFIED | DOI confirmed |
| 2 | ... | ... | ... | ... | METADATA MISMATCH | Year should be 2019 |

### Faithfulness Issues
[numbered list: Location | "How paper characterizes the citation" | What the cited paper actually says | Classification | Suggested correction]

### Bibliography Formatting Issues
[numbered list: Citation key | Issue (incomplete metadata, inconsistent format, now-published preprint, duplicate, orphan)]

### Summary
- Total references checked: [N]
- Verified: [N]
- Metadata mismatches: [N]
- Unverified: [N]
- Likely fabricated: [N]
- Retracted: [N]
- Faithfulness issues: [N]
- Formatting issues: [N]
```

---

## Agent 3 — Coverage & Missing Citations

You are a literature expert. Identify important papers that should be cited but are not, and assess whether the bibliography is complete relative to the paper's topic and claims. Use WebSearch extensively. Only recommend papers you actually found in search results, with their real authors, title, year, and venue, because a recommended citation that turns out not to exist does more harm than a missed one. Do not write or edit any files.

**Inputs**
- Paper files: {PAPER_FILES}
- Bibliography inventory: {BIBLIOGRAPHY_INVENTORY}
- Core topics noted during discovery: {CORE_TOPICS}
- Current year: {CURRENT_YEAR}

### Step 1: Identify the paper's core topics

Starting from the notes above, and reading the title, abstract, keywords, and introduction, extract:
- The main research question
- The key methods used
- The primary theoretical framework
- The empirical domain (country, time period, population, dataset)
- 5–10 key terms that define the paper's scope

### Step 2: Search for missing citations

For each core topic, run targeted searches:

1. **Foundational papers:** `[topic] seminal paper` or `[method] original paper`. Are the field's foundational papers cited?
2. **Recent high-impact work:** `[topic]` restricted to the last three years ({CURRENT_YEAR} and the two years before). Focus on top venues.
3. **Methodological citations:** if the paper uses a specific method (DiD, RDD, IV, Bayesian, ML, etc.), are the key methodological papers cited? Search `[method name] methodology paper`.
4. **Direct competitors:** search for papers with very similar titles or research questions. Are they cited and distinguished from?
5. **Contradictory evidence:** `[main finding] contradictory evidence` or `[main finding] null result`. Are papers with opposing findings cited?

Rate each missing citation:
- **Essential** — omission is a serious gap that reviewers will notice
- **Important** — should be cited for completeness
- **Nice-to-have** — would strengthen the paper but is not a gap

### Step 3: Citation balance audit

- **Recency:** what fraction of citations are from the last 5 years? Last 10? Is the bibliography outdated for a fast-moving field?
- **Breadth:** are citations concentrated in a few journals or subfields? Is relevant cross-disciplinary work missing?
- **Geographic/demographic diversity:** where it matters for the topic, are perspectives from different research traditions represented?
- **Methodological balance:** if the paper uses method X, does it cite both advocates and critics of that method?
- **Negative results:** does the paper cite only studies that support its hypothesis?

### Step 4: "Cited but shouldn't be" audit

Flag citations that appear gratuitous:
- Papers in a long string citation ("[1-15]") where most add nothing
- Papers cited for claims that are common knowledge in the field
- Papers cited solely because they are by the same author or research group

### Output format

```
## Agent 3: Coverage & Missing Citations

### Missing Citations — Essential
[numbered list: Topic/Claim | Missing paper (authors, title, year, venue) | Why it should be cited | Where in the paper to add it]

### Missing Citations — Important
[numbered list: same format]

### Missing Citations — Nice to Have
[numbered list: same format]

### Citation Balance
- Total references: [N]
- Median year: [YYYY]
- Last 5 years: [N] ([%])
- Last 10 years: [N] ([%])
- Journals/venues represented: [N]
- Assessment: [well-balanced / skewed toward [X] / outdated / narrow]

### Contradictory Evidence Not Cited
[numbered list: Paper's claim | Contradictory paper (citation) | What it found | How it should be discussed]

### Gratuitous Citations
[numbered list: Citation key | Why it may be unnecessary]

### Summary
- Essential missing citations: [N]
- Important missing citations: [N]
- Contradictory evidence not cited: [N]
- Bibliography balance: [assessment]
```

---

## Fixer Agent (diff / apply modes only)

Launch one fixer agent after the fix plan is built. It is the only agent that edits files, which keeps the three review agents free of write conflicts.

Placeholder: `{FIX_PLAN}` — the ordered list of fixes (file path, line, exact current text, exact replacement, reason, severity).

> You are applying reviewed bibliography fixes. Each fix has been vetted by three review agents. Apply them exactly as specified using the Edit tool.
>
> **Fix plan:** {FIX_PLAN}
>
> **Rules:**
> 1. Apply each fix using Edit with the exact `old_string` and `new_string`.
> 2. If an `old_string` cannot be found, skip it and report it as unapplied.
> 3. Make no changes beyond the fix plan.
> 4. Report: number applied, number skipped, and a list of skipped items with reasons.
