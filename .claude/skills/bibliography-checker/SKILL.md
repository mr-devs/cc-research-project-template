---
name: bibliography-checker
description: >-
  Audits the citations and bibliography of an academic paper by verifying via web search that every cited work exists and is described faithfully, flagging claims that need a citation, near-paraphrase, self-citation, and important missing or contradictory literature, and optionally fixing .bib and in-text problems. Use this skill whenever the user wants to check, audit, verify, or clean up references, citations, a reference list, or a .bib file in a manuscript, thesis, or grant (LaTeX, Quarto, R Markdown, or Markdown), asks whether citations are real, hallucinated, retracted, or mischaracterized, wants to know what literature they are missing before submission, or asks for a citation or reference check, even if they don't name the skill. Not for generating new BibTeX entries from a DOI, URL, or title (use bib-generator) or for checking the abstract against the body (use abstract-checker).
argument-hint: "[path/to/paper] [apa|chicago|harvard|vancouver|ieee|nature|science|bibtex] [review|diff|apply]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
  - WebSearch
  - WebFetch
metadata:
  version: 1.1.0
  source: https://github.com/SolomonMg/research-agent-skills
---

# Bibliography Checker

Coordinate a three-agent audit of a paper's citations. The goal goes beyond formatting: confirm that cited works are real, that the paper describes them faithfully, that claims needing attribution have it, and that the bibliography covers the literature reviewers will expect.

Agents ground their findings in web searches (Semantic Scholar, CrossRef, Google Scholar, publisher sites) rather than memory. This matters because the most damaging bibliography errors — fabricated, retracted, or misdescribed papers — are exactly the ones a model is prone to miss or introduce when working from recall. Never add or recommend a citation that has not been confirmed by a search result; an invented reference is worse than a missing one.

## Scope and related skills

In scope: citation existence and metadata, characterization faithfulness, uncited claims, near-paraphrase, self-citation, missing and contradictory literature, bibliography balance, and `.bib`/in-text citation fixes.

Out of scope, with where to go instead:
- Generating a BibTeX entry from a DOI, URL, or title → `bib-generator`
- Whether the abstract matches the body → `abstract-checker`
- Argument logic and contribution framing → `top3-reviewer`
- Statistical methods → `statistical-reviewer`
- Prose clarity and style → `writing-editor`; paragraph and section structure → `structural-editor`
- Code and replication materials → `review-paper-code`

## Phase 1: Parse arguments

Parse `$ARGUMENTS` token by token (case-insensitive):

**Citation style** → `CITE_STYLE`

| Token | Style |
|---|---|
| `apa` | APA 7th edition (Author, Year) |
| `chicago` | Chicago author-date |
| `harvard` | Harvard referencing |
| `vancouver` | Vancouver numbered |
| `ieee` | IEEE numbered |
| `nature` | Nature superscript numbered |
| `science` | Science numbered |
| `bibtex` | BibTeX/BibLaTeX (auto-detect details from the .bib file) |

If no style token is given, set `CITE_STYLE` to `auto` and detect it from the document (`\bibliography`, `\addbibresource`, `natbib`, `biblatex`, or in-text citation patterns).

**Fix mode** → `FIX_MODE`

| Token | Behavior |
|---|---|
| *(none)* → `report` | Default. Read-only: produce the report, modify no files. |
| `review` | Interactive. For each fixable item, open VS Code at the location, show the issue and proposed fix, and apply only what the user approves. |
| `diff` | Apply all auto-fixable changes, then open VS Code so the user can inspect and revert hunks. |
| `apply` | Apply all auto-fixable changes without opening VS Code (headless or non-VS-Code environments). |

Any remaining text is the file path. If `$ARGUMENTS` is empty, auto-detect everything.

## Phase 2: Discover the paper and bibliography

1. If no path was given, Glob for `**/*.tex`, `**/*.qmd`, `**/*.Rmd`, `**/*.md` and pick the main document (a `.tex` with `\documentclass`, or a `.qmd`/`.Rmd` with a YAML `title:`). Read it and every file it includes.
2. Find `.bib` files from `\bibliography{}` or `\addbibresource{}`; otherwise Glob for `**/*.bib`. Read them all. If references are inline (no `.bib`), parse the reference list from the document.
3. Build two inventories:
   - **Citation inventory** — every in-text citation (author-year or numbered) with the sentence it appears in.
   - **Bibliography inventory** — every reference entry with key, authors, title, year, venue, and DOI if present.
4. Cross-reference them to find **orphans**: in-text citations with no bibliography entry, and bibliography entries never cited.
5. Note the paper's **core topics**: title, main research question, and a handful of key terms from the abstract and introduction. Agent 3 refines this.

Tell the user what you found before launching agents: file paths, detected citation style, number of in-text citations, number of bibliography entries, orphan count, and fix mode.

## Phase 3: Launch the three review agents in parallel

Read `references/agents.md`. It contains the full prompts for:

