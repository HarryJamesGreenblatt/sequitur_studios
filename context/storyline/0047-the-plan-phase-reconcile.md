# 0047 — The plan-phase reconcile: a `Plan`, and a whole crew

> Date: 2026-08-15 · Focus: give the plan phase its **reconcile** — a `Director.plan`
> that fuses the Screenwriter's story descriptor and the Production Designer's design
> descriptor into a new **`Plan`** aggregate — and complete `full_crew()` across all
> three phases. The connective verb the dailies-model first slice needs. **Code.**

---

## What happened

The plan seats (`Screenwriter` `0035`, `ProductionDesigner` `0046`) each return a
*descriptor*, not a `Shot`, and were deliberately kept out of `full_crew()` because the
plan phase had **no reconcile** — the Director could fold the shoot crew into a `Shot`
(`0014`) and the assemble crew into a `Sequence` (`0023`), but nothing fused the two plan
descriptors. This session builds that missing verb, the third and last reconcile.

1. **A new plan aggregate — [`sequitur/plan.py`](../../sequitur/plan.py).** `Plan` is the
   plan-phase analogue of [`shot.py`](../../sequitur/shot.py) (the shoot aggregate) and
   [`edit.py`](../../sequitur/edit.py) (the assemble aggregate): a frozen-shaped dataclass
   carrying `scene`/`mood`/`aspect_ratio` plus two descriptor halves — `story` (the
   Screenwriter's taxonomy layers) and `design` (the Production Designer's visual concept +
   look). Unlike a `Shot`, a `Plan` is **not renderable** — it is the *intent* the later
   phases realise, and the source of the two dailies deliverables (treatment ← story,
   poster ← design).

2. **The reconcile — `Director.plan(brief, contributions) -> Plan`.** Mirrors
   `reconcile`/`assemble`: it groups each seat's owned fields, routing the Production
   Designer's slice into `design` and everything else into `story`. Because the two
   descriptors own **disjoint keys**, the grouping is loss-free (the same conflict-free
   merge the other two reconciles rely on). It returns a `Plan`, not a `Shot`.

3. **`Engine.plan(brief) -> Plan`.** The plan-phase analogue of `Engine.run` (shoot) and
   `Engine.assemble` (assemble): filter the crew to `Phase.PLAN`, collect each seat's
   `Contribution`, hand them to `Director.plan`.

4. **`full_crew()` now spans all three phases.** With every phase reconcilable
   (plan → `Plan`, shoot → `Shot`, assemble → `Sequence`), the default mount is
   `plan_crew() + shoot_crew() + assemble_crew()`. `run`/`assemble`/`plan` each filter by
   the active phase, so mounting every seat is harmless — the `0035`/`0046` "kept out of
   `full_crew`" caveat is now resolved.

5. **Tests + surface.** `Plan` exported from the package; `test_engine.py` gains two plan
   tests (the reconcile lands disjoint story/design halves; producer hints route to the
   right half). Suite: **test_engine 10**, all 10 modules green.

## Decisions

1. **A `Plan` is a descriptor pair, not a typed record (yet).** The plan seats already
   emit descriptor *dicts* (`0035` set that shape); `Plan` holds them as `story`/`design`
   dicts rather than forcing a premature `StoryDescriptor`/`DesignDescriptor` dataclass
   refactor. The two halves are the honest unit the deliverable producers consume.

2. **Route by seat, keep the halves.** Unlike `reconcile`/`assemble` (which flatten all
   fields into one aggregate), `plan` *preserves* provenance — story vs. design — because
   the two deliverables read different halves (the treatment reads story; the poster reads
   design). Routing is by the Production Designer's title; disjoint keys make it robust.

3. **Not renderable on purpose.** A `Plan` has no `execute` path. Its outputs are a
   *treatment* (text) and a *poster* (an image rendered from the design concept via
   `ImageStudio`) — the two producers built next — not a direct render.

## Resulting state

- **All three phases reconcile.** plan → `Plan`, shoot → `Shot`, assemble → `Sequence`;
  the crew engine is complete across the production timeline.
- **The dailies first slice is unblocked at the seam.** `Engine.plan` produces the intent;
  the treatment + poster producers can now read a `Plan` and file deliverables through the
  `Gate` (`0040`).

## Next

- **The two plan producers (the `0036` first slice):** a **treatment** from `plan.story`
  (human-readable, grounded Glebas + Directing Ch. 3–11) and a **poster** from
  `plan.design` (the visual concept as one evocative frame via `ImageStudio`), each filed
  through the `Gate`.
- Then the verdict → board binding (`0040` deferral) and the interactive dailies loop.
- **Deferred:** the sound layer's `Composer` + toaster-strudel (MCP) integration — parked
  until the baseline plan → shoot → assemble pipeline is proven end-to-end.

## Addendum — the two producers, built (same arc)

The producers landed in this same slice, so they ship here:

- **`Director.deliver_plan(plan, *, gate, treatment=None, out_path=None)`** — produces the
  plan phase's two dailies deliverables and files them through a `Gate`: a **treatment**
  (from `plan.story`) and a **poster** (from `plan.design`). Both tiers feed it — the
  deterministic **A** composers by default, a persona-authored `treatment` / a landed
  `visual_concept` when the **B** agents supply them (the A path is only the offline
  baseline).
- **`build_poster_prompt(plan.design, …)`** in [`prompt.py`](../../sequitur/prompt.py) —
  composes the visual concept into an image prompt (production art — *a scene of the
  world*, explicitly not a printed poster).
- **`Screenwriter.treatment(plan)`** — the deterministic treatment skeleton (the **B**
  agent narrates the real one).
- **CLI** [`scripts/deliver_plan.py`](../../scripts/deliver_plan.py) runs the slice
  plan → {treatment + poster} → gate end-to-end.

**Coherence fix (persona wiring).** The first tier-A run produced a rambling treatment
(taxonomy metadata pasted as prose) and a blank-concept poster (the heuristic leaves
`visual_concept` empty). The fix wired `deliver_plan` to accept persona-authored input and
proved the loop live: dispatching the **Screenwriter** and **Production Designer**
subagents produced a coherent treatment and a purposeful concept frame — the tier-B path
is where quality lives; tier A is the deterministic stub. (`build_key_art_prompt` also
lands here — the composer the KeyArtist skill directs in `0048`.)

