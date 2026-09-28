---
name: stem-lesson-author
description: Create new Ukrainian interactive STEM lessons for grade 7 from a topic or an author-provided scenario, using an author review brief, a clean learner-facing experience, natural TTS narration, and generated Marimo/Manim/p5/D3 artifacts. Use for new lessons in this project; do not use to retrofit legacy notebooks or for other grades.
---

# STEM Lesson Author

Create one new grade-7 STEM lesson as a durable, reviewable authoring package before generating learner-facing code.

## Scope

- Subjects: algebra, geometry, physics, chemistry, and biology for grade 7.
- Work on new lessons only. Treat existing notebooks as legacy unless the user explicitly asks to change one.
- Design for a child and an adult using the lesson together. The notebook supports their conversation; it is not a replacement for an adult explanation or shared discussion.
- Place short prompts for the adult directly at useful pauses in the lesson. Do not create a separate adult mode, dashboard, or control panel.
- Default to the existing Gumball cast for original, task-relevant dialogue. Use other characters or a neutral story only when requested.
- Use one Ukrainian TTS voice for the whole lesson. Do not clone character voices or copy dialogue from the show.
- Offline operation is optional, not a default requirement. Record any runtime network dependency and make its learner-visible failure understandable; require a fully local runtime only when the author asks for it.

## Choose the mode

- **Guided:** the user gives a topic. Ask only for missing decisions that materially change the lesson, one question at a time.
- **Scenario-first:** the user supplies prose. Preserve it in the brief, extract what is already decided, and ask only about critical gaps.
- **Quick:** when the user explicitly says to create everything immediately, make reasonable secondary decisions, record them in `decisions.md`, and proceed without intermediate approval. Still stop for a serious scientific contradiction, a locked-text conflict, missing authority, or unavailable required input.

Read [references/workflow.md](references/workflow.md) when starting or resuming a lesson. Read [references/templates.md](references/templates.md) when creating or updating authoring artifacts.

## Non-negotiable invariants

1. Create or reuse `authoring/<lesson-slug>/`; never scatter authoring state across chat only.
2. `lesson_brief.md` is the source of truth. Copy the raw request byte-for-byte to `source_prompt.md` and the brief, then seal it with `seal_integrity.py`. Preserve it and all paired `[ЗБЕРЕГТИ ДОСЛІВНО]` blocks unless the user authorizes a change.
3. In standard mode, obtain and record two explicit approvals: first the completed brief, then the generated scenario. Do not generate notebook, animation, simulation, or audio before scenario approval.
4. Learner-facing text must not expose POEM, BKT, Bayesian calculations, misconception IDs, model names, authoring notes, or percentages that imply calibrated mastery.
5. Keep screen mathematics exact, but write narration as natural Ukrainian. Never send raw LaTeX, formula syntax, digits, abbreviated units, or animation directives to TTS.
6. Simple arithmetic may be spoken in words when it materially helps the explanation.
7. Humor must advance the problem, embody a misconception, prompt an action, or reward completion. Remove decorative jokes.
8. The learner must act and record an observation before receiving the explanatory synthesis.
9. Generate audio automatically after approval or in quick mode, one clip per scene, with selective re-voicing and preserved previous takes.
10. Do not silently correct a scientific contradiction. Explain it and request permission when resolving it would alter an approved or locked idea.
11. Adult prompts must be brief conversational invitations such as a question to ask, something to compare, or a reason to pause. Keep technical pedagogy out of them.

Read [references/narration.md](references/narration.md) before preparing narration, generating audio, or re-voicing a scene.

When a lesson needs a simplified scientific illustration, interactive diagram, or draggable biological structure, read [references/scientific-illustrations.md](references/scientific-illustrations.md). Reuse the recorded tool decision instead of repeating web research unless the reference's re-research conditions apply.

## Build and verification

- Use the existing project toolchain and read the relevant implementation skill before building: `marimo-agent` for notebooks, `manim` for animation, `p5js` or `d3js` for browser simulations, and `stem-didactics` for the learner flow.
- Put exact scientific or mathematical logic in testable Python functions separate from UI cells.
- Reuse `stem_lab` components where they fit; do not copy legacy notebook structure merely for consistency.
- Before editing, record the legacy notebook status. At handoff, verify no legacy notebook changed.
- After creating a new notebook, add one linked bullet with a one-sentence description to `docs/new_notebooks.md`. Never backfill legacy notebooks into that file.
- Record approvals with `record_approval.py`. Run the deterministic artifact validator with `--final`, `--require-audio`, and a learner file or root, then the relevant project checks. Read [references/quality-gates.md](references/quality-gates.md) before implementation and again before final handoff.
- Safe local defects may be repaired automatically. Stop when a repair would change an approved learning goal, locked wording, or story decision.

## Handoff

Report the created authoring folder, generated learner artifacts, audio status, checks run, any assumptions recorded, and any remaining limitation. Keep the summary about the lesson itself; do not surface internal pedagogy in learner-facing output.
