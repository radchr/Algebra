# Authoring workflow

Use this workflow when starting or resuming a lesson.

## 1. Inspect before asking

1. Read the user's latest request and any pasted scenario.
2. Look for an existing matching directory under `authoring/`.
3. If resuming, read `workflow.json`, `source_prompt.md`, `lesson_brief.md`, `decisions.md`, and the current scenario before asking anything.
4. Do not ask for facts already present in those sources.

## 2. Initialize the lesson

Choose a short lowercase hyphenated slug. Run:

```powershell
python .agents/skills/stem-lesson-author/scripts/init_lesson.py <slug> --subject <subject> --mode <guided|scenario|quick>
```

If the directory exists, reuse it rather than creating a duplicate. The script refuses to overwrite existing files.

Copy the user's request exactly into `source_prompt.md` and under `Початкова ідея автора`. After adding any locked blocks, seal both with:

```powershell
python .agents/skills/stem-lesson-author/scripts/seal_integrity.py authoring/<lesson-slug>
```

Never refresh a seal unless the user explicitly authorized changing the original or locked text.

## 3. Build the author brief

Preserve the user's raw prompt under `Початкова ідея автора`. Extract:

- one central learning outcome;
- questions the lesson must illuminate;
- likely grade-7 misconceptions;
- the one-variable investigation;
- the observation the learner must record;
- the integrated story problem;
- the moments where the adult should ask, compare, or pause with the child;
- learner-visible screen content;
- narration intent and constraints.

Mark proposed items with statuses: `запропоновано`, `погоджено`, `уточнити`, or `відхилено`.

Ask one question at a time only when the answer materially changes the learning goal, scientific model, story, or required artifact. For a secondary gap, choose a conservative default and record it in `decisions.md`.

## 4. Apply author revisions

Interpret natural commands such as:

- «це прибрати»;
- «тут уточнити»;
- «додай гумор»;
- «цю помилку робить Річард»;
- «це не озвучувати».

Update the brief and decision log together. Do not reintroduce rejected items. Compare every locked block before and after the edit.

## 5. Brief approval gate

In standard mode, show the revised brief and wait for explicit approval before producing the scenario. Record the user's exact approval phrase:

```powershell
python .agents/skills/stem-lesson-author/scripts/record_approval.py authoring/<lesson-slug> brief --evidence "<exact user phrase>"
```

In quick mode, record `approval_bypassed_by_user: true` and continue.

## 6. Produce the scenario

Create a short coherent sequence:

1. a character-driven problem and learner prediction;
2. a focused investigation with one manipulated variable;
3. a learner observation or evidence statement;
4. a brief inline invitation for the adult to discuss the observation when useful;
5. a plain-language synthesis with exact mathematics on screen;
6. a practical mission and brief comedic resolution.

These are authoring functions, not labels for the learner UI.

Present the complete scenario to the user. In standard mode, wait for a second explicit approval and record it before generating any learner artifact or audio:

```powershell
python .agents/skills/stem-lesson-author/scripts/record_approval.py authoring/<lesson-slug> scenario --evidence "<exact user phrase>"
```

## 7. Generate artifacts

Create only the artifacts the scenario needs. A lesson may use Marimo alone; do not add Manim, p5.js, or D3.js without a learning reason.

After the scenario is approved:

1. prepare `narration_ua.md` and `scenes.json`;
2. validate narration;
3. generate one audio clip per scene and a timeline;
4. implement testable domain logic;
5. implement the learner-facing module;
6. run quality gates;
7. add the notebook to `docs/new_notebooks.md` with a short description;
8. repair safe defects without changing approved intent.

## 8. Resume after interruption

Treat files as authoritative. Read the durable stage and approval evidence from `workflow.json`; do not infer approval from placeholder files. Do not regenerate approved audio whose narration hash has not changed.
