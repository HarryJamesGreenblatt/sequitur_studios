# 0012 — The crew, un-flattened: grammar.py becomes roles

> Date: 2026-08-08 · Focus: begin the crew engine (`0008`) by its most concrete
> step — **decompose the source-named `grammar.py` into department roles**. This is
> a **code** entry: the first structural move of phase A, done behaviour-neutrally
> and guarded by a new smoke test.

## What happened

`grammar.py` was named after the *book* (*Grammar of the Shot*), not the
responsibility, and it **fused three departments** — camera, electric, grip — into
one flat module of enums. This session re-seated that vocabulary under the roles
that own it, establishing the shared seat every future role will fill.

1. **New `crew/` package + a thin `Role` base.**
   [`crew/role.py`](../../sequitur/crew/role.py) defines `Role` (the *chooser* that
   owns a slice of the grammar) plus the axes that place it: `Department`
   (camera/electric/grip/editorial/sound) and `Phase` (plan/shoot/assemble/ship).
   Per `0008` the base is deliberately thin — a role only *declares* what it owns
   (`title`, `department`, `phase`, `vocabulary`); the reasoning layer (`Judgment`)
   and the `Director` reconciler are the next pass.

2. **Three shoot-phase roles, each owning its verbatim vocabulary.**
   [`crew/camera.py`](../../sequitur/crew/camera.py) → **Cinematographer** (framing
   Ch. 1–2 + lens/focus Ch. 3: `ShotSize`, `SubjectView`, `CameraAngle`,
   `ShootingStyle`, `Composition`, `FocalLength`, `DepthOfField`);
   [`crew/lighting.py`](../../sequitur/crew/lighting.py) → **Gaffer** (Ch. 4:
   `LightScheme`, `LightQuality`, `LightDirection`, `ColorTemperature`, + the
   `eye_light` flag); [`crew/grip.py`](../../sequitur/crew/grip.py) → **KeyGrip**
   (Ch. 6: `CameraMovement`, `MotionSpeed`). The enum bodies moved **verbatim**
   (phrases/intents/codes unchanged) — this is a re-home, not a rewrite.

3. **`Shot` extracted to its own module.** [`shot.py`](../../sequitur/shot.py) now
   holds the aggregate spec the three crews compose into — kept **whole** (one flat
   canvas, not one fragment per department) since it is the unit the renderers and
   `build_prompt` consume.

4. **Import sites rewired; `grammar.py` deleted.** `prompt.py`, `edit.py`,
   `image.py`, `studio.py` now import `Shot` from `.shot`; `__init__.py` sources the
   vocabulary from the `crew` package and re-exports the same names **plus** the new
   crew classes (`Role`/`Department`/`Phase`, `Cinematographer`/`Gaffer`/`KeyGrip`).
   The public surface (`__all__`) kept every prior name, so `scripts/generate.py`
   and the CLI are untouched.

5. **Guarded and proven behaviour-neutral.** Added the first test —
   [`tests/test_prompt.py`](../../tests/test_prompt.py) (runs bare or under pytest) —
   asserting the prompt builders against the *public* surface so it survives internal
   moves. Captured the exact `build_prompt`/`build_image_prompt` output **before** the
   refactor and diffed **after**: `IDENTICAL`. CLI dry-run and role introspection
   both verified; no lint errors.

## Decisions

1. **Roles are classes; grammar stays enums.** The classes we added are the
   *owners* (roles), not a re-typing of the vocabulary. Enums remain the right shape
   for a closed vocabulary; each is now homed under the role that wields it. This is
   `0008`'s "roles are classes; grammar stays enums" made literal.

2. **Vocabulary-only in this pass; behaviour next.** No `Judgment`/`Director`/engine
   yet — the roles declare ownership and nothing more. This kept the change small,
   reviewable, and provably output-neutral, and it sets the seat that Editor,
   SoundMixer, and the Director drop into later with zero reorg.

3. **Concern-named modules, module-level enums.** Enums live at module level in
   their concern file (`from .crew.camera import ShotSize` still resolves after a
   mechanical move) rather than nested under the role class — lowest churn, and the
   file name already carries the ownership signal.

4. **Don't stub the whole matrix.** Only roles with real vocabulary today were
   created (Cinematographer/Gaffer/KeyGrip). Editor (re-seat `edit.py`), the sound
   roles, Colorist, and the pre-pro roles are deferred until they have code/grounding
   to own — an empty `Role` subclass is noise.

## Resulting state

- `sequitur/crew/` (`role`, `camera`, `lighting`, `grip`) + `shot.py` replace the
  flat `grammar.py`. Three roles expose their owned `vocabulary`; the public API and
  every prompt are byte-for-byte unchanged. First test suite entry exists.

## Open threads

- **Crew engine, next passes:** re-seat `edit.py` → **Editor** (bigger — model +
  `validate()`, not just enums); then add the `Role` **behaviour** layer
  (`Judgment`: heuristic A) and the **`Director`** reconciler; then the `Engine` over
  a minimal in-memory Production, later the `0005` local-folder `ProductionProvider`.
- **SoundMixer** slots in once it has a real judgment (it already has
  `SpeechRenderer` to wield).
- **`Renderer` protocol** (deferred `0006`, now three backends) — still worth
  formalizing; independent of the crew work.
- **Reconciliation sweep (carried):** the reference chapters' "Studio application"
  tie-ins still say `grammar.py`; realign them (and the appendix-D map) when the role
  behaviour settles.
- Carried: provider seams (`0005`); the post cut-decision engine (`0007`);
  toaster-strudel MCP (`0009`).
