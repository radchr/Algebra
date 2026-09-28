---
name: anti-slop
version: 3.2.0
description: >
  De-Slop Engine v3.2. Audits text for 8 error types: jargon inflation, mathematical
  decor, unexecutable metaphors, apophenia, unfalsifiable dogma, intellectual impostures
  (Sokal/Bricmont), Catch-22 logic traps, cognitive biases (Beck/Burns/Kahneman).
  Use whenever asked to "de-slop", "audit this theory", "чи це не слоп",
  "перевір на апофену", "feynman test", "catch-22 check", "impostures check",
  "cognitive bias audit", or when you need a rigorous audit of any theoretical text.
allowed-tools: Read Write Edit Glob Grep Skill
license: VIGIL/KAIROS internal
metadata:
  skill-author: CogDelta
  ecosystem: VIGIL v3.1.1 + KAIROS v0.0.1
  date_created: "2026-08-11"
  version_history:
    - "1.0.0 (2026-08-11): Initial release — strict 5-phase acid test"
    - "2.0.0 (2026-08-11): TRIZ-inspired integration, 4-Zone Matrix, Seed [M] protection"
    - "3.0.0 (2026-08-28): Added Sokal/Bricmont, Catch-22, Cognitive Bias phases, QA self-verification"
    - "3.1.0 (2026-08-28): Added Phase 0 (Steelmanning), worked example, core/extended split, removed TRIZ jargon wrapper"
    - "3.2.0 (2026-08-28): Self-audit cleanup. Removed own jargon, fixed description, added 2nd example, defined [H], clarified steelman role"
---

# anti-slop v3.2 — De-Slop Engine

## Purpose

AI can generate pages of academic-sounding prose with LaTeX, category theory, and complex diagrams that contain zero operational substance — **slop**: text that mimics the form of scientific breakthrough while being empty. But dogmatic skepticism is equally dangerous: breakthroughs often start as vague metaphors before formalization. A de-slop tool that destroys everything abstract kills creative ideation.

**Goal:** Purge real slop while protecting genuinely novel ideas that aren't yet formalized.

---

## The 4-Zone Matrix

Every audited claim goes into one of four zones, each with severity levels (Critical / Major / Minor):

```
                 HIGH NOVELTY
                      │
    🟡 SEED [M]       │    🟢 GROUNDED [E]/[F]
  (Preserve, test)    │    (Actionable core)
                      │
 ─────────────────────┼───────────────────── LOW → HIGH RIGOR
                      │
    🔴 SLOP           │    🟠 CLICHÉ
  (Flag, document)    │    (Strip jargon)
                      │
                 LOW NOVELTY
```

**Edge case rules:**
- **🟡↔🔴:** Can the claim produce at least 1 testable prediction? Yes → 🟡. No → one reformulation attempt, then 🔴 LOW-CONFIDENCE.
- **🟡↔🟢:** Does a working measurement or validated proxy exist today? Yes → 🟢. No → 🟡.
- **🟠↔🔴:** True statement under the jargon? Yes → 🟠. No → 🔴.

**🔴 severity:** Critical = pure noise; Major = decorative formalism hiding triviality; Minor = valid point in overly complex phrasing.

---

## 5 Audit Heuristics

These guide the auditor's judgment across all phases:

1. **Layer separation:** Separate metaphors `[M]`, math logic `[F]`, and sensor data `[E]`. Don't judge `[M]` by `[E]` rules prematurely.
2. **Core mining:** Extract the high-leverage core claims from jargon filler. Don't burn the whole document.
3. **Presumption of value:** The auditor must show a metaphor is useless, not assume guilt. If P.o.V. conflicts with code demand (Phase 3), use: can it produce a testable prediction? Yes → 🟡, skip code demand. No → one reformulation attempt, then 🔴.
4. **Toy model proxy:** If you can't measure it, build a short Python simulation to test internal logical consistency.
5. **Multi-horizon scale:** Evaluate across three horizons — immediate test, 1-year model, decade paradigm.

---

## Core Protocol (always run)