- **Agent 1 — Claim Extraction & Citation Needs:** classifies every claim, flags uncited claims, near-paraphrase, and self-citation.
- **Agent 2 — Citation Verification & Faithfulness:** web-verifies each reference's existence and metadata, checks how each is characterized, audits formatting.
- **Agent 3 — Coverage & Missing Citations:** web-searches for essential, recent, methodological, competing, and contradictory work; audits balance and gratuitous citations.

Fill each prompt's placeholders with the Phase 2 results and pass the complete prompt text to the Agent tool (`subagent_type: "general-purpose"`). Subagents cannot read this skill directory, so the prompt itself must carry everything. Launch all three in a single message so they run concurrently. All three are read-only; keeping edits out of the review agents avoids conflicting writes.

## Phase 4: Apply fixes (skip in report mode)

If `FIX_MODE` is `report`, skip to Phase 5 — the skill stays read-only.

Otherwise, build a **fix plan** from the agents' findings, including only items where a concrete change can be specified.

**Auto-fixable**
- `.bib` corrections: wrong year, misspelled author names, incorrect DOI, missing fields
- Missing `.bib` entries for citations the agents recommend adding (ready-to-paste entries appended to the `.bib` file, built only from verified search results)
- Citation key mismatches: `\cite{wrong_key}` where the correct key exists
- In-text characterization fixes: "Smith (2020) finds X" where X misrepresents the source
- Formatting fixes: inconsistent citation formatting, missing periods, wrong brackets
- Duplicate bibliography entries (remove the duplicate)

**Recommend only** — these require the author's judgment, so list them in the report rather than editing:
- Whether and where to add a new citation to the prose
- Near-paraphrase rewrites (they require rewriting surrounding text)
- Choosing among several candidate citations for a claim
- Removing citations the author chose to include, even if arguably unnecessary

For each fixable item record file path, line number, exact current text, exact replacement, reason, and severity. Order by severity (CRITICAL first, following the triage hierarchy below), then group by file.

**`review` mode** — for each item in the plan:
1. Run `code -g FILE:LINE` via Bash to open VS Code at the location.
2. Show severity, file and line, current text, proposed fix, and reason.
3. Ask with AskUserQuestion: "Apply this fix? (yes / skip / stop)". On **yes**, apply it immediately with Edit; on **skip**, move on; on **stop**, end and skip the rest.
4. Track applied vs. skipped.

**`diff` and `apply` modes**
1. In `diff` mode, check whether each target file is git-tracked. If it is not, back it up first (`cp FILE FILE.bib-checker-backup`) so the user has something to diff against.
2. Launch a single fixer agent using the Fixer prompt in `references/agents.md`, filled with the fix plan. It is the only agent that edits files.
3. After it returns:
   - `diff`, git-tracked: run `code -g FILE:1` for each modified file and tell the user to open Source Control (Cmd+Shift+G) to review and revert individual hunks.
   - `diff`, not git-tracked: run `code -d FILE.bib-checker-backup FILE` for each modified file.
   - `apply`: summarize the changes only.

Record the outcome (applied / skipped / failed per item) as `FIX_RESULTS`.

## Phase 5: Consolidate and save the report

Read `references/report-template.md` and fill it in. Save to the current working directory as `BIBLIOGRAPHY_CHECK_[YYYY-MM-DD].md` using today's date.

Rank the Priority Action Items with this triage hierarchy, which orders problems by how badly they damage the paper's credibility:

1. Fabricated or retracted citations (Agent 2)
2. Distorted characterizations (Agent 2)
3. Uncited empirical claims (Agent 1)
4. Essential missing citations (Agent 3)
5. Near-paraphrase issues (Agent 1)
6. Metadata mismatches (Agent 2)
7. Important missing citations (Agent 3)
8. Formatting issues (Agent 2)
9. Balance concerns (Agent 3)

Include the "Fixes Applied" section only when `FIX_MODE` is not `report`.

## Phase 6: Tell the user

After saving, report:
1. The path to the saved report
2. The bibliography health assessment
3. If fixes were applied: how many were applied, skipped, and failed
4. Counts of fabricated/retracted references, faithfulness issues, uncited claims, and missing citations
5. The top 5 remaining priority action items (excluding items already fixed)
6. How many ready-to-paste citations are in the "Citations to Add" section
7. In `diff` mode: a reminder to review changes in VS Code Source Control

## Examples

```
/bibliography-checker path/to/paper.tex             # auto-detect style, report only
/bibliography-checker apa path/to/paper.tex         # specify citation style
/bibliography-checker bibtex path/to/paper.tex      # BibTeX-based paper
/bibliography-checker nature path/to/paper.tex      # Nature-style numbered references
/bibliography-checker path/to/paper.tex review      # approve fixes one by one in VS Code
/bibliography-checker path/to/paper.tex apply       # apply fixes headlessly
```

## Sources

This skill synthesizes ideas from RefChecker (Russinovich); Citation-Check-Skill (serenakeyitan); CiteAudit (arXiv 2602.23452); SemanticCite (arXiv 2511.16198); SourceCheckup (Nature Communications 2025); Citation-Hallucination-Detection (Vikranth3140); scite.ai citation-context classification; the Semantic Scholar, CrossRef, and OpenAlex APIs; Imbad0202/academic-research-skills; and AutoCitation (sypsyp97).
