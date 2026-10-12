# Report Template

Read this in Phase 5. Save the report to the current working directory as `ACADEMIC_REVIEW_[YYYY-MM-DD].md`, using today's date. Paste each agent's output into its numbered section, preserving its structure. Write the Executive Summary, verdict, Priority Action Items, Elevator Pitch, and Combined Questions yourself from all three agents.

```markdown
# Academic Review Report

**Paper**: [Title]
**Authors**: [Authors]
**Date**: [Today's date]
**Journal standard**: [TARGET_JOURNAL]
**Reviewer persona**: Senior scientist, Science/Nature/PNAS regular

---

## Executive Summary

[5–7 sentences covering:
1. What the paper does (one sentence)
2. The main contribution and whether it is sufficient for TARGET_JOURNAL
3. The strongest aspect of the argument
4. The most critical logical or framing problem
5. The devil's advocate's fatal flaw
6. Overall verdict]

**Verdict**: [Publish as-is | Minor revision | Major revision | Revise and resubmit | Desk reject]

---

## 1. Argument Architecture

[Agent 1 output, preserving its structure]

---

## 2. Contribution & Framing

[Agent 2 output]

---

## 3. Devil's Advocate

[Agent 3 output]

---

## Priority Action Items

Triage hierarchy: logical fallacies and non sequiturs (Agent 1) > missing warrants in
major claims (Agent 1) > contribution/framing problems (Agent 2) > devil's advocate
objections (Agent 3) > section coherence (Agent 1) > audience calibration (Agent 2).

**CRITICAL** (these will sink the paper):
1. ...
2. ...
3. ...

**MAJOR** (reviewers will raise these):
4. ...
5. ...
6. ...

**SHOULD ADDRESS** (strengthens the paper):
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

## The Elevator Pitch

If this paper were accepted, the one-sentence finding that would appear in a news
article is:

> [one sentence — if this sentence is boring or unclear, the paper has a framing problem]

---

## Combined Questions for Authors

[Deduplicated and prioritized list of the most important questions from Agents 1–3,
ordered by severity. Maximum 10 questions.]
```
