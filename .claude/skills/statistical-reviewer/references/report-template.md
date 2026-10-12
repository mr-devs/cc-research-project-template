# Report Template

Save the consolidated report as `STATISTICAL_REVIEW_[YYYY-MM-DD].md` (today's date) in the current working directory. Preserve each agent's internal structure when pasting its output into sections 1–4.

```markdown
# Statistical Review Report

**Paper**: [Title]
**Authors**: [Authors]
**Date**: [Today's date]
**Journal standard**: [TARGET_JOURNAL or "Leading Field Journal"]
**Statistical perspective**: [PERSPECTIVE — full name and one-line description]

---

## Executive Summary

[4–6 sentences: What the paper does, the main statistical approach, the most critical
statistical issue, and overall assessment of statistical rigor.]

**Statistical rigor assessment**: [Strong | Adequate | Needs work | Serious concerns]

---

## 1. Statistical Methods & Assumptions

[Agent 1 output, preserving its structure]

---

## 2. Effect Sizes & Reporting Quality

[Agent 2 output]

---

## 3. Causal Inference & Research Design

[Agent 3 output]

---

## 4. Perspective Review — [PERSPECTIVE]

[Agent 4 output, or "Skipped (no perspective requested)" if Agent 4 was not launched]

---

## Priority Action Items

Apply this triage hierarchy across agents: causal identification failures (Agent 3) >
numerical inconsistencies (Agent 2) > methods/assumption violations (Agent 1) >
perspective-specific concerns (Agent 4). Within each agent: Critical > Major > Minor.

**CRITICAL** (may invalidate conclusions):
1. ...
2. ...
3. ...

**MAJOR** (weaken conclusions or will be raised by reviewers):
4. ...
5. ...
6. ...

**MINOR** (best-practice improvements):
7. ...
8. ...
9. ...

---

## Fixes Applied

*Include this section only if FIX_MODE is review, diff, or apply. Omit if report.*

| # | File | Fix | Severity | Status |
|---|---|---|---|---|
| 1 | ... | Short description | CRITICAL/MAJOR/MINOR | Applied / Skipped / Failed |

**Summary:** X fixes applied, Y skipped, Z failed.

---

## Statistical Checklist

| Item | Status | Notes |
|---|---|---|
| Appropriate test selection | ✓/✗/partial | |
| Assumptions checked | ✓/✗/partial | |
| Power analysis | ✓/✗/partial | |
| Multiple comparisons addressed | ✓/✗/partial/N/A | |
| Effect sizes reported | ✓/✗/partial | |
| Confidence intervals reported | ✓/✗/partial | |
| P-values internally consistent | ✓/✗/partial | |
| Causal claims match design | ✓/✗/partial/N/A | |
| Sensitivity analysis | ✓/✗/partial | |
| Software & code documented | ✓/✗/partial | |
| Pre-registered | ✓/✗/unknown | |
| Data available | ✓/✗/partial | |
```
