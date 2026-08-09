# Chapter 5 — Voice

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy*, Ch. 5.
> **Scope:** the fourth layer — **Voice**, *how* the story is told. Not genre (you
> can tell any genre in any voice); the storyteller's chosen "vehicle."

## Core idea

Once genre is set, Voice decides how the audience will **experience** it. The same
gangster Crime story is *Black Mass* (traditional), *Bugsy Malone* (kids'), *Mafia!*
(parody), *Guys and Dolls* (musical), or animated — same genre, different voice.

A **traditional voice** is: a *linear* narrative, *modern* filmmaking technique, for
a *broad* audience, in *live-action* with *human* characters who *speak* their
dialogue as *oblivious* participants (unaware of the camera). Six questions — six axes
a writer can flip:

## The six axes of Voice

1. **Linearity.** Linear, or one of ~6 nonlinear devices: **Flashback**,
   **two time periods intercut** (*Godfather II*), **parallel realities**
   (*French Lieutenant's Woman*), **repetition/loop** (*Run Lola Run*, *Groundhog
   Day*), **time travel** order-scrambling, **reverse chronology** (*Memento*).
2. **Filmmaking style.** The "modern" default (color, prime lenses, dolly/crane,
   CGI, complex sound design, a cut every 5–30 s). Every element is subvertible:
   black-and-white-with-color inserts (*She's Gotta Have It*, *Schindler's List*),
   minimalist/creative silence (*A Man Escaped*, *No Country*), long takes / slow
   rhythm (*Stranger Than Paradise*), few camera moves (*The New World*).
3. **Audience breadth.** Place your content on five continua —
   **Language · Violence · Humor · Sexuality · Gore** — to aim at kids vs. adults.
   Same subject, different voice: *Animal House* ↔ *Monsters University*;
   *The Untouchables* ↔ *Bugsy Malone*. Adult themes *can* live in G-rated films
   (*The Lorax*, *Watership Down*) — just adjust the voice. Also: general vs.
   **specific** audience (build on assumed knowledge, but get the details right).
4. **Medium / performer.** Live-action human, or a deliberate choice of
   **animation / puppets / stop-motion** — a *form*, not a genre (Kaufman): capable of
   family *and* mature work (*Anomalisa*, *Akira*, *Superstar: The Karen Carpenter
   Story*).
5. **Dialogue mode.** How interiority reaches the audience: **spoken** dialogue,
   **musical** numbers (feelings sung, not said), **silence / no-dialogue**
   (*Blancanieves*, *After the Apocalypse*), or **internal monologue / VO**
   (*Adaptation*, *Goodfellas*).
6. **Oblivious participants / the fourth wall.** Keep it intact, or **break** it —
   characters address the camera (*American Psycho*, *The Big Short*, *Deadpool*), or
   the whole film adopts a **mockumentary** frame (five platforms: Low-Budget,
   Sham-Reality, Known-Actor, Satiric-Media, Uchronia).

## Studio application

- **Voice is a *struct of axes*, not a single enum** — the key modeling insight for a
  `Screenwriter` role. Where Supergenre is one closed choice, Voice is ~6 orthogonal
  fields (`linearity`, `style`, `audience`, `medium`, `dialogue_mode`, `fourth_wall`).
  This mirrors how a [`Shot`](../../../sequitur/shot.py) is a *bundle* of independent
  grammar fields, not one label.
- **Voice is where the story layer *reaches into the render grammar*.** Its axes are
  literally the other departments' knobs: "modern filmmaking style" = the DP/Grip/Editor
  grammar already encoded in [`crew/`](../../../sequitur/crew/); "dialogue mode" routes
  to the sound layer's [`SpeechRenderer`](../../../sequitur/speech.py) (spoken vs.
  musical vs. silent vs. VO); "medium" (live-action vs. animation) selects the render
  backend itself (Gemini video vs. a stylized image path). **Voice is the seam between
  the Screenwriter's plan and the studio's existing renderers.**
- **The audience continuum is a content-rating field with real downstream force.** The
  five continua (language/violence/humor/sexuality/gore) belong in the `Brief` as a
  ceiling that constrains every later department — the plan-phase analogue of a safety
  budget. A heuristic default of "broad audience / traditional" keeps output safe unless
  a Producer brief widens it.
- **Nonlinearity is an Editor concern the Screenwriter *declares*.** Reverse chronology,
  intercut timelines, and loops are voice decisions that the post layer
  ([`edit.py`](../../../sequitur/edit.py) / `Editor`) must execute — a concrete
  plan→assemble handoff: the Screenwriter sets `linearity`, the Editor orders the
  `Sequence` to honor it.

Next: [Pathway](ch06-pathway.md) — the trajectory Voice is delivered along.
