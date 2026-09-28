# Quality gates

Use this checklist before implementation and final handoff. The script catches deterministic issues; the model must still review meaning and learner experience.

## Authoring integrity

- The brief has one central learning outcome.
- Approved questions are covered; rejected questions are absent.
- All paired locked blocks are unchanged.
- Model-selected assumptions are recorded in `decisions.md`.
- Standard mode has separate explicit brief and scenario approvals in `workflow.json`; quick mode records the bypass.
- `source_prompt.md` and locked blocks match their integrity seal.

## Learning flow

- The learner makes an explicit prediction without a preselected answer.
- The investigation changes one independent variable at a time.
- The learner records an observation before explanation appears.
- The explanation connects the observation to the exact screen model.
- The mission has a measurable success condition.
- Hints scaffold without immediately giving the final setting or answer.
- The lesson creates natural pauses for conversation between the child and adult; it does not assume unsupervised completion.

## Story and learner UI

- Humor changes the problem, represents a misconception, prompts an action, or rewards success.
- Characters never shame the learner.
- Learner-facing text contains no POEM, BKT, Bayesian, misconception IDs, model names, author notes, or uncalibrated mastery percentages.
- The opening screen has a single clear action and no decorative overload.
- Information is not communicated by color alone.
- Interactive controls have labels, keyboard operation, visible focus, and a reduced-motion path when animation is used.
- Charts and simulations have a concise text equivalent.
- Adult prompts appear inline only when useful, remain visually secondary, and contain no internal pedagogy labels.

## Scientific model

- Domain logic is separate from UI and covered by boundary tests.
- Assumptions, valid ranges, units, and omitted effects are explicit in authoring material.
- Visual forces, quantities, and graphs agree with the calculation.
- A scientific conflict is surfaced rather than silently corrected.

## Narration and audio

- Narration contains no raw digits, formula syntax, LaTeX, abbreviated units, or animation directives.
- Simple spoken calculations sound natural.
- One Ukrainian voice is used consistently.
- Every narrated scene has an approved clip and recorded duration.
- Re-voicing one scene does not alter other approved clips.

## Runtime and repository

- Runtime network dependencies are intentional and recorded in the authoring material.
- When offline operation was explicitly requested, all runtime assets are local and validation uses `--require-offline`.
- A missing network resource produces a clear learner-visible message instead of a broken blank area.
- `marimo check`, Ruff, relevant unit tests, and any implementation-specific checks pass.
- No legacy notebook changed. Compare status before and after implementation.
- Every newly created notebook has one linked, one-sentence entry in `docs/new_notebooks.md`; legacy notebooks remain absent.
- Generated heavy media remains consistent with the repository's ignore policy.

Run:

```powershell
python .agents/skills/stem-lesson-author/scripts/validate_lesson.py authoring/<lesson-slug> --learner-root <generated-artifact-root> --require-audio --final
```

Treat validator success as necessary, not sufficient.
