# Pathology Catalog

The full list of writing pathologies (P0–P2) and clarity issues (C1–C6) that Agent 2 (Clarity & Pathology Scanner) scans for. The orchestrator pastes this entire file into Agent 2's prompt where `[insert references/pathology-catalog.md]` appears. The editor agent's "pathology awareness" list (in `editor-agent.md`) is a condensed version of the same patterns.

## Contents

- [Severity tiers](#severity-tiers)
- [P0: Always flag — credibility-damaging](#p0-always-flag--credibility-damaging) (P0-1 to P0-7)
- [P1: Quality signal — flag when clustered](#p1-quality-signal--flag-when-clustered) (P1-8 to P1-16)
- [P2: Density-dependent](#p2-density-dependent) (P2-17 to P2-28)
- [Clarity issues](#clarity-issues) (C1 to C6)

## Severity tiers

- **P0 — Credibility-damaging.** Flag every instance and provide a specific rewrite. These make text read as formulaic or mechanical.
- **P1 — Quality signal.** Flag every instance and provide a specific rewrite. One isolated instance per paragraph may survive, but the default is to fix it: justify keeping, not flagging.
- **P2 — Density-dependent.** Flag every instance and provide a specific rewrite; do not skip these. After the paragraph-by-paragraph scan, do a dedicated **P2 sweep**: count em dashes, synonym cycles, and bold usage across the full document. Thin any section that exceeds the thresholds below.

**The default for every tier is: rewrite.** Each finding needs a concrete replacement, because a flag without a fix just hands the work to someone with less context. If the problem is identifiable, the fix is writable. The editor applies every rewrite unless it can name a specific reason to keep the original.

Flag **clarity issues** (C1–C6) separately from the pathology patterns, also with a specific rewrite for each.

---

## P0: Always flag — credibility-damaging

**P0-1. Contrasting constructions**
"This isn't about X, it's about Y"; "Not only X, but Y"; "Rather than X, we Y"; "It's not just about X — it's about Y."
*Why it's bad:* Wastes the reader's time by saying what something isn't before saying what it is. Rewrite as a direct positive statement.

**P0-2. Significance inflation**
Words: "stands/serves as," "is a testament to," "a pivotal/crucial/vital role," "underscores/highlights its importance," "reflects broader trends," "marking/shaping the," "key turning point," "evolving landscape," "indelible mark," "groundbreaking," "transformative"
*Why it's bad:* Tells the reader something is important instead of showing why. Puffs up ordinary claims with empty grandeur.

**P0-3. Copula avoidance**
"Serves as," "stands as," "functions as," "represents," "marks," "boasts," "features," "offers" — used where "is," "are," or "has" would do.
*Why it's bad:* Obscures simple relationships behind unnecessarily complex verbs. "The library is the research facility" beats "The library serves as the research facility."

**P0-4. Filler openers and closers**
"At its core," "Ultimately," "In a world where," "What this means is," "Put simply," "In short," "In conclusion," "Let's dive in," "Here's the thing," "When it comes to."
*Why it's bad:* Delays the point. The reader must wade through throat-clearing to reach the actual content.

**P0-5. Claim-restatement phrasing**
Broad claim + em dash or colon + elaboration that restates the same claim in different words.
*Why it's bad:* Says the same thing twice. The reader gains no new information from the elaboration.

**P0-6. Conversational artifacts**
"Great question!" "You're absolutely right!" "I hope this helps!" "Let me know if you'd like me to expand." "Here is an overview of..."
*Why it's bad:* Residue from interactive conversation, not prose. Immediately signals the text was not written for its current context.

**P0-7. Generic positive conclusions**
"The future looks bright." "Exciting times lie ahead." "This represents a major step in the right direction."
*Why it's bad:* Evacuates meaning. Says nothing verifiable or specific. Readers learn nothing.

---

## P1: Quality signal — flag when clustered

These matter most when they cluster (2+ per paragraph), but flag and rewrite every instance by default.

**P1-8. Overused cliché vocabulary**
Additionally, align with, delve, encompass, enduring, enhance, elucidate, facilitate, foster, garner, highlight (verb), holistic, interplay, intricate/intricacies, key (adjective), landscape (figurative), leverage, multifaceted, nuanced, paradigm, pivotal, robust, showcase, synergy, tapestry (figurative), testament, underscore (verb), utilize, valuable, vibrant, realm, myriad, plethora
*Why it's bad:* These words are so overused they've lost meaning. They signal formulaic writing to attentive readers.

**P1-9. Superficial -ing phrases**
"highlighting/underscoring/emphasizing...," "ensuring...," "reflecting/symbolizing...," "contributing to...," "cultivating/fostering...," "showcasing..."
*Why it's bad:* Tacks fake depth onto sentences. The participle phrase promises analysis but delivers nothing. Usually deletable without information loss.

**P1-10. Rule of three**
Forcing ideas into groups of three: "innovation, inspiration, and insight"; "speed, quality, and reliability"; "streamlining processes, enhancing collaboration, and fostering alignment."
*Why it's bad:* Manufactured triads pad word count and create a false sense of completeness. Say what you mean — two things or four things are fine.

**P1-11. Promotional language**
"vibrant," "rich" (figurative), "profound," "nestled," "in the heart of," "renowned," "breathtaking," "stunning," "must-visit," "commitment to excellence," "seamless"
*Why it's bad:* Reads like advertising copy, not analysis or exposition. Replaces specific detail with empty superlatives.

**P1-12. Negative parallelisms**
"Not only...but also..."; "It's not merely X, it's Y."
*Why it's bad:* Same issue as P0-1 (contrasting constructions) in a slightly different form. Wastes time with what something isn't.

**P1-13. False concession structure**
"While X is true, what really matters is Y." / "Sure, X, but the real story is Y."
*Why it's bad:* Simulates balanced reasoning without actually engaging the concession. If the concession matters, integrate it. If it doesn't, cut it.

**P1-14. Emotional flatline**
Every sentence at the same emotional register. No surprise, no frustration, no delight, no uncertainty.
*Why it's bad:* Makes text feel assembled rather than written. Even technical writing has moments where something is surprising or counterintuitive — noting them is honest and engaging.

**P1-15. Rhetorical question openers**
"But what does this mean for the future?" "So why does this matter?" "Have you ever wondered...?"
*Why it's bad:* Delays the answer. The reader came for information, not Socratic dialogue. Answer directly.

**P1-16. Vague attributions**
"Experts argue," "Industry reports suggest," "Observers have noted," "Some critics say," "several sources"
*Why it's bad:* Attributes claims to unnamed authorities. Either name the source or delete the attribution.

---

## P2: Density-dependent

**P2-17. Em dash overuse**
Flag every em dash. Replace with commas, colons, parentheses, semicolons, or periods. Keep an em dash only when no alternative works and it genuinely adds clarity. **Threshold: more than 2 em dashes per page (or more than 3 in any section) is a cluster that must be thinned.** After scanning for other pathologies, do a dedicated em-dash sweep: count all em dashes in the document and flag sections that exceed the threshold.
*Why it's bad:* Overuse of em dashes as a rhetorical pause creates a choppy, sales-pitch cadence. Commas, periods, and sentence restructuring usually work better.

**P2-18. Synonym cycling (elegant variation)**
"The protagonist... The main character... The central figure... The hero..."
*Why it's bad:* Cycling through synonyms for the same referent forces the reader to figure out whether you're talking about the same thing or something new. Repeat the same word — clarity beats variety.

**P2-19. Boldface overuse**
Mechanical emphasis in running text.
*Why it's bad:* When everything is emphasized, nothing is. Remove bold unless it serves a genuine structural purpose.

**P2-20. Inline-header vertical lists**
Bullet points where each item starts with a bolded header and colon.
*Why it's bad:* Fragments ideas into disconnected items. Convert to flowing prose when the list has fewer than 5 items or when items are short.

**P2-21. Title case in headings**
Capitalizing every main word: "Strategic Negotiations And Global Partnerships."
*Why it's bad:* Sentence case reads more naturally and is the norm outside of newspaper headlines.

**P2-22. Curly quotation marks**
Curly quotes (“...”) instead of straight quotes ("...").
*Why it's bad:* A formatting artifact from certain tools. Replace with straight quotes if the target format expects them.

**P2-23. Emojis**
Decorative emojis in headings or bullet points.
*Why it's bad:* Inappropriate for most prose contexts. Remove unless the format explicitly calls for them.

**P2-24. Hyphenated word pair overuse**
Mechanically consistent hyphenation of common compound modifiers (cross-functional, data-driven, high-quality, end-to-end).
*Why it's bad:* Unnatural consistency in hyphenation reads as mechanical. Natural writing is inconsistent about these.

**P2-25. False ranges**
"From X to Y" where X and Y aren't on a meaningful scale.
*Why it's bad:* Creates a false sense of scope. Just list the topics.

**P2-26. Knowledge-cutoff disclaimers**
"As of [date]," "While specific details are limited," "Based on available information."
*Why it's bad:* Residue from tools with training cutoffs. Delete.

**P2-27. Novelty inflation**
"Groundbreaking," "revolutionary," "first-of-its-kind," "game-changing," "unprecedented."
*Why it's bad:* Almost always an overstatement. Readers discount inflated claims; it damages credibility.

**P2-28. Reasoning chain artifacts**
"Let me think about this step by step," "First, let's consider...," "This brings us to an important point."
*Why it's bad:* Residue from chain-of-thought reasoning processes. Not prose. Delete.

---

## Clarity issues

Flag these separately from the pathology patterns above.

**C1. Passive voice** — Flag when the actor matters and is omitted. "The data were analyzed" → "We analyzed the data."

**C2. Weak verb + noun** — "Performed an analysis of" → "Analyzed." "Is indicative of" → "Indicates."

**C3. Filler phrases** — Apply the delete-on-sight table:

| Kill | Replace with |
|---|---|
| "It is important to note that" | *(delete)* |
| "It should be noted that" | *(delete)* |
| "In order to" | "To" |
| "Due to the fact that" | "Because" |
| "At this point in time" | "Now" |
| "The system has the ability to" | "The system can" |
| "In the event that" | "If" |
| "A number of" | the actual number, or "several" |
| "In terms of" | *(rephrase or delete)* |
| "In other words" | *(fix the first version instead)* |
| "As a matter of fact" | *(delete)* |
| "It goes without saying" | *(then don't say it)* |
| "This paper contributes to the literature" | say what it actually contributes |
| "At the end of the day" | *(delete)* |
| "Needless to say" | *(delete)* |

**C4. Excessive hedging** — More than one hedge per claim. "It could potentially possibly be argued" → "X may affect outcomes."

**C5. Mid-sentence interjections** — "X, which does Y, also does Z." Unpack nested clauses.

**C6. Multi-idea sentences** — Sentences containing two or more independent ideas. Split them.
