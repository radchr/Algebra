# Natural Ukrainian narration and audio

Read this reference whenever writing narration, generating audio, or re-voicing a scene.

## Separate meaning from notation

Screen text carries exact notation. Narration carries the idea.

Screen:

```text
rho = m / V
```

Narration:

```text
Густина показує, скільки речовини припадає на певний об'єм.
```

Do not transliterate a formula into a list of symbols unless the author explicitly requires a short spoken arithmetic step.

## TTS-safe rules

- Spell all numbers as Ukrainian words.
- Expand units and percentages into natural phrases.
- Prefer familiar expressions such as «пів літра» over mechanical decimal readings when the value is exact.
- Replace symbolic comparisons with meaning: `rho_body > rho_liquid` becomes «тіло густіше за рідину».
- Keep sentences short enough to speak comfortably in one breath.
- Do not include Markdown headings, bullets, code fences, URLs, file paths, LaTeX, stage directions, or raw variable names in the TTS payload.
- Keep emotion and direction metadata outside `text` unless the selected engine explicitly supports those controls.

Simple arithmetic is allowed when it teaches the step:

```text
Два помножити на три дорівнює шість.
```

Avoid unnatural readings such as «пе дорівнює ро же аш».

## Automatic generation

Use the project's established TTS architecture in `docs/tts_voiceover_architecture.md`. Use one Ukrainian voice consistently across characters. Character identity comes from wording and context, not voice cloning.

Generate one clip per scene. Store candidates in `audio/takes/<scene-id>/`; copy the selected clip to `audio/approved/`. Record the narration hash, selection, duration, and any prior approved paths in `audio_manifest.json`, then update `timeline.json`.

## Re-voicing

When the user requests a re-voice:

1. identify the scene and preserve all other approved clips;
2. revise text only when requested or when pronunciation requires it;
3. rerun narration validation;
4. generate a new take;
5. keep the previous approved clip recoverable;
6. update duration and timeline for that scene only.

Do not regenerate an unchanged approved clip.
