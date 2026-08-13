# 0023 — The Assemble Phase, and a True-to-Form Grade

> Date: 2026-08-12 · Focus: **code** — two advances committed together:
> **(1)** made the crew engine **phase-aware** so the just-seated `Colorist` (and the
> `Editor`) actually *participate* — `Engine.assemble` dispatches the post crew and
> `Director.assemble` reconciles them into a **graded edit `Sequence`**; and
> **(2)** replaced the grade executor's placeholder ffmpeg filters with the
> industry-standard **3D-LUT** path (colour-science → `.cube` → ffmpeg `lut3d`),
> **superseding `0022`'s `eq`/`colorbalance` filtergraph**.

---

## Part 1 — Wiring the assemble phase

`0022` seated the `Colorist` but left it inert — the `Engine` only knew the **shoot**
phase (crew → a single `Shot`). The assemble phase is a *different shape*: its inputs
are a set of shots (coverage) and its output is a **`Sequence`** (an EDL) carrying a
per-clip **grade**, not a field-merge into one object. This session taught the engine
that second phase.

- **`Brief` gained `shots`** — the coverage to assemble (empty for the shoot phase).
- **`Editor.heuristic`** now proposes the cut structure over that coverage: open on a
  `FADE_IN`, then straight `CUT`s with an `INFORMATION` reason (`cut` field).
- **`Colorist.heuristic`** now returns the sequence's **base `grade`** (its `Look`
  compiled to a reified `Grade`) instead of a bare look enum.
- **`Director.assemble`** reconciles the two disjoint contributions (`cut` + `grade`)
  into a `Sequence`: one act → one scene → a `Beat` per shot, each `Clip` carrying a
  **copy** of the base grade.
- **`Engine.assemble`** filters the crew to assemble-phase roles, collects their
  contributions, and hands them to `Director.assemble`.
- **`Clip` gained a `grade` field** — the colour decision rides *in* the EDL (pure
  model, no render dependency), so a graded `Sequence` serialises into a production
  plan (`0005`) and stays backward-compatible with the `Cutter` (which ignores it).

### Decisions

