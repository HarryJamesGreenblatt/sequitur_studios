# 0013 — The Editor takes a seat: re-seating the edit vocabulary

> Date: 2026-08-08 · Focus: the second crew-engine pass (`0008`) — re-seat
> `edit.py`'s vocabulary under an **Editor** role, mirroring the camera/electric/grip
> move in `0012`. A **code** entry; the editorial department now has a first-class
> seat, and the post model reads as the editorial analogue of `shot.py`.

## What happened

`0012` un-flattened `grammar.py` into three shoot-phase roles. `edit.py` was the
obvious next re-seat, but it differs from the camera carve: it is *vocabulary plus a
model* — three enums (`Transition`/`EditReason`/`EditCategory`) **and** the
shots → scenes → acts EDL with real behaviour (`timeline()`/`validate()`). So the
split follows the same shape as the shot layer:

- **Vocabulary + role → [`crew/editorial.py`](../../sequitur/crew/editorial.py):**
  the three enums moved **verbatim**, plus a new **`Editor`** role
  (`Department.EDITORIAL`, `Phase.ASSEMBLE`, `vocabulary = (Transition, EditReason,
  EditCategory)`).
- **Aggregate + logic stays in [`edit.py`](../../sequitur/edit.py):** `Clip`,
  `Edit`, `Beat`, `Scene`, `Act`, `Sequence`, `TimelineEntry`, and the
  `timeline()`/`runtime`/`validate()` methods. `edit.py` now imports its vocabulary
  from `crew.editorial` and reads as the **editorial counterpart to `shot.py`** — the
  model the Editor composes, cleanly separated from the words it composes with.

This makes the parallel exact: `crew/camera.py` : `shot.py` :: `crew/editorial.py` :
`edit.py`.

## Decisions

1. **The Editor owns the *vocabulary*; the model is the aggregate it composes.** Just
   as `Shot` (the aggregate) is not the Cinematographer, the `Sequence`/EDL model is
   not the Editor — it is the editorial canvas. `timeline()`/`validate()` stay on the
   `Sequence` aggregate (domain logic on the data), consistent with vocabulary-only
   roles; a later `Judgment` will *call* `validate()`, not absorb it.
2. **No empty Colorist/SoundEditor.** `0008` names them as also-editorial, but they
   own nothing in `edit.py` (Colorist ≈ colour, currently with the Gaffer;
   SoundEditor is sound department). Per the "don't stub the matrix" rule, only
   `Editor` — which has real vocabulary today — was created.
3. **Public surface preserved; imports unchanged for consumers.** `__init__.py` now
   sources `Transition`/`EditReason`/`EditCategory` from `crew.editorial` and the
   model classes from `.edit`, and exports **`Editor`**. Because `edit.py` re-exports
   the enums, `cutter.py`'s `from .edit import Sequence, Transition` still resolves —
   no executor change.

## Resulting state

- Two departments now seated as roles: shoot-phase `Cinematographer`/`Gaffer`/
  `KeyGrip` (`0012`) and assemble-phase **`Editor`** (`0013`). Their aggregates are
  `shot.py` and `edit.py` respectively.
- New guard test [`tests/test_edit.py`](../../tests/test_edit.py): exercises
  `timeline()` overlap (only handle transitions shift the incoming clip),
  `validate()` (missing dissolve handles + reasonless cut are flagged), and the
  Editor's vocabulary. Both suites green (`test_prompt` 3, `test_edit` 4); no lint
  errors.

## Open threads

- **Add the `Role` behaviour layer** — with camera *and* editorial vocabulary now
  seated, the next pass is `Judgment` (heuristic **A**) + a `Contribution` type + the
  **`Director`** reconciler over a dumb `Engine`, then a minimal in-memory Production
  (later the `0005` local-folder `ProductionProvider`). The Editor's `Judgment` can
  wrap `Sequence.validate()` as its first heuristic.
- **SoundMixer** slots in once it has a real judgment (already has `SpeechRenderer`
  to wield); **Colorist**/**SoundEditor** wait for owned vocabulary.
- **`Renderer` protocol** (deferred `0006`, three backends) — still independent and
  worth formalizing.
- **Reconciliation sweep (carried):** the edit reference chapters' "Studio
  application" tie-ins can now point at `crew/editorial.py` + `edit.py`; realign when
  the role behaviour settles.
- Carried: provider seams (`0005`); the cut-decision engine over the model (`0007`);
  toaster-strudel MCP (`0009`).
