# Report Template

Read this in Phase 5. Save the report to the current working directory as `BIBLIOGRAPHY_CHECK_[YYYY-MM-DD].md`, using today's date. Paste each agent's output into its numbered section. Write the Executive Summary, Priority Action Items, and both Quick Reference sections yourself from the combined findings.

```markdown
# Bibliography Check Report

**Paper**: [Title]
**Authors**: [Authors]
**Date**: [Today's date]
**Citation style**: [CITE_STYLE]
**Total references**: [N]
**Total in-text citations**: [N]

---

## Executive Summary

[4–6 sentences: How many issues found, most critical problems, overall
bibliography quality assessment.]

**Bibliography health**: [Clean | Minor issues | Needs attention | Serious problems]

---

## 1. Claim Extraction & Citation Needs

[Agent 1 output]

---

## 2. Citation Verification & Faithfulness

[Agent 2 output]

---

## 3. Coverage & Missing Citations

[Agent 3 output]

---

## Priority Action Items

Triage hierarchy: fabricated/retracted citations (Agent 2) > distorted characterizations
(Agent 2) > uncited empirical claims (Agent 1) > essential missing citations (Agent 3) >
near-paraphrase issues (Agent 1) > metadata mismatches (Agent 2) > important missing
citations (Agent 3) > formatting issues (Agent 2) > balance concerns (Agent 3).

**CRITICAL** (fix before submission):
1. ...
2. ...
3. ...

**MAJOR** (reviewers will likely flag):
4. ...
5. ...
6. ...

**MINOR** (improves bibliography quality):
7. ...
8. ...
9. ...

---

## Fixes Applied

*Include this section only if a fix mode (review, diff, or apply) ran. Omit it in the default report mode.*

| # | File | Fix | Severity | Status |
|---|---|---|---|---|
| 1 | ... | Short description | CRITICAL/MAJOR/MINOR | Applied / Skipped / Failed |

**Summary:** X fixes applied, Y skipped, Z failed.

---

## Quick Reference: Citations to Add

[Consolidated list of all citations the agents recommend adding, with
full bibliographic information and where in the paper to insert them.
Format each as a ready-to-paste BibTeX entry if the paper uses BibTeX.]

---

## Quick Reference: Citations to Fix

[Consolidated list of all citations needing correction — metadata fixes,
characterization rewrites, formatting corrections. For each, provide
the current text and the corrected version.]
```
