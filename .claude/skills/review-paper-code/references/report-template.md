# Report Template

Read this in Phase 7. Save the report to the current working directory as `code_review_report_[YYYY-MM-DD].md`, using today's date. Fill every bracketed field. Write "None found" rather than deleting an empty subsection, so readers can tell the check ran. Paste the raw agent outputs and the paper summary into the appendix so the user can audit the synthesis.

```markdown
# Code Review Report: [Paper Title]

*Reviewed: [today's date] | Languages: [LANGUAGES] | Depth: [REVIEW_DEPTH] | Domain: [DOMAIN] | Paper: [PAPER_FILE filename] | Code: [CODE_DIR]*

---

## Overall Assessment

[3-5 sentences. Lead with strengths. Then the most important reproducibility, analytical, or alignment issue. End with an overall characterization: e.g., "The codebase is largely reproducible with a few verification items" or "Several issues require attention before the code can be considered a reliable replication package."]

## What's Working Well

- [Specific positive from Agent A]
- [Specific positive from Agent B]
- [Specific positive from Agent C]
- [Additional positives]

---

## Reproducibility and Execution Feasibility

### Reproducibility Checklist

| Check | Status | Details |
|---|---|---|
| Entry point / master script | LABEL | ... |
| Run order documented | LABEL | ... |
| Relative file paths | LABEL | ... |
| Random seed practice | LABEL | ... |
| Dependency management | LABEL | ... |
| Output files traceable | LABEL | ... |
| Cross-language handoffs | LABEL | ... |
| README / documentation | LABEL | ... |

### Execution Assessment

[Can this code plausibly run on a clean machine? Specific blockers if any.]

### Key Findings

[Top findings from Agent A, condensed]

---

## Data Integrity and Analytical Logic

### Data Processing

[Summary of merge, filter, missing data, variable construction quality from Agent B]

### Statistical Methods

[Summary of estimation, inference, testing quality from Agent B]

### Sensitivity and Robustness

[Which claimed robustness checks exist in code? Which are absent? Untested specification choices?]

### Key Findings

[Top findings from Agent B, condensed]

---

## Paper-Code Alignment

### Design Match

[Summary: does the code implement the research design described in the paper?]

### Results Verification

| Table / Figure | Generating Script | Output File | Status |
|---|---|---|---|
| Table 1 | ... | ... | ... |
| Figure 1 | ... | ... | ... |

### Hardcoded Numbers at Risk

[Numbers in paper prose not traceable to code output]

### Robustness Claim Status

| Claim in Paper | Found in Code? | File | Status |
|---|---|---|---|
| ... | ... | ... | ... |

### Likely Discrepancies

[Items where paper and code point in different directions]

### Items to Verify

[Ambiguous matches worth checking]

---

## Fixes Applied

*Include this section only if a fix mode (review, diff, or apply) ran. Omit it in the default report mode.*

| # | File | Line | Fix | Severity | Status |
|---|---|---|---|---|---|
| 1 | ... | ... | Short description | CRITICAL/MAJOR/MINOR | Applied / Skipped / Failed |

**Summary:** X fixes applied, Y skipped, Z failed.

[If any fixes were skipped or failed, list them with reasons.]

---

## Priority Action Items

Triage hierarchy: data integrity failures > execution blockers > paper-code discrepancies on main results > reproducibility gaps > analytical concerns on secondary results > hardcoded number risks > missing robustness code > code quality.

*If fixes were applied, mark fixed items as "DONE" and focus the action list on remaining items.*

**CRITICAL** (must address — blocks reproducibility or may invalidate main claims):
1. ...

**MAJOR** (should address — likely raised in review or replication):
2. ...

**MINOR** (improves quality):
3. ...

---

## Appendix: Agent Outputs

### A. Reproducibility and Execution Feasibility
[Paste `REPRODUCIBILITY_SUMMARY`]

### B. Data Integrity and Analytical Logic
[Paste `ANALYSIS_SUMMARY`]

### C. Paper-to-Code Mapping and Results Verification
[Paste `MAPPING_SUMMARY`]

### Paper Summary
[Paste `PAPER_SUMMARY`]
```
