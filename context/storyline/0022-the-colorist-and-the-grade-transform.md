# 0022 — The Colorist and the Grade Transform

> Date: 2026-08-12 · Focus: **code** — the third and final step of `0019`'s locked
> sequence (ground color → protocol → **Colorist + grade renderer**). Seated the
> **Colorist** role, built the reified **`Grade`** decision model, the **`Grader`**
> ffmpeg transform, and split the renderer registry into **two planes** (producers
> keyed by `Medium`, operators keyed by `Operation`). First code since `0021`.

## What happened

`0019` closed with a locked three-step sequence; `0020` grounded color and `0021`
formalized the `Renderer` protocol. This session built step 3. Rather than bolt the
grade on as "a fifth renderer," a short design discussion (Nystrom's *Game
Programming Patterns*, GoF) surfaced that a **grade is a different shape** from the
existing backends — and that shape decision drove the whole build.

**The asymmetry.** The three generative backends are **producers**: 0 media in → 1
out; their decision is a full spec (a `Shot`, a line of text). `Cutter` is a
**reducer**: n clips → 1 film (it changes medium, VIDEO\*→FILM). A **grade** is an
**operator**: 1 media in → 1 out, and — crucially — **medium-preserving** (grade a
still → a still, grade a film → a film). It can't run until a producer has made the
pixels it transforms.

**The patterns that resolved it.**

- **Service Locator (Nystrom).** Our `renderer_for(medium)` registry already *is*
  one. Its **decorated-service** refinement (the GoF **Decorator**) is exactly a
  grade: a thing that wraps a provider, exposes the *same* interface, forwards, and
  post-processes. A decorator **shares the type of what it wraps** → a grade is
  medium-preserving, which is why keying it by an *output medium* (`Medium.GRADE`)
  was a category error: it's a **verb**, not an artifact **noun**, and would collide
  with a producer's medium (a graded STILL is still `STILL`).
- **Command (Nystrom / GoF).** "A reified method call." The grade *decision* is an
  **ordered stack of reified ops** — which the color grounding already demanded
  ("grade contrast first, colour second; an ordered stack, not a flat blob",
  Ch. 3–4). Reifying buys **serialization into the production plan** (`0005`) for
  free — the same decision-vs-executor split `edit.py` ↔ `cutter.py` already embody.

## Decisions

1. **Two-plane registry.** Producers stay keyed by `Medium` (`renderer_for`);
   **operators** get their own plane keyed by `Operation` (`operator_for`), because
   a medium-preserving transform is a different kind of thing than a medium-producing
   source. `render.py` now exposes both a `Renderer` protocol (`render(decision)`)
   and a `Transform` protocol (`apply(artifact, decision)`) — the `apply` signature
   makes the **1-media-in dependency explicit** instead of smuggling it inside the
   decision. `Cutter` stays a producer (a reducer that mints a distinct `FILM`); no
   forced migration.

2. **The grade decision is a reified `Command` stack** ([`grade.py`](../../sequitur/grade.py)),
   the color analogue of [`edit.py`](../../sequitur/edit.py): frozen op dataclasses
   (`Contrast` = lift/gamma/gain, `ColorBalance` = per-`TonalRange` RGB push,
   `Saturation`), a `Grade` aggregate that is ordered, `validate()`-able (bad params;
   the contrast-before-color rule), and `to_dict`/`from_dict`-serializable. No
   ffmpeg dependency — the model layer stays plan-serializable.

3. **The `Grader` is a medium-preserving `Transform`** ([`grader.py`](../../sequitur/grader.py)),
   the color analogue of [`cutter.py`](../../sequitur/cutter.py): it compiles the op
   stack into an ffmpeg filtergraph (`eq` / `colorbalance`) and runs it over an
   existing artifact — so **re-grading never re-invokes the (expensive,
   non-deterministic) generative backend**. `filtergraph()` is a pure function, so
   it's unit-testable without an ffmpeg binary.

4. **`Look` is an open preset library, not a closed taxonomy.** Creative looks are
   unbounded, so `Look` makes **no completeness claim** — it's the color analogue of
   the taxonomy's open-tag `Microgenre` (`0016`). The *comprehensive* vocabulary is
   the op basis; any look outside the presets is authored directly as a `Grade`
   (the analogue of hand-building a `Sequence`).

