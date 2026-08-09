# Chapter 8 — Case Studies

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy*, Ch. 8.
> **Scope:** all six layers applied **together** — four comparisons of acclaimed
> films, plus three reimaginings of *Romeo & Juliet* — showing the taxonomy as both
> an *analytic* and a *generative* instrument.

## Core idea

Laid side by side, the full six-layer breakdown makes films that "feel similar" reveal
their real differences (and vice versa). The taxonomy is a **complete descriptor
vector** — Type · Supergenre · Macro/Micro · Voice · Pathway · POV — and comparing
vectors surfaces the exact decisions that distinguish two stories.

## Four comparisons (the pattern)

| Pair | Shared | The decisive divergence |
|------|--------|-------------------------|
| **A. *12 Years a Slave* vs. *Argo*** | both historical docudramas, traditional voice, adult audience | Super **Day-in-the-Life** (→ Primary-Limited POV, Fish-out-of-Water) vs. **Thriller** (→ Filmmaker-Omniscient, Unlikely-Ensemble) |
| **B. *Shrek* vs. *Butch Cassidy & Sundance Kid*** | both **Buddy-Movie** pathway, **Filmmaker-Omniscient** POV, bromance | Type/Super Comedy-Fantasy vs. Drama-Western+Crime |
| **C. *The Imitation Game* vs. *Casablanca*** | both WWII-set, **nonlinear** voice | neither is a *War* film: Crime (biography/workplace/military) vs. Action (love/workplace/identity) |
| **D. *The Godfather* vs. *Godfather II*** | one novel, one writing team; both Crime, historical gangster antihero | **Lost Innocence** + traditional voice vs. **Coming of Age** + nonlinear voice |

The lesson of each: **the layers that differ are the whole story.** *12 Years a Slave*
isn't "less thrilling than *Argo*" — Ridley chose a super whose POV and pathway make
*realism*, not suspense, the payoff. Coppola/Puzo couldn't tell an origin story twice,
so they flipped one pathway (Lost Innocence → Coming of Age) and one voice axis
(linear → nonlinear) and got a second classic from the same source.

## The taxonomy as a *generative* tool

Reimagining *Romeo & Juliet* three ways from **one story** by rolling the layers:

- **"Stabbed in the Heart"** — Drama/Crime, Mystery-Whodunit + Legal-Courtroom,
  nonlinear + fourth-wall Voice, Noir pathway, Primary-Omniscient POV.
- **"RoBot SiX + Joules-01"** — Comedy/Sci-Fi, AI-Robots + Womance, animated musical
  for kids, Human-vs-Technology pathway, Filmmaker-Omniscient POV.
- **"Blood Trail"** — Tragedy/Western, Survival + Protection, traditional voice (leads
  never share a language), Chase/Hunt pathway, Filmmaker-Omniscient POV.

Same characters and plot skeleton; six knobs turned; three unique films.

## Studio application

- **This chapter is the spec for the `Screenwriter` `Contribution` as a *vector*.** The
  comparison tables *are* the data structure: a fixed set of fields (Type, Supergenre,
  \[Macro→Micro\], Voice-axes, Pathway, POV) filled per production. Two productions can
  then be diffed field-by-field — the plan-phase analogue of how
  [`tests/test_engine.py`](../../../tests/test_engine.py) asserts a complete `Shot`.
- **Generative mode = the studio's actual use.** The *Romeo & Juliet* reimaginings show
  the taxonomy is best used to **roll one seed into varied outputs** — exactly the
  "instance-per-production, engine stays singular" model
  ([storyline 0005](../../../context/storyline/0005-productions-as-instances-and-output-storage.md)):
  one Production seed, many configured renders. A `Screenwriter` heuristic can hold the
  logline fixed and vary Supergenre/Voice/Pathway/POV to generate structured
  alternatives for the Producer (HITL) to greenlight.
- **The full vector is what flows to the `Director`.** All six layers together form the
  plan-phase `Brief` the `Director` reconciles into shoot/assemble decisions
  ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)) — Type/Super
  set atmosphere & theme (Production Design, DP), Voice routes medium & dialogue (render
  backends, [`SpeechRenderer`](../../../sequitur/speech.py)), Pathway shapes the
  [`Sequence`](../../../sequitur/edit.py), POV constrains coverage (camera). This
  chapter is the proof that the taxonomy's layers are **not independent tags but a
  connected control surface** for the entire studio.

Full taxonomy: [Road Map](ch01-the-need-for-a-road-map.md) ·
[Type & Supergenre](ch02-movie-types-and-supergenres.md) ·
[Macro & Micro](ch03-macrogenres-and-microgenres.md) ·
[Genre Case Studies](ch04-genre-case-studies.md) · [Voice](ch05-voice.md) ·
[Pathway](ch06-pathway.md) · [Point of View](ch07-point-of-view.md).
