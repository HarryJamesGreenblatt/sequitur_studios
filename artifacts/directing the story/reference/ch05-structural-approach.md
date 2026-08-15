# Chapter 5 — Structural Approach: Tactics to Reach the Goal

> Abridged from Francis Glebas, *Directing the Story: Professional Storytelling and Storyboarding Techniques for Live Action and Animation* (Routledge/Focal Press), Ch. 5.
> **Scope:** the two-plane model of a film — the *events* the audience watches above the **threshold of awareness** and the invisible *structure* (narrative questions, delays, answers) working below it — and the director's remit to keep that structure invisible so the viewer stays "lost" in the story.

## Core idea

A story is not made dramatic by its content but by **how its parts fit together**. Glebas' "Once upon a time…" *Mad Libs* shows that almost any place, hero, or obstacle can fill the blanks — what makes the result *structurally dramatic* is the fixed shape underneath: a **conflict** is presented, builds to an **inevitable confrontation and climax**, and then **resolves**. Every piece is load-bearing; drop one and the audience feels that something is missing. The structural approach begins from what the audience is *doing* while they watch, and aims to give them an emotionally satisfying experience by **working at the structure, not the surface**. These are the *tactics to reach the goal*: the tools a director deploys — invisibly — to keep the viewer emotionally engaged all the way to the end.

## The two planes: events and structure

Glebas' organizing chart splits a film into two planes divided by a **threshold of awareness**:

| Plane | What it is | The audience… |
|---|---|---|
| **Events** (above the line) | what is going to happen next in the story | consciously watches and follows |
| **Threshold of awareness** | the dividing line between what we notice and what we don't | crosses it only when something is *out of place* |
| **Structure** (below the line) | *how* the story is told — narrative questions, delays, answers, the "speaking metaphor" (one idea at a time) | processes unconsciously, never noticing |

The mind runs both planes at once, far faster than conscious thought. Consciousness is "the tip of a great iceberg"; most of the perceptual work of following a story happens below it. A director works the lower plane so the upper plane feels effortless.

## Keeping the structure invisible

Glebas' puppet-show parable — a clothesline as the literal threshold — makes the rule concrete: the audience enjoys the characters' antics until one puppet **notices something out of place** and points at it. The curtain drops, the Wizard-of-Oz illusion shatters, and the viewer is bumped up to the structural level and out of the story.

- We become aware of the structure almost always because the **filmmaker did something wrong** — a small fault (a continuity error) or a big one (the story is boring). Either way the audience stops feeling good.
- So the tactic is **invisibility**: never call attention to the cutting, staging, composition, or the storyteller's choices. Keep the seams hidden and the viewer stays "lost."
- A deliberate *out-of-place* element is the exception that proves the rule — Scheherazade's charcoal-smudged face briefly interrupts the inner tale, but it *serves* the outer story by revealing that her guard is down and the sultan is warming to her. An anomaly is only permitted when it does **structural work**.

## Tactics at the structural level

The recap Glebas carries into this chapter is itself the toolkit — the tactics deployed below the threshold:

- **Aim at the heart.** Work the structure to reach emotion, not the surface to impress.
- **Speaking metaphor — one idea at a time.** The conscious mind attends to a single thing; present one clear idea per beat.
- **Punctuate.** Give the audience pauses to process; don't run information together.
- **Pose narrative questions, then delay the answers.** Intrigue holds attention; teasing the answer is what keeps them guessing.
- **Build a hierarchy of questions.** Nest small questions inside larger ones so complexity accumulates and the audience never runs out of things to wonder about.

The end-state is mastery-then-forgetting: learn the tactics deliberately, run them intuitively, and reach back for them only when analyzing a story to fix what feels flat or unclear.

## Studio application

- **This is the dramatic spine the plan-phase *treatment* must carry.** Ch. 5's structure — conflict → confrontation → climax → resolution, sequenced as a chain of tactics aimed at an emotional goal — is exactly what the Screenwriter's human-readable treatment output needs to state before any shot is composed. The machine-readable [`Screenwriter` descriptor](../../../sequitur/crew/screenwriting.py) *classifies* the story; the treatment *tells its spine*, and this chapter grounds that telling.
- **The two-plane model maps onto the studio's decision/render split.** "Events above the threshold" is the story the [`Director`](../../../sequitur/crew/director.py) reconciles into a [`Shot`](../../../sequitur/shot.py); "structure below the threshold" is the grammar those seats wield ([camera](../../../sequitur/crew/camera.py), the [edit layer](../../../sequitur/edit.py)) that must stay *invisible*. "Keep the structure invisible" is the standing rationale for the continuity-driven cutting the [Editor](../../../sequitur/crew/editorial.py) enforces.
- **"Narrative question → delay → answer" is a withholding schedule the edit executes.** The tactic of teasing an answer is the plan-phase intent the [`Sequence`](../../../sequitur/edit.py) later realises through reveal timing — the same discipline the cut-decision seat in [`judgment.py`](../../../sequitur/crew/judgment.py) applies at the micro level.
- **"Aim at the heart" seeds the `Brief` the Director reconciles.** The emotional goal is the top-level intent a [`Brief`](../../../sequitur/crew/director.py) carries into the crew; every department's proposal is a tactic toward it, and the Director's job is to keep those tactics coherent and invisible ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)).

> **Overlap flag:** the "story spine / tactics to reach the goal" here is the **visual/tactical** telling of structure. The Screenwriter's Taxonomy gives its **classification** ([Ch. 6 — Pathway](../../the%20screenwriter%27s%20taxonomy/reference/ch06-pathway.md), the closed structural-arc enum) and Rabiger gives the **dramaturgy** ([Directing Ch. 5 — Plot, Time, and Structure](../../directing/reference/ch05-plot-time-and-structure.md)). Reconcile all three when the `Screenwriter` structural vocabulary is built: Glebas names the *tactics*, Williams names the *arc*, Rabiger names the *craft*.

Next: [Ch. 6 — What Do Directors Direct?](ch06-what-do-directors-direct.md) — the director's actual remit, which turns out to be a single thing: the audience's attention.
