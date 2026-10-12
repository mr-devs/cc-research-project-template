# Report Templates — Structural Editor

Two templates: the restructuring plan built in Phase 3, and the final report saved in Phase 5.

## Restructuring plan (Phase 3)

```
## RESTRUCTURING PLAN

### Writing context: [WRITING_CONTEXT]

### CRITICAL (breaks argument flow)
R1. [type]: [location] | [description] | Fix: [specific instruction]
R2. ...

### MAJOR (weakens clarity)
R3. ...

### MINOR (polish)
R7. ...

Total findings: X CRITICAL, Y MAJOR, Z MINOR
```

## Final report (Phase 5)

Save to `STRUCTURAL_EDIT_[YYYY-MM-DD].md` in the current working directory.

```markdown
# Structural Edit Report

**Document**: [Title or filename]
**Date**: [Today's date]
**Writing context**: [WRITING_CONTEXT]
**Fix mode**: [FIX_MODE]

---

## Executive Summary

[4–6 sentences covering:
1. Overall structural quality (strong / adequate / needs significant restructuring)
2. The most critical structural problem
3. The pattern-level diagnosis (e.g., "lead sentences consistently bury the point" or "results and discussion are interleaved")
4. Proportion of paragraphs with forecasting leads (X/Y = Z%)
5. Whether the reverse outline reads as a coherent argument
6. Recommended scope of revision (minor touch-ups / targeted restructuring / major reorganization)]

---

## 1. Paragraph-Level Structure

[Agent A output, preserving its tables and format]

---

## 2. Section & Document Architecture

[Agent B output, preserving its format]

---

## Restructuring Plan

[From Phase 3 — the consolidated, deduplicated, prioritized plan]

### Triage hierarchy

Information placement errors > reverse outline gaps > section handoff failures >
paragraph ordering problems > lead sentence issues > transition problems >
heading issues > given-new flow breaks > length flags.

**CRITICAL** (X items):
1. ...

**MAJOR** (Y items):
4. ...

**MINOR** (Z items):
7. ...

---

## Fixes Applied

*Include only if FIX_MODE is review, diff, or apply. Omit for report.*

| # | File | Line | Fix | Severity | Status |
|---|---|---|---|---|---|
| 1 | ... | ... | Short description | CRITICAL/MAJOR/MINOR | Applied / Skipped / Failed |

**Summary:** X fixes applied, Y skipped, Z failed.

---

## Structural Health Summary

| Metric | Value |
|---|---|
| Paragraphs with forecasting leads | X / Y (Z%) |
| Paragraphs with unity issues | X |
| Given-new flow breaks | X |
| Mechanical transitions | X |
| Missing transitions | X |
| Information placement errors | X |
| Heading hierarchy issues | X |
| Reverse outline coherence | Coherent / Partial gaps / Significant gaps |

---

## Recommended Next Steps

[Ordered list of the 3–5 most impactful structural changes the author should make,
focusing on non-auto-fixable items that require the author's judgment. Be specific:
"Move the cost analysis (Section 4.3, paras 2–4) into the Methods section after
the sampling description" rather than "consider restructuring."]
```
