# Authoring artifact templates

Use these shapes as stable contracts. Add topic-specific material, but keep the core fields.

## `lesson_brief.md`

```markdown
---
lesson_id: PHY-XX
slug: lesson-slug
subject: physics
grade: 7
status: draft
creation_mode: guided
approval_bypassed_by_user: false
---

# Робоча картка уроку

## Початкова ідея автора

## Головна думка уроку

## Питання, які потрібно розкрити

- [запропоновано] ...

## Типові помилки учня

## Візуальний дослід

### Що змінює учень
### Що залишається сталим
### Що спостерігає учень
### Що учень має зафіксувати

## Сюжет і персонажі

## Спільна розмова дитини й дорослого

### Де зупинитися
### Що дорослий може запитати

## Текст для екрана

## Ідеї для озвучення

## Потрібні артефакти
```

Store the exact unedited author request separately in `source_prompt.md` and repeat it verbatim under `Початкова ідея автора`.

## Locked text

Use paired markers:

```text
[ЗБЕРЕГТИ ДОСЛІВНО]
Цей текст не можна переписувати без прямого дозволу автора.
[/ЗБЕРЕГТИ ДОСЛІВНО]
```

Before each write, compare the full contents of all locked blocks. A scientific conflict inside a locked block requires author approval; it is not a reason to alter the block silently.

## `decisions.md`

```markdown
# Рішення автора і моделі

| Дата | Рішення | Хто вирішив | Причина |
|---|---|---|---|
| YYYY-MM-DD | ... | автор / модель | ... |
```

Record only decisions that affect learning goals, story, artifacts, narration, scientific assumptions, or user-visible behavior.

## `scenario.md`

For each scene include:

```markdown
## Сцена 1. Назва

- Мета сцени:
- Дія учня:
- Що видно на екрані:
- Репліка або наратив:
- Коротка підказка для спільної розмови, якщо потрібна:
- Перехід до наступної сцени:
- Критерій завершення:
```

Do not use internal methodology names as learner-visible headings.

## `narration_ua.md`

```markdown
# Озвучення

## scene-001

speaker: narrator
emotion: доброзичливо
text: Природна українська репліка без цифр і формул.
```

## `scenes.json`

```json
{
  "version": 1,
  "voice_profile": "single_ukrainian_voice",
  "scenes": [
    {
      "id": "scene-001",
      "speaker": "narrator",
      "emotion": "доброзичливо",
      "narration": "Природна українська репліка.",
      "screen_math": "p = rho * g * h",
      "audio": "audio/approved/scene-001.wav",
      "duration_seconds": null
    }
  ]
}
```

Keep `screen_math` out of the string passed to TTS.

## State and integrity files

- `workflow.json` stores durable brief/scenario approval evidence or the user-requested quick-mode bypass.
- `integrity.json` stores hashes for `source_prompt.md` and every locked block.
- `legacy_notebooks.json` stores the baseline hashes captured at initialization.
- `audio_manifest.json` maps each scene to its narration hash, selected clip, duration, and recoverable previous approved clips.
- `timeline.json` stores the ordered scene durations used by the learner artifact.
