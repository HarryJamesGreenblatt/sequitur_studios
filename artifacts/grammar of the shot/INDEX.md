# Grammar of the Shot — grounding index

Christopher J. Bowen, *Grammar of the Shot* (4th ed.), DOI
`10.4324/9781003257356`. This is the studio's **production-phase /
cinematography** grounding: how to frame, compose, light, and shoot-for-the-edit.
It is the source the vocabulary under [`sequitur/crew/`](../../sequitur/crew/)
(the `Cinematographer`/`Gaffer`/`KeyGrip` roles) is derived from.

> This file was the project's original one-page overview; it is now the **index**
> for this source. The faithful, chapter-by-chapter material lives in
> [`reference/`](reference/).

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals + `media/` (as imported).
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth**.
- [`reference/`](reference/) — abridged, session-ready references (what agents load).

## Chapter → code map

| Chapter | Covers | Primary code layer |
|---------|--------|--------------------|
| [Ch. 1 — The Shots](reference/ch01-the-shots.md) | shot sizes, the frame, production pipeline | `ShotSize`, `aspect_ratio` |
| [Ch. 2 — Composition](reference/ch02-shot-composition.md) | angles, framing, look room, two-shots | `SubjectView`, `CameraAngle`, `ShootingStyle`, `Composition` |
| [Ch. 3 — Depth, Perspective, Focus](reference/ch03-depth-perspective-focus.md) | lines, FG/MG/BG, lens, DOF | `FocalLength`, `DepthOfField`, `lens` |
| [Ch. 4 — Lighting](reference/ch04-lighting.md) | color temp, exposure, quality, direction | `LightQuality`, `LightScheme`, `LightDirection`, `ColorTemperature`, `eye_light` |
| [Ch. 5 — Shooting for Editing](reference/ch05-shooting-for-editing.md) | continuity, 180°/30°, matching, eye-line | *sequence layer (planned)*; `single_scene` |
| [Ch. 6 — Dynamic Shots](reference/ch06-dynamic-shots.md) | motion, camera moves, playback speed | `CameraMovement`, `MotionSpeed` |

## Appendices

- [Appendix A — Aspect Ratios](reference/appendix-a-aspect-ratios.md) — history behind `aspect_ratio`.
- [Appendix C — Resources](reference/appendix-c-resources.md) — further reading.
- [Appendix D — Crew Positions](reference/appendix-d-crew-positions.md) — the roles that constitute a
  production studio; feeds the studio's workflow architecture in
  [`../../context/architecture.md`](../../context/architecture.md).

## Scope note

Grammar of the Shot grounds the **camera department during the production phase**.
Its Ch. 5 (shooting-for-the-edit) *points toward* post-production but does not
cover it — the editorial layer needs its own source (*Grammar of the Edit*; see
the [grounding library](../INDEX.md)).
