# 0000 — Genesis: the studio scaffold

> **Reconstructed** from repo state on 2026-08-07. The original session left no
> notes, so this entry is inferred from the committed files rather than a
> first-hand record. Treat specifics as best-effort.

## Focus

Stand up "Sequitur Studios" — a Gemini Omni Flash video studio that composes
shots through Bowen's grammar of the shot.

## What was built

- The `sequitur/` package:
  - `grammar.py` — Bowen's vocabulary as typed enums + a `Shot` dataclass. This
    first pass was derived from a **shallow read** of the text (a single flat
    `Lighting` enum, a vertical-only `CameraAngle`, no VLS, no lens/DOF/motion-speed
    axes). Later corrected — see `0001`.
  - `prompt.py` — `build_prompt(Shot)` → a film-literate Omni Flash prompt (leads
    with scene, layers camera/lighting, states sound design, folds negatives inline).
  - `studio.py` — `render()` / `edit()` over the Interactions API (conversational,
    stateful editing).
  - `config.py` — `.env` loading / key handling.
- `scripts/generate.py` — CLI renderer with `--dry-run`.
- `artifacts/grammar of the shot/reference.md` — a one-page overview of the Bowen
  concepts the enums encode.
- Project plumbing: `README.md`, `requirements.txt`, `.env.example`, `.gitignore`,
  `Sequitur-Studios.code-workspace`, `output/` (gitignored).

## Model note

Built on `gemini-omni-flash-preview` (native multimodal, conversational editing).
Veo 3.1 noted as available for scene-extension / last-frame control if needed.

## Resulting state

A working end-to-end scaffold: you could compose and render a single grammar-aware
shot. The grammar vocabulary was serviceable but shallow, and `reference.md` was a
loose summary rather than a faithful abridgement of the source.