### Phase 0 — Steelmanning
Before any critique:
1. *"What is the strongest version of what the author is trying to say?"*
2. *"If this were written by a competent expert having a bad writing day, what would they mean?"*
3. Write a 2-sentence steelman. This anchors the audit against prosecutorial bias. **The steelman does not override Phases 1–5 findings — it prevents dismissing valid ideas, not excusing real slop.**

### Phase 1 — Feynman De-Slop
1. Identify academic buzzwords. Translate central claims into 5-year-old language ("Explain Like I'm 5").
2. Separate **🟠 Trivial Clichés** (plain truths in big words) from **Novel Claims**.

### Phase 2 — Variable Grounding
For every equation or symbol: build `[Symbol | Meaning | Unit/Domain | Sensor OR Proxy]`.
- No sensor but clear logical rules → Seed 🟡 (Simulation Proxy Available).
- Purely decorative, no rules or observables → Slop 🔴 (Pseudo-Math Decor), strip.

### Phase 3 — Runnable Code Demand
1. Write a minimal executable Python script demonstrating the concept.
2. For Seeds 🟡 — build a Toy Model Proxy showing internal logical consistency.
3. If not codeable — apply Heuristic #3 (Presumption of Value) before classifying.

### Phase 4 — Anti-Apophenia (Hanlon's Razor)
Compare H_Intent (strategic pattern) vs H_Noise (bureaucracy / laziness / noise):
- Count independent evidence for each. If N_noise ≥ 3 and N_intent ≤ 1 → likely noise.
- If N_intent ≥ 3 and N_noise ≤ 1 → pattern may be real, retain.
- Otherwise → INCONCLUSIVE, do not flag.
Strip conspiratorial *framing* while keeping the systemic observation if one exists.

### Phase 5 — Falsification
1. *"What exact observation would prove this claim FALSE?"* (Popper test)
2. For surviving Seeds 🟡, outline the upgrade roadmap: `[M] → [H] → [E]`, where:
   - `[M]` = metaphor (untested intuition)
   - `[H]` = hypothesis (testable prediction formulated)
   - `[E]` = empirically validated (measured and confirmed or refuted)

---

## Extended Protocol (on request, or for complex / cross-disciplinary texts)

### Phase 6 — Impostures Filter (Sokal/Bricmont)
For every term borrowed from another discipline:
- (a) Does the author understand the original technical meaning?
- (b) Is there logical rationale for the cross-domain transfer?
- Both No → **Intellectual Imposture** (flag with original meaning vs. misuse).
- (a) Yes, (b) Partial → **🟡 [M]** with noted import gap.
- Both Yes → **Legitimate transfer**, no action.
- **Self-application:** Apply this check to the audit itself.

### Phase 7 — Catch-22 Detector
1. Find all conditional requirements ("if X then Y").
2. Circular dependency? (X needs Y, Y needs X)
3. Double-bind? (reader trapped regardless of choice)
4. Self-referential definition? (term defined by itself)
5. Flag as **structural logic defect**. Propose resolution for each.

### Phase 8 — Cognitive Bias Scan (Beck/Burns/Kahneman)
Check for:
1. **All-or-nothing framing** — only 2 options where spectrum exists?
2. **Anchoring** — first-mentioned option given disproportionate weight?
3. **Confirmation bias** — method only confirms, never disconfirms?
4. **Emotional reasoning** — "feels true ∴ is true"?
5. **Labeling** — evaluative labels instead of descriptions?
6. **Overgeneralization** — single example → universal pattern?
7. **Should statements** — rigid imperatives where conditionals fit?
Flag as **methodological concerns**, separate from content slop.

---

## Self-Verification (run once after audit, do NOT recurse further)

1. **Retraction test:** Which findings would I retract on a 3-sentence defense? → reduce confidence, don't flag 🔴.
2. **Confirmation bias check:** Did I find what I looked for, or what was there? Re-read for missed strengths.
3. **Inter-rater test:** Would a second auditor agree? If uncertain → LOW-CONFIDENCE.
4. **Regression check:** Does the de-slopped text still convey its core message? If not → audit was too aggressive.
5. **Sensitivity check:** Change one key word — does the classification change? If yes → fragile, mark LOW-CONFIDENCE.

