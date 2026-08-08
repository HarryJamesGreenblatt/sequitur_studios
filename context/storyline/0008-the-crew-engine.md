# 0008 — The crew engine: roles as behavior, the Production as container

> Date: 2026-08-08 · Focus: decide **how the department/role model becomes code** —
> the long-deferred "roles first-class" question (`0002`). Converged on a **crew
> engine**: dumb dispatch + specialized role-components + a human **Producer** seat,
> with the **Production** (the `0005` PM-backed instance) as the container. This is a
> **design/decision** entry — the shape we build to, recorded before building so the
> future doesn't drift back into a monolith.

## The problem it fixes

The architecture *describes* departments/roles ([`architecture.md`](../architecture.md)'s
phase → department → grounding → code table) but the code doesn't *embody* them.
`grammar.py` is a **flattened crew**: its "orthogonal layers" (framing/angle = camera,
lighting = electric, movement = grip) are three departments collapsed into flat
static enums in one module. `edit.py` is the same for the editorial crew. There is no
seam where a role owns its concern + its grounding + its judgment. `0002` deferred
making roles first-class *"until a second department (editorial) exists to justify
it"* — `edit.py` **is** that second department, so the deferral has expired.

## Decisions

1. **Roles are classes; grammar stays enums.** Enums are the *closed vocabulary*
   (`ShotSize`, `LightScheme`, `Transition` — the choices). A **`Role`** is the
   *chooser*: an abstract base + concrete subclasses (`Cinematographer`, `Gaffer`,
   `KeyGrip`, `Editor`, `Colorist`, `SoundEditor`), grouped by **`Department`**. A
   role **owns and wields a slice of the grammar** — `grammar.py`/`edit.py` enums get
   *re-seated under the role that owns them*, not deleted. (Matches the repo's own
   "abstract base + nested concretes" preference.)

2. **Judgment is a swappable strategy — this is the A→B seam.** A role doesn't hard-
   code its reasoning; it holds a **`Judgment`**: `HeuristicJudgment` (**A** —
   deterministic, no LLM), `PersonaJudgment` (**B** — an LLM persona reasoning over
   the role's *scoped* grounding), or `HumanJudgment` (**HITL**). Same `propose()`
   signature, so any single role can be upgraded to a persona — or hand-driven by a
   human — individually. **A is the foundation for B.**

3. **Three authority tiers — this fills the Producer gap.** `architecture.md` gives
   the **Producer** a row but no code analogue, while the **Director** has plenty.
   That is the signal: the Producer was never meant to be code — it is the **human
   seat (HITL)**.
   - **Producer = HITL (the user)** — owns *what* & *whether*: brief, constraints,
     greenlight, approval. Works the board (below); does not live in the engine.
   - **Director = agent** — owns *how*: reconciles the crew into the vision. It is a
     **`Role`** (the reconciler), not the container — so agency lives in a component.
   - **Crew = role-components** — each decides its own concern in isolation.

4. **The container is the Production, not a new `Unit`.** The dumb container that
   wires the crew is **not** a fresh abstraction — it is the **Production** already
   defined in `0005` (a plan whose buckets = department layers, each holding the four
   faces). Inventing a `Unit` to "group the crew" would duplicate that. So: **the
   Production encapsulates the crew.** Nystrom's Component Pattern, in its data-
   oriented (ECS) form:
   - **Entity = Production** — dumb per-instance *data* (the department buckets).
   - **System/behavior = the engine's Roles** — singular, shared across productions.
   - **Dumb dispatch = the engine (driver-client)** — mounts a Production, dispatches
     the active crew for a phase, lets the Director reconcile. **No film logic in the
     container or the dispatcher.**

5. **Behavior vs. state split (maps onto `0005`'s engine-vs-instance).** Role
   *behavior* (the class, its `Judgment`, its grounding) lives in the **engine**
   (singular). Role *state* (that role's seeds/history/guidance/output) lives in the
   **Production** bucket (per-instance). The engine binds behavior to state at runtime
   via the `0005` `ProductionProvider` seam.

6. **The Production is the PM board — the keystone.** Because the container is the
   `0005` Production, and its buckets are the `ProductionProvider`'s per-department
   items, the **Production *is* the Planner/ADO/GH-Projects board**. The **Producer
   (human) works the board** — literally what a producer does (greenlight, brief =
   seeds, approve = history) — and the **agent crew executes against its buckets**.
   This is the payoff of the whole "reusable framework whose project state lives in
   the PM tool" goal: the container is the PM-backed Production, not an in-memory
   object.

7. **Phase terminology fix.** "Production" now means the **instance/board**, so stop
   using it for the phase. Use the phase verbs already in `architecture.md`:
   **plan · shoot · assemble**. A Production *moves through* plan→shoot→assemble; a
   phase is just which crew is on call — **not** a separate container. (Retires the
   `ProductionEngine`/`PostProductionEngine` split: one engine, one Production,
   phase-activated crews.)

## Resulting shape (agreed, mostly unbuilt)

```
Producer (HITL) ── works ──▶ Production (PM board; per-department buckets = 0005 faces)
                                        ▲   ▼  (ProductionProvider seam)
Engine (singular, dumb dispatch) ── mounts, dispatches active crew per phase
   └─ Role (behavior) ×N  ──▶ Director (role: reconcile) ──▶ decision → written to bucket
        └─ Judgment: Heuristic (A) │ Persona (B) │ Human (HITL)
```

- **Grammar layers already exist** to be re-seated under roles: `grammar.py`
  (camera/electric/grip vocab) and `edit.py` (editorial vocab; note `movie.py` was
  renamed to `edit.py`, with the MoviePy executor split into a separate `cutter.py`).
- **Nothing about the renderer plane changes** — `Studio`/`ImageStudio`/`Cutter`
  stay the *execution* plane; roles are the *decision* plane.

## Open threads

- **Build phase A** — `Role`/`Judgment`/`Contribution` + a dumb engine over a
  **local-folder Production** (`ProductionProvider` impl #1 from `0005`), re-seating
  `grammar.py`'s enums under `Cinematographer`/`Gaffer`/`KeyGrip` and `edit.py`'s
  under `Editor`/`Colorist`/`SoundEditor`, with a `Director` reconciler. No LLM.
- **Phase B later** — back a role's `Judgment` with an LLM persona over its scoped
  grounding (the squeeze that's worth it once A proves the seam).
- **Wire the Production to a real PM board** — GH Projects v2 vs. ADO (`0005`),
  once a first real production exists; local-folder provider stands in.
- Carried: build the `edit.py` post layer proper (`0007`); the reconciliation sweep;
  the provider seams; broader discipline sources.
