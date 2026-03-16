# Sentence-Level Writing Style (CSS Edition)

## Core Philosophy

The reader's ability to interpret complex computational models depends on **structural predictability**. Clarity in CSS writing is achieved by linking "known" theoretical constructs to "new" empirical findings through consistent sentence architecture based on Gopen and Swan's principles.

---

## 1. The Structural "Handshake"

### The Topic Position (Context/Link)

- **Definition:** The first 5–10 words of the sentence.
- **Instruction:** Start sentences with "old" information (theoretical terms, previously mentioned variables, or citations).
- **Goal:** Establish a "safe harbor" for the reader before introducing new complexity.

### The Stress Position (The "Finding")

- **Definition:** The end of the sentence.
- **Instruction:** Place the most significant technical result, the p-value significance, or the specific model outcome here.
- **Goal:** Use the natural emphasis at the end of a sentence to land your most complex points.

---

## 2. Computational Flow & Cohesion

- **The Chain Rule:** Ensure the Stress position of Sentence A informs the Topic position of Sentence B.
- **Logical Continuity:** Do not jump to a new subject without a bridge. If a sentence introduces a new concept, that concept should have been hinted at in the previous sentence's Stress position.
- **Variable Consistency:** Use consistent terminology for variables and models to maintain the Topic-Stress link.

---

## 3. Sentence Architecture & Rhythm

- **Variability is Key:** Use short sentences to state a definitive finding and longer, multi-clause sentences to describe complex data pipelines or theoretical nuances.
- **Subject-Verb Proximity:** Keep the subject (e.g., "The classifier") and the verb (e.g., "identified") as close together as possible. Avoid long "interrupted" clauses.
- **Complexity != Impenetrability:** Nuance is welcome, but it must follow the Topic-to-Stress progression to remain readable.

---

## 4. Tactical CSS Constraints

- **Strong Verbs:** Use active, "doing" verbs. Avoid turning actions into nouns (nominalization). (e.g., Use "The algorithm **clustered**..." instead of "The **clustering** was performed by...")
- **The Math-Prose Bridge:** When referencing formulas or variables, ensure they occupy the Stress position if they are being defined, and the Topic position if they are being used to explain a subsequent result.
- **Minimal Signposting:** Avoid "It is important to note that..." or "Interestingly..." Let the structure of the prose signify what is important.

---

## Example: Weak vs. Style-Aligned

**Weak (Fragmented & Passive):**
Large Language Models (LLMs) often exhibit hallucinations. A benchmark was developed by our team to test this. We found that proprietary models performed better than open-source ones in the context of political news.

**Style-Aligned (Fluid & Compelling):**
While **Large Language Models (LLMs)** are increasingly sophisticated, they remain prone to **hallucinations.** To quantify these **errors**, we developed a specialized **benchmark.** Applying this **benchmark** to political news, we found that **proprietary models significantly outperformed their open-source counterparts.**