---

## Worked Example

**Input text (3 sentences):**
> "The autopoietic tensor field of organizational consciousness undergoes phase transitions when the eigenvalues of the stakeholder attention matrix exceed the criticality threshold λ_c = 2.73, triggering a symmetry-breaking cascade that reorganizes the firm's cognitive topology."

**Phase 0 (Steelman):** The author might mean: organizations have tipping points where enough people paying attention to an issue causes rapid structural change.

**Phase 1 (Feynman):** In plain language: "When enough people in a company focus on the same thing, the company suddenly reorganizes." This is a known observation (tipping points in organizations). The 15 technical terms add zero clarity → mostly 🟠 Cliché.

**Phase 2 (Variables):**
| Symbol | Meaning | Sensor | Status |
|---|---|---|---|
| "autopoietic tensor field" | undefined | none | 🔴 Decor |
| "eigenvalues of stakeholder attention matrix" | undefined matrix, no data source | none | 🔴 Decor |
| λ_c = 2.73 | arbitrary constant | no derivation given | 🔴 Decor |
| "symmetry-breaking cascade" | phase transition metaphor | — | 🟡 Seed if formalized |

**Verdict:** 🟠 Cliché (Major) — valid observation (organizational tipping points) buried under decorative physics terminology. The "symmetry-breaking" metaphor is a 🟡 Seed [M] if the author can define what symmetry is being broken and build a toy model.

### Example 2: Mostly clean text

**Input text:**
> "We measured response latency across 400 participants using a within-subjects design. The priming condition reduced reaction time by 23ms (95% CI: 15–31ms, p < 0.001). This suggests automatic semantic activation occurs before conscious awareness of the prime."

**Phase 0 (Steelman):** The author presents a well-powered experiment with a clear result — priming speeds up reactions, implying unconscious semantic processing.

**Phase 1 (Feynman):** In plain language: "We showed people a word they couldn't consciously see, and it made them faster at recognizing a related word. This means the brain starts understanding words before you're aware of seeing them." No unnecessary jargon detected.

**Phase 2 (Variables):** All variables (latency, N=400, 23ms, CI, p) have defined units, sensors (reaction time software), and standard statistical meaning. → All 🟢.

**Phase 5 (Falsification):** Falsifiable: "If a replication with N=400 shows no RT difference (CI includes 0), the claim fails." The final sentence ("suggests automatic semantic activation occurs before conscious awareness") goes slightly beyond the data → 🟡 Seed [M] that needs further experiments (e.g., awareness probes).

**Verdict:** 🟢 Grounded (Minor note) — clean experimental report. One sentence is a 🟡 interpretive Seed, not slop.

---

## Output Template

Save as `<slug>-de-slop-report.md`:

```markdown
# De-Slop Audit Report: [Target Title]

**Date:** YYYY-MM-DD | **Auditor:** anti-slop v3.2.0
**Target:** [path or description]
**Purity Score:** [0–100%] | **Confidence:** [HIGH/MEDIUM/LOW]
**Protocol:** Core / Core + Extended

## 1. Steelman & Plain Summary
> **Steelman:** [2 sentences — strongest version of what author means]
> **ELIF-5:** [1-2 sentences in simple language]

## 2. Zone Matrix
| Zone | Count | Severity | Items | Action |
|---|---|---|---|---|
| 🟢 Grounded | N | — | [List] | Actionable Core |
| 🟡 Seed [M] | N | — | [List] | Preserved / Prediction Written |
| 🟠 Cliché | N | — | [List] | De-jargoned |
| 🔴 Slop | N | C/Maj/Min | [List] | Flagged with reasoning |

## 3. Toy Model & Predictions
[Python code and/or prediction table for Seeds]

## 4. Variable Audit
[Symbol | Meaning | Domain | Sensor/Proxy | Status]

## 5. Falsification Roadmap
[Claim | Falsifying Observation | Upgrade Path]

## 6. Extended Findings (if run)
[Impostures table | Catch-22s found | Cognitive biases detected]

## 7. Self-Verification
[5-question results table | Errors found in this audit]

---
*Generated by anti-slop v3.2.0*
```