1. **Phase-aware Director, not one overloaded `reconcile`.** `reconcile` (shoot → a
   `Shot` via disjoint field-merge) and `assemble` (post → a `Sequence`) are genuinely
   different reconciliations, so they are **separate methods**. The engine still just
   *routes* by phase (the `0008` "agency lives in a component, the engine only
   dispatches" rule holds).

2. **The grade rides in the `Clip`, not a parallel structure.** A graded `Sequence` is
   one object: `Clip.grade` sits alongside `Clip.source`. Both `edit.py` and `grade.py`
   are render-dependency-free pure models, so the coupling is a `TYPE_CHECKING`-only
   import and the EDL stays the single serialisable decision artifact for the phase.

3. **One base look for the whole sequence — the anchor.** The Colorist contributes a
   single base grade copied to every clip. This is Ch. 9's *starting point* — grade an
   anchor, then match the rest; **per-shot matching is a later refinement**.

4. **The Engine's default crew is now the `full_crew`** (shoot + assemble). `run` and
   `assemble` each filter by phase, so a full mount is backward-compatible. Added
   `assemble_crew()` and `full_crew()` beside `shoot_crew()`.

---

## Part 2 — A true-to-form grade (superseding `0022`'s filtergraph)

`0022` shipped the `Grader` compiling the op stack into an ffmpeg **`eq`/`colorbalance`**
filtergraph. Those filters are **not calibrated to any colour standard** — ffmpeg's own
transfer curves and zone falloffs — so it was, honestly, *arbitrary preset knobs*: a
placeholder that proved the seam, not a real grade.

A design discussion (recorded in-session) first asked whether colour even belongs in
**post** for a *generative* pipeline — where leverage is at the prompt/seed, not in
post-hoc correction. The conclusion: **keep post-grade** (faithful to the craft, and it
uniquely allows a content-preserving tweak without re-rolling a non-deterministic
generation), but **make the executor legitimate**. This part does that.

- **New [`lut.py`](../../sequitur/lut.py)** — the **authoring** stage. Bakes a grade's
  **primaries** into a `colour.LUT3D` and writes a spec-correct Iridas **`.cube`** via
  **colour-science**: `Contrast` → **ASC CDL** slope/offset/power (`gain`/`lift`/`gamma`),
  `ColorBalance` → per-zone RGB offset weighted by a smooth luma membership, `Saturation`
  → Rec. 709 luma lerp. A **pure function** — unit-testable without ffmpeg.
- **Reworked [`grader.py`](../../sequitur/grader.py)** — the **execution** stage:
  author `.cube` → apply with ffmpeg **`lut3d`**. An identity grade short-circuits to a
  copy (no needless re-encode); the `.cube` is persisted beside the output as a
  **portable look** artifact.

### Decisions

1. **colour-science over hand-rolled numpy.** The whole point of the upgrade is
   *correctness*, and the two standards-critical pieces — the ASC CDL maths and the
   `.cube` format (domain, `LUT_3D_SIZE`, red-fastest node order) — are notoriously
   easy to "cook" subtly wrong. A battle-tested library at the authoring step is *more*
   aligned with the goal, not gratuitous. colour-science authors; ffmpeg applies.

2. **LUT for primaries, masked passes for secondaries.** Contrast, colour balance, and
   saturation bake cleanly into a global 3D LUT. HSL qualification and shape windows are
   spatially/chroma-gated and **cannot** live in a global LUT — exactly how real tools
   treat them (LUT = the primary look; secondaries are separate nodes). So the LUT is
   the T1 scope; **secondaries stay a deferred, separate masked-pass concern**.

3. **A contained executor swap — the seam earned its keep.** The `Grade` decision model,
   the `Colorist`, and the two-plane registry are **untouched**. Fidelity was always an
   *executor* concern behind `Operation.GRADE`; upgrading the `Grader`'s internals from
   arbitrary filters to LUT+`lut3d` touched no role and no decision — precisely what the
   `0021`/`0022` seam was built to absorb.

## Resulting state

- **New:** [`sequitur/lut.py`](../../sequitur/lut.py) (grade → `LUT3D` → `.cube`).
- **Changed (assemble):** `crew/role.py` (`Brief.shots`), `crew/editorial.py`
  (`Editor.heuristic`), `crew/colorist.py` (`Colorist.heuristic` → base grade),
  `crew/director.py` (`Director.assemble`), `crew/engine.py` (`Engine.assemble`,
  `assemble_crew`, `full_crew`, full default mount), `edit.py` (`Clip.grade`). Package
  surface adds `assemble_crew` · `full_crew`.
- **Changed (grade executor):** `grader.py` rewritten onto the LUT path (the
  `filtergraph()` method is **gone**); `Grade`/`Colorist`/registry unchanged.
- **New dependency:** `colour-science` (LUT authoring + `.cube` I/O) and explicit
  `numpy`, beside `imageio-ffmpeg`.
- **Tests:** `tests/test_engine.py` gains `test_engine_assembles_a_graded_sequence`
  (4→5); `tests/test_grade.py`'s filtergraph test is replaced by a LUT-**bake** test
  (still ffmpeg-free — asserts identity→identity lattice, CDL pins black/white,
  saturation collapses to grey). All **26** smoke tests green (`test_prompt` 3 ·
  `test_edit` 4 · `test_engine` 5 · `test_render` 6 · `test_grade` 8). Verified
  **end-to-end**: a NOIR grade on a real image authored a `.cube` and ffmpeg `lut3d`
  applied it, desaturating `[126,63,30]`→`[104,79,65]` (channels converging toward luma).
- Docs reconciled: `architecture.md`, `README.md`, `OVERVIEW` (grade executor now
  described as LUT-based, not the `0022` filtergraph); a forward-pointer added to `0022`.

## Open threads

- **Secondaries as masked passes (not LUT)** — HSL qualification (Ch. 5) + shape windows
  (Ch. 6) as new `GradeOp` types executed by the `Grader` as *separate* qualified/masked
  ffmpeg passes *around* the primary LUT (they can't bake into a global 3D LUT).
- **The scope-reader `validate()` / broadcast-safe gate** (Ch. 2/10) — a *reader*-flavor
  transform (ffmpeg `waveform`/`vectorscope`/`histogram`) backing a colour QC gate.
- **Bind a local-folder `Production` (`0005`)** in place of the bare `Brief` — the
  coverage `shots` and look/cut hints come from a plan; the graded `Sequence` writes back.
- **Per-shot grade matching (Ch. 9)** — grade an anchor clip, then a Colorist/Director
  reconcile matches the rest across the `Sequence`, instead of one uniform base look.
- **A real cut-decision heuristic** — the `Editor.heuristic` is the trivial
  all-straight-cuts assembly today; the Ch. 5 six-motivator engine is the next pass.
- **`PersonaJudgment` (B)** — the assemble roles reason with `HeuristicJudgment` (A) today.
- Carried: let roles *hold* their renderer through the registry; register
  `Composer`/`SoundAnalyst`.
