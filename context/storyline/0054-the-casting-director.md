# 0054 — The Casting Director: the cast axis, casting as design *and* selection

> Date: 2026-08-16 · Focus: close a skip in the plan slice — the pipeline named a
> character (Nora) and rendered her, but nobody ever *cast* her, so every render invented
> a different Nora. Build the **Casting Director** seat and the **`Character` / `Actor`**
> entities: the missing **cast axis**, and casting modelled as both a **design** and a
> **selection**. **Phase 1 (entities + seat + agent); the render/selection loop is next.**

---

## What happened

The Producer caught a real gap. The plan phase produced a treatment (Story), a world
concept (Art), and key art (Marketing) — but between "the Screenwriter names Nora in prose"
and "the KeyArtist renders a woman," there was **no casting or character design**. Nora
lived only as a word in the treatment; each render re-invented her from the model's whims.
In real production an entire set of processes sits in that gap (casting, costume, hair &
makeup); in a **generative** studio they collapse into one crucial artifact — a **locked
character reference** every downstream render conditions on. That reference is the
generative analogue of casting an actor, and it's the consistency backbone the studio was
missing.

1. **Casting is a distinct plane, not part of the PD.** The Production Designer owns the
   **world** (Rizzo Ch. 1 is explicit); casting owns the **people**. The grounding was
   already staged and unused: the architecture had flagged a *"CASTING/ACTORS dimension
   (Directing 18–20), unmodelled."* Rabiger Ch. 18 even anticipates generative casting — it
   frames casting as *developmental* ("what would this actor *give* the film?"), prescribes
   **abundance** (several candidates to choose from), lists the transferable *suitability*
   axes, and flags **voice** as a first-class casting choice (the through-line to
   `SpeechRenderer`).

2. **Casting is a *design* **and** a *selection*.** The naming tension — "Character
   Designer" (accurate: it's a design) vs. "Casting Director" (the intent) — dissolves by
   making it both, in sequence, exactly as real casting works: **design** the role →
   generate candidate **embodiments** (the audition) → **select** one (the Producer's call).
   The selection makes "casting" literally true, not a metaphor — and it *is* the first
   concrete instance of the verdict loop.

3. **The cast is a second diegetic axis — it needs its own entities.** A character isn't a
   node under a scene; it cuts **across** `Cut → Act → Scene → Beat → Shot` (a protagonist
   appears in many scenes). It doesn't fit any existing category (not a `Deliverable`) — so,
   like `Cut` and the marketing plane before it, it gets first-class representation. And the
   selection process *needs two* entities, mirroring casting's central relation — **an Actor
   plays a Character**:
   - **`Character`** — the diegetic **role**: name, dramatic function, essence, plus the
     grounded casting brief (`Billing`, `AgeBand`) it's cast *for*, its `candidates` (the
     audition), and its `cast` (the chosen embodiment).
   - **`Actor`** — a generated visual **identity**: a `look` + a `reference` image (+ a
     `voice`). Many audition for one Character; one is cast. Its `reference` is the
     character's locked look. (An `Actor` is reusable — a future studio **repertory** — but
     that's deferred.)

## Decisions

1. **Seat name = Casting Director** (owns the whole process); "character design" is its
   first step. Grounded in Directing Ch. 18–20, `Department.CASTING` (new), `Phase.PLAN`.
2. **Two entities, not one.** A single `Character`-with-a-look can't represent the audition
   or the selection; the `Actor` entity is what makes casting-as-selection expressible.
3. **The cast is the Plan's third axis.** `Plan` gains `cast: list[Character]` beside
   `story`/`design`; `Director.plan` routes the Casting Director's contribution there
   (disjoint, loss-free, like the other two halves).
4. **Vocabulary + heuristic, like the other plan seats.** The seat owns the closed axes
   (`AgeBand`, `Billing` — Ch. 18 *suitability* / *billing*); look/essence/wardrobe/voice are
   open, narrated by the persona **B** from the treatment. The heuristic **A** can't read the
   treatment, so it leaves the cast empty (hints-overridable) — the same descriptor-vs-
   narration split the Production Designer draws. Only what *transfers* to a generated
   identity is modelled; the actor-as-person axes (directability, commitment) are dropped.
5. **The seat designs and auditions; it never selects.** The agent proposes 2–3 candidate
   `Actor` looks per principal (abundance) and leaves `cast` empty — the Producer's choice.

## Resulting state

- **New code:** [`sequitur/cast.py`](../../sequitur/cast.py) (`Character` + `Actor`),
  [`crew/casting.py`](../../sequitur/crew/casting.py) (`CastingDirector` + `AgeBand` +
  `Billing`), `Department.CASTING`, `Plan.cast`, the plan reconcile + `plan_crew` routing,
  package exports, and the agent twin
  [`casting_director.agent.md`](../../.github/agents/casting_director.agent.md). Eight agents
  now. `tests/test_casting.py` (7); 12-module suite green.
- The plan phase now has a complete cast axis in code — Nora can be *designed* and *cast*
  before she's rendered.

## Next

- **Phase 2 — casting as selection (the verdict loop's first instance):** render each
  principal's candidate `Actor`s via `ImageStudio` (the audition), file them through the
  `Gate`, and let the Producer **select** one — binding the cast `Actor` and locking its
  reference.
- **Phase 3 — thread + generalize:** condition key art / PD / shots on the cast reference
  (the consistency payoff), then generalize the verdict loop so an approved plan advances to
  script + storyboard.
- **Board:** a **Casting** area + (later) whether `Character` / `Actor` want WIT
  representation so the audition is reviewable on the board (the `Cut` question again).
- Deferred: an `Actor` **repertory** reusable across productions; `voice` → `SpeechRenderer`.
