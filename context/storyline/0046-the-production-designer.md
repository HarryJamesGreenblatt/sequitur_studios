# 0046 — The Production Designer: the art department, in code

> Date: 2026-08-15 · Focus: build the **Production Designer** — the plan-phase art
> department head — as a code seat (`crew/production_design.py`) plus its persona twin
> (`production_designer.agent.md`), grounded in the just-abridged **Art Direction
> Handbook** (Rizzo, `0044`/`0045`). The last unbuilt crew seat. **Code.**

---

## What happened

With the grounding library complete (nine abridged sources), the work turns to code. This
session builds the seat the Rizzo abridgement unlocked, following the `0035` pattern exactly
(the Screenwriter): a **plan-phase, vocabulary-only** role whose `Contribution` is a
*descriptor*, not a `Shot`, plus a persona agent twin.

1. **The code seat — [`crew/production_design.py`](../../sequitur/crew/production_design.py).**
   A `ProductionDesigner(Role)` in a new **`Department.ART`**, `Phase.PLAN`. It owns the
   design vocabulary reduced from Rizzo to the axes that survive the jump to a generative
   image backend:
   - **`ConceptStance`** (2 — Ch. 4): `UNDERSCORE` / `CONTRAST` (does the design echo the
     scene's emotion or push against it).
   - **`MediumLook`** (3 — Ch. 3): `FILM` / `VIDEO` / `DIGITAL` (film and video are
     physically different images; a real look, not a filter).
   - **`EraMarker`** (7 — Ch. 3): `OPTICAL_TOY` … `NTSC_COLOR` / `DIGITAL_WEB` /
     `CONTEMPORARY` — Rizzo's *medium*-era markers (not art periods; palette/period grading
     stays the Colorist's).
   - **`SetKind`** (2 — Ch. 5): `INTERIOR` / `EXTERIOR`.
   - plus two **open** descriptor fields: `visual_concept` (a `str` — the single central
     metaphor, Ch. 4's spine) and `motifs` (a `list[str]` — the research "wall of icons").

2. **The heuristic leaves the concept blank.** The deterministic **A** lands only the
   structural axes (a clean, contemporary interior that underscores the scene); the central
   `visual_concept` defaults to `""`. That is deliberate — it is the payload the machine can
   *classify* but not *narrate*, so the **persona B** fills it (the treatment-vs-descriptor
   split, mirroring the Screenwriter).

3. **Wired into the plan crew, kept out of `full_crew`.** `plan_crew()` now seats
   `[Screenwriter(), ProductionDesigner()]`; both stay out of `full_crew()` because a
   descriptor is not `Shot`-reconcilable — the plan-phase reconcile is a later pass. Exports
   added to the package surface; `tests/test_production_design.py` (5) asserts the seat, the
   closed-axis membership, the neutral heuristic, hint overrides, and that `plan_crew` seats
   both. **All 10 test modules green.**

4. **The persona twin — [`production_designer.agent.md`](../../.github/agents/production_designer.agent.md).**
   A tier-B VS Code agent grounded in the Rizzo `reference/`, bound to the code's enums, that
   lands the central visual concept and the structural axes. The **Director agent** gained a
   plan-phase dispatch step for it (seeded by the Screenwriter's descriptor, since the concept
   is *downstream of the story*, Ch. 1). Seven agents now sit beside the Director.

## Decisions

1. **PD owns the concept; code owns the realisation.** Rizzo's Ch. 1 split maps cleanly onto
   the two tiers: the Production Designer owns the *visual concept*; `build_prompt` +
   `ImageStudio` are the *realisation* (the Art-Director half). So the seat's payload is the
   concept, and the image pipeline stays the execution plane.

2. **Only design intent transfers.** A generative backend has no location scout, no
   construction budget, no wild walls — the whole location-vs-build economy (Ch. 5) has no
   analogue. The vocabulary is exactly what survives: concept, medium/era *look*, stance,
   interior/exterior.

3. **Era is design intent; grade is the Colorist.** `EraMarker` names the era a concept
   *evokes* (a recognizable "meme" token); the actual palette/balance is the
   [`Colorist`](../../sequitur/crew/colorist.py)'s grade. Overlap logged (Rizzo Ch. 3 ↔ Van
   Hurkman), kept on the concept side of the seam.

4. **New `Department.ART`.** The art department had no code home; added `Department.ART`
   (Appendix D places the Production Designer level with the Director). No other seat moves.

## Resulting state

- **The last crew seat exists.** Plan (Screenwriter + Production Designer), shoot
  (Cinematographer/Gaffer/Key Grip), assemble (Editor/Colorist) — every modeled department
  now has a code seat and a persona twin. Remaining crew work is a `StoryboardArtist` seat and
  a plan-phase reconcile.
- **Descriptor, not `Shot`.** Like the Screenwriter, the Production Designer's `Contribution`
  is a design descriptor; the plan-phase reconcile that turns {story descriptor + design
  descriptor} into downstream briefs (and a treatment + poster deliverable) is the next step.

## Next

- The **`0036` first slice** is now unblocked on both producers: the Screenwriter treatment
  (human-readable, grounded Glebas + Directing Ch. 3–11) and the Production Designer's concept
  → a **poster** ("the PD's look as one evocative frame") → the `Gate`.
- A plan-phase reconcile (descriptor → `Brief` overlay → `build_image_prompt`), then the
  `StoryboardArtist` seat, then a generated vocabulary card (the hand-listed enums in the
  agents are the drift risk).
