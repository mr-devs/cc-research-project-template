# Abstract Checker — Report Template

Write the report to the current working directory as `abstract_check_[YYYY-MM-DD].md` (today's date). Fill every bracketed field. Where a list section has no entries, write "None found" rather than deleting the heading, so readers can see the check was run.

Conditional sections:
- **Fixes Applied** and **Revised Abstract** — only when `FIX_MODE` is `review`, `diff`, or `apply` (Revised Abstract only if at least one change was applied).
- **Recommended Abstract** — only when `FIX_MODE` is `report`.

```markdown
# Abstract Check Report: [Paper Title]

*Reviewed: [today's date] | Paper: [PAPER_FILE] | Abstract: [line range] | Word count: [N]*

---

## Overall Assessment

[3-5 sentences. How well does the abstract represent the paper? Lead with strengths. Then the most important gap or mismatch. End with overall quality characterization.]

**Abstract quality**: [Strong | Good | Needs work | Major revision needed]

---

## Claim Verification (Abstract → Body)

### Claim-by-Claim Results

| # | Abstract Claim | Verdict | Body Evidence | Notes |
|---|---|---|---|---|
| 1 | ... | SUPPORTED | ... | ... |

### Numerical Mismatches

[List, or "None found"]

### Overstatement Flags

[List, or "None found"]

### Unsupported Claims

[List, or "None found"]

**Summary**: N of M claims fully supported, N partially supported, N overstated, N numerically inconsistent, N not found.

---

## Finding Coverage (Body → Abstract)

### Coverage Table

| Rank | Finding | In Abstract? | Weight | Should Include? |
|---|---|---|---|---|
| 1 | ... | Yes/No | ... | Essential/Important/Optional |

### Missing from Abstract

[Findings that should be there, with suggested sentences]

### Could Be Cut or Shortened

[Abstract content that could be trimmed]

### Emphasis Misalignment

[Where weight doesn't match importance]

**Summary**: N of M top findings covered, N essential findings missing, N sentences could be cut.

---

## Structural Assessment

- Flow: [assessment]
- Research question clarity: [assessment]
- "So what" factor: [assessment]
- Opening sentence: [assessment]
- Closing sentence: [assessment]
- Word count: [N] (target: [range])

---

## Fixes Applied

| # | Change Type | Current Text | Revised Text | Reason | Status |
|---|---|---|---|---|---|
| 1 | Revise / Cut / Add | ... | ... | ... | Applied / Skipped |

**Summary:** X changes applied, Y skipped.

---

## Revised Abstract

> [Final abstract as it stands after edits]

---

## Recommended Abstract

> [Recommended revised abstract for the author to consider]

**Changes from original:**
1. [Change 1 and why]
2. [Change 2 and why]
3. ...

---

## Priority Action Items

**CRITICAL** (abstract misrepresents the paper):
1. ...

**MAJOR** (abstract omits important content or overstates):
2. ...

**MINOR** (polish):
3. ...

---

## Appendix: Agent Outputs

### A. Verification (Abstract → Body)
[Paste VERIFICATION_SUMMARY]

### B. Coverage (Body → Abstract)
[Paste COVERAGE_SUMMARY]
```
