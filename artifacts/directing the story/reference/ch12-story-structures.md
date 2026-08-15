# Chapter 12 — The BIG Picture: Story Structures

> Abridged from Francis Glebas, *Directing the Story: Professional Storytelling and Storyboarding Techniques for Live Action and Animation* (Routledge/Focal Press), Ch. 12.
> **Scope:** the macro shapes that give a film its skeleton — Propp's function-maps, Aristotle's plot curve, and the Hero's Journey — reconciled against **narration**, plus the working apparatus of act structure (ending-first design, turning points, scene types, exposition, plant-and-payoff, stakes).

## Core idea

**Structure is the relationship among a story's parts** — and, like a skeleton, the support that lets the whole stand and move. Because audiences already *know* the common structures, they can predict what is coming (we know the returning astronauts won't crash), so the director's task is to honour the shape while defeating the prediction: invent trouble, then answer it from *within the story's own material* (the goofball chimp who kept missing the target truck finally lands the spacecraft *on* one). Glebas frames three interlocking levels of structural analysis — **macro** (the Hero's Journey / Aristotle's curve — the shape of the events), **mid** (Propp's function-maps — where the story goes next), and **micro** (narration — how each moment is told through narrative questions). Only the last supplies the *motor* that pulls a viewer through; the macro shapes give form but do not, by themselves, keep anyone watching.

## Primitive structures and Propp's maps

The earliest filmic structures are the two irreducible engines:

- **The peep show** — the unveiling of something hidden, surprising, or desirable.
- **The chase** — active conflict racing against time in pursuit of someone or something.

Other simple structures are metaphors of familiar activities (jack-in-the-box, hunting, tug-of-war, roller coaster, rolling snowball). Vladimir **Propp** analysed thousands of folktales and found a fixed set of character types and **functions** (action verbs). Each function can be **mapped** to a beginning / middle / end, and the map both reveals variations you hadn't considered and **nests inside other maps** (a theft leads to a chase, so the chase-map becomes a sub-part of the theft-map). **Context supplies qualifiers**: the same image of a hand about to take something means different things depending on what we saw earlier — is he stealing, or taking back what was stolen from him? Maps are idea-generators, not formulas.

## Three ways to read the macro shape

Glebas compares three analytic frames and where each is strong:

| Frame | What it charts | Strength | Weakness |
|---|---|---|---|
| **Aristotle's plot curve** | dramatic intensity (how "lost" we are) over time — rising beginning (~30 min) · middle climb to a crisis (~60 min) · climactic peak + descent (~30 min) | maps intensity and pace against the running time | descriptive shape only; no moment-to-moment motor |
| **Hero's Journey** (Campbell / Vogler) | the mythic stages of a journey of self-discovery | rich *inspiration*; addresses life-passages and change | the supreme ordeal lands mid-Act-II, so it **doesn't map cleanly** onto the dramatic curve; formulaic if followed literally |
| **Narration** | the flow of information — narrative questions, delays, answers | the actual **motor**; explains why you get "lost" even joining mid-scene | says nothing about overall shape |

The takeaway: the Hero's Journey is best used as **suggestive inspiration, not a plot formula**, and narration is the level that must *always* be running.

## The Hero's Journey (a.k.a. the Neurotic's Road Trip)

The Journey is human change put into visible, dramatized action. Its value is the emotional truth underneath — a journey of **facing fear**, the psychological process of growing up that we all relate to, staged in far-off places only because that is less boring to watch. Glebas' compressed stages:

> ordinary world → call to adventure → **refusal** (resistance) → accept the call → leave home → meet the **mentor** → cross the **threshold guardian** → enter the special world → **tests** → **supreme ordeal** (facing the worst fear; death-and-survival) → **reward** → the road back (rededicate — the villain isn't fully dead) → **resurrection** (reborn, changed) → return with the **elixir**.

The archetypal characters are defined by **function**, not costume: the **mentor** (one who has already taken the journey), the **trickster** (a shape-shifting catalyst), the **allies**, and the **shadow** (the dark force — often a disowned part of the self, *projected* outward). That projection is the engine of drama itself: internal conflicts externalised as conflicts between characters who serve the functions.

**What goes wrong with it:** one shared map makes stories look alike (the Disney formula — the "I want…" song, the merchandisable sidekick, the villain who must engineer his own demise). Repetition is predictable, and predictable is boring; *Shrek* and *Hoodwinked* stayed fresh by parodying the formula.

## The working apparatus

Structure in practice, not theory:

- **Design from the ending backwards.** Start at the end so you know where you are going. The **ending is what the story proves**; the **beginning is that ending asked as a question**; the **middle is the obstacle** between them.
- **Turning points** are moments where the hero must change direction on meeting a consequence or obstacle; they mark the transition into each act and are prime spots to surprise the audience.
- **Scene types carry specific loads:** the **title** sets expectations; the **prologue / exposition** frames the world; the **backstory** is layered in bits (enough to matter, never so much it stalls the motion); the **opening** starts on a turning point, ideally with a bang.
- **Exposition sets the rules** — push plausibility but never break believability, and once the rules are set, keep them or you are not playing fair. **Dramatize** exposition through action; a character who stops to *explain* pushes the structure above the threshold of awareness.
- **Plant and payoff** — seed items and information early so later events feel inevitable rather than arbitrary; payoffs are the rewards and punishments of what was planted.
- **Stakes** — show what is at risk, make it big emotionally, and establish it **early**.

## Studio application

- **The macro / mid / micro split is the studio's own layering.** Glebas' three levels map straight onto the seams: **macro** structure is the [`Screenwriter` descriptor's](../../../sequitur/crew/screenwriting.py) `Pathway` and the treatment's arc; **mid** (Propp's maps — a theft nesting a chase) is the sequence shape the [`Sequence`](../../../sequitur/edit.py) assembles; **micro** narration ("question → delay → answer") is the [Editor](../../../sequitur/crew/editorial.py)'s reveal timing. Structure decided in the plan phase is the contract the cut honours.
- **Story structures resolve to the `Pathway` vocabulary.** The Hero's Journey — and its divergences — is exactly what the Taxonomy encodes as a closed enum; this chapter is the *narrative* telling of that classification. A [`Screenwriter`](../../../sequitur/crew/screenwriting.py) seat owns `Pathway`, and the treatment grounded here supplies the human-readable spine the descriptor abbreviates.
- **"Design from the ending backwards" and "turning points" are `Brief`-shaping directives.** The ending-as-thesis and the act-transition turning points are the top-level intent a [`Brief`](../../../sequitur/crew/director.py) carries into the crew; they set the shape the [`Director`](../../../sequitur/crew/director.py) reconciles toward, phase by phase, so that a revise re-runs one phase against a known destination ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)).
- **Plant-and-payoff and stakes are continuity constraints the edit inherits.** A planted item must survive from the [`Shot`](../../../sequitur/shot.py) that seeds it to the one that pays it off — the same across-a-sequence consistency the [Editor](../../../sequitur/crew/editorial.py) polices when it times and validates the [`Sequence`](../../../sequitur/edit.py).

> **Overlap flag:** this is Glebas' **visual / tactical** telling of macro structure. Reconcile it with the Taxonomy's **classification** ([Ch. 6 — Pathway](../../the%20screenwriter%27s%20taxonomy/reference/ch06-pathway.md), the closed arc enum), Rabiger's **dramaturgy** ([Directing Ch. 5 — Plot, Time, and Structure](../../directing/reference/ch05-plot-time-and-structure.md), the three-act mechanics and time-handling), and the board artist's **visual restatement** ([Professional Storyboarding Ch. 5 — Story Structure](../../professional%20storyboarding/reference/ch05-story-structure.md)). When the `Screenwriter` structural vocabulary is encoded, these four are the same skeleton seen four ways — Glebas the tactics, Williams the enum, Rabiger the craft, Paez & Jew the drawing board.

Structure decided, the plan phase can hand the crew a spine to render — the Taxonomy turns this shape into the closed [`Pathway`](../../the%20screenwriter%27s%20taxonomy/reference/ch06-pathway.md) enum the studio's `Screenwriter` owns.