5. **Productions can define their own looks.** A named-look **registry**
   (`register_look` / `named_look` / `registered_looks`) lets a production name and
   reuse a `Grade` template when no preset fits. Because a look *is* a `Grade`, a
   custom look serializes into the plan (`0005`) for free; `Colorist.grade` accepts
   a `Look` **or** a registered name, and resolution returns a fresh copy so the
   template is never mutated.

6. **The `ColorTemperature` two-seat overlap is made explicit, not silently shared.**
   The Gaffer keeps capture-time `ColorTemperature` (in-camera white balance); the
   Colorist gets a **distinct grade-side `Cast`** vocabulary (`0020`'s flagged
   overlap). Same "warm/cool" language, different pipeline stage — no silent collision.

## Resulting state

- **New:** [`sequitur/crew/colorist.py`](../../sequitur/crew/colorist.py) (the
  `Colorist` role + `Look`/`TonalRange`/`Cast` vocabulary),
  [`sequitur/grade.py`](../../sequitur/grade.py) (the reified model + look registry),
  [`sequitur/grader.py`](../../sequitur/grader.py) (the ffmpeg transform), and
  [`tests/test_grade.py`](../../tests/test_grade.py) (8 smoke tests: vocabulary
  ownership, look→valid-ordered-grade, validate lints, dict round-trip, filtergraph
  compilation, operator-plane registration + protocol satisfaction, registry
  override, and the production look registry).
- **Changed:** [`render.py`](../../sequitur/render.py) gained the `Operation` enum,
  the `Transform` protocol, and the `operator_for` / `register_operator` /
  `registered_operations` operator plane. `crew/role.py` gained `Department.COLOR`.
  The package surface adds `Colorist` · `Look` · `TonalRange` · `Cast` · `Grade` ·
  `GradeOp` · `Contrast` · `ColorBalance` · `Saturation` · `Grader` · `Transform` ·
  `Operation` · `operator_for` · `register_operator` · `registered_operations` ·
  `register_look` · `named_look` · `registered_looks`.
- **New dependency:** `imageio-ffmpeg` (resolves the ffmpeg binary for the `Grader`);
  added to [`requirements.txt`](../../requirements.txt).
- **Green:** all five smoke suites pass (`test_prompt` 3 · `test_edit` 4 ·
  `test_engine` 4 · `test_render` 6 · `test_grade` 8 = 25). The retrofit is
  behaviour-neutral for existing callers.
- Docs reconciled: `architecture.md` (Colorist row → implemented; renderer-seam
  section → two planes), `README.md` (layout tree + status bullets), this `OVERVIEW`.

## Open threads

- **HSL / shape secondaries** — the second grade tier (Color Correction Handbook
  Ch. 5–6): a chroma/luma qualifier and geometric windows limiting a correction to a
  color range or region. New `GradeOp` types on the same stack; the `Grader` grows
  the matching ffmpeg filters.
- **The scope-reader `validate()` / broadcast-safe gate** — a *sensor/reader* transform
  (Ch. 2/10) that measures an image (waveform / vectorscope / parade) and backs a
  color QC gate, the color counterpart to `Sequence.validate()` and the Rose
  sound-layer validate. Distinct flavor from the `Grader` (reads, doesn't write).
- **Wire the Colorist into the assemble phase** — the `Engine`/`Director` currently
  reconcile a shoot-phase `Shot`; the Colorist (assemble phase) needs the
  assemble-phase behaviour to dispatch it, and a `Grade` bound to each graded `Clip`.
- **Ch. 9 shot matching** — grade an anchor clip, then a Colorist/Director reconcile
  matches the rest across a `Sequence` (the color analogue of the Editor's continuity
  check; Omni renders each shot with no shared look).
- Carried from `0021`: register `Composer`→Strudel (score) and the non-generative
  `SoundAnalyst` (audio MIR) backends; let roles *hold* their renderer through the
  registry; the `0005` Production binding; `PersonaJudgment` (**B**); the
  reconciliation sweeps.
