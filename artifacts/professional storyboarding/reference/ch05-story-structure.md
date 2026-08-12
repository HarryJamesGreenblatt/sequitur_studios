# Chapter 5 — Story Structure

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 5.
> **Scope:** what a story *is*, the three-act structure, the nested hierarchy from gesture up to story, the elements that drive it (protagonist, conflict, inciting incident, climax), and how the board artist controls rhythm, setup/payoff, and choice.

## Core idea

A story is **a progression from point A to point B** — and the only thing that makes it a story is *change* along the way (even A→A counts if the journey changes something; absence of change means nothing to document). Narrowed to cinema: a story is **the emotional journey of a character pursuing a goal from A to B**. A protagonist fixes on an object of desire; opposing forces create conflict; the middle is the visible record of the attempt; the end is arrival at B — which is *not* necessarily success, just the exhaustion of time or choices.

For the board artist this matters because structure and visual design are one job. You rarely get to rewrite the script, but you fully control *how each beat is shown* — so you are the first editorial pass, shaping rhythm, tension and emphasis with images. Thinking about structure *while boarding* lets the visual design progress in step with the story: calm camera before a reversal, angular shapes around the villain at the climax, cutaways that stretch tension instead of dumping it.

## The structural hierarchy

Everything nests. Small units compose upward into the whole:

> **gestures → actions → beats → shots → scenes → sequences → acts → story**

| Unit | What it is |
|------|-----------|
| **Story** | The whole, A→B, with change |
| **Acts** | Three markers — I set-up (character + problem), II confrontation (dealing with it), III resolution |
| **Sequences** | Closely related scenes forming a unified whole to land one act point |
| **Scenes** | Beats unified by character/location/time/theme; each needs an objective and must **turn** |
| **Shots** | The camera set-ups — *unique to film*; each is a bundle of camera decisions |
| **Beats** | Smallest unit of action — a single thought (one sentence describing the action to a blind friend) |
| **Actions** | A character act with a start and end, relaying one piece of information |
| **Gestures** | *How* an action is taken — this is acting; where character is revealed (animation boards go down to here) |

Every scene must cause change — a **turning point** — via one of four levers: **surprise** (reversal), **increased curiosity** (what next?), **insight** (fills an earlier set-up), or **new direction** (redirects the film). A **beat board** captures only the major beats that drive the story, not continuous action.

Each shot answers concrete questions — *which subjects? camera height? camera direction? wide or long lens? how cropped? what part of the action, starting/stopping when?* — which get easy once you first answer: **what does my character want and why should we care?** and **what does the audience need to see right now?**

## Story elements

- **Protagonist** — the subject of the story (person, object, or abstract ideal).
- **Motivation** — the inner driving force; the protagonist conceives an *object of desire*.
- **Conflict** — the opposing forces, at three levels: **inner** (self), **personal** (friends/family), **outer/extra-personal** (society, institutions, nature).
- **Antagonist** — the personified major opposing force (villain, nemesis, even the weather).
- **Inciting incident** — the event that upsets the protagonist's balance and launches active pursuit; happens *to* or is *caused by* the protagonist; sits early, in Act I.
- **Plot** — the action, usually external conflict; a story can carry many subplots.
- **Climax** — the point of maximum emotional intensity; *without it there is no story*. Usually near the start of Act III.
- **Resolution** — the winding-down; a beat for the audience to gather their thoughts.

## The story chart — the emotional curve

Track three braided strands, each with its own A→B change: **plot** (external action), **character** (human nature, internal conflict), **theme** (the larger idea; the world changing around the character). Plotted, the three acts rise in growing arcs to an apex at the Act III climax, then dip slightly into resolution — the curve *is* the audience's emotional journey. Each act also has its own mini-climax / turning point (an apex then a dip before the next act rises). The inciting incident sits near the front, in Act I. Blocking structure this way keeps a complex story legible.

## Rhythm, choice, and payoff — the board artist's levers

- **Rhythm** — how fast or slowly a scene develops. Scripts are vague here; the artist interprets pacing for the emotional beat. Being the first editorial pass, you can *withhold* — inject cutaways and reaction shots to build tension toward a climax rather than revealing everything at once.
- **Choice reveals character** — true character shows in choices made *under pressure*; the harder the dilemma, the deeper the character. Trivial choices carry no weight (coffee vs. tea is not it); true choice is dilemma (Michael Corleone choosing to kill his brother; the Iron Giant's self-sacrifice).
- **Expectation should not meet result** — set up, then pay off *originally*. A story whose ending the audience correctly predicts has no tension and no reason to keep watching. Build intensity toward the climax; give the audience what they want, but not the way they expect.

## Studio application

- **This grounds the plan-phase structure the edit layer later realises.** The board sequence *is* the structure made visual: acts→sequences→scenes→shots is exactly the nesting the studio plans before shooting, and a board sequence is what the editorial [`Sequence`](../../../sequitur/crew/editorial.py) then assembles into a cut. Structure decided here is the contract the cut honours.
- **The gesture→…→story hierarchy is the studio's unit ladder; the [`Shot`](../../../sequitur/shot.py) is the pivot rung.** Below the shot lives acting/gesture (the imagined-character intent a board commits); at and above it lives the camera grammar of [camera.py](../../../sequitur/crew/camera.py) / [grip.py](../../../sequitur/crew/grip.py). The per-shot questions ("what does the audience need to see *right now?*") are precisely what a role's `heuristic` resolves in [role.py](../../../sequitur/crew/role.py) — structure decides *why* a shot exists, grammar decides *how* it looks.
- **Overlaps the plan-phase sources — treat this as the visual restatement of them.** Cross-reference [The Screenwriter's Taxonomy Ch. 6 — Pathway](../../the%20screenwriter's%20taxonomy/reference/ch06-pathway.md) (the character's route A→B and its turning points) and [Directing Ch. 5 — Plot, Time, and Structure](../../directing/reference/ch05-plot-time-and-structure.md) (three-act mechanics). This chapter is the same skeleton seen from the drawing board, where structure first becomes pictures.
- **Rhythm and setup/payoff are the [Director](../../../sequitur/crew/director.py)'s pacing contract, applied before the cut.** Withholding for tension, escalating toward the climax, and "expectation ≠ result" are decisions the board makes as the first editorial pass — the same intent the [Editor](../../../sequitur/crew/editorial.py) inherits when timing the [`Sequence`](../../../sequitur/edit.py).
