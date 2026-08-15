# Chapter 4 — The Design Process

> Abridged from Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed., Routledge/Focal Press), Ch. 4.
> **Scope:** the core production-design pipeline — how a **screenplay** becomes a **visual concept** (a single central image), then research, thumbnails, concept art, models, and drafting turn that concept into a buildable (or renderable) design. This is the spine of the studio's planned **Production Designer** seat: the plan-phase intent that feeds the image backend.

## The visual concept: landing a central image

Filmmakers tell stories; the **visualization** process is the translation of the written word into the rectangle of a screen. Its product is a **visual concept** — *the* central idea of a movie stated in **iconic** terms: a metaphor, trope, or core image that "optically binds all sections of the movie." It is the reason the art department exists, and it "informs and shapes every choice" downstream.

Rizzo's canonical examples: the **ovoid / egg** as the pre-cog chamber in *Minority Report* (why an egg, not a pyramid, for that idea); Ken Adam's **War Room** for *Dr. Strangelove*; the framing of *Barry Lyndon*. The concept is a *single* deliberate metaphor, not a mood board.

Four paths Rizzo lists for finding it:

- Finding the **visual arcs** within the story.
- Identifying **thematic elements**.
- Recognizing **emotional tones**.
- Weighing **underscoring vs. contrasting** (does the design echo the scene or push against it?).

Beneath this sits a composition claim: the **golden rectangle** (5:8 ratio) and an **optimal fractal density** (~1.3 on a 1–2 scale) are what the eye reads fastest — the "Goldilocks" amount of information, neither chaotic nor starved. Aspect ratio and frame density are therefore design decisions, not just camera settings.

## The pipeline stages

The chapter walks a single spine from script to buildable design. Each stage is a *different representation of the same visual concept*:

| Stage | What it produces | Why it matters |
|---|---|---|
| **Visualization** | the mental image + first marks | the inner/outer "two mirrors" of the imagination and the hand |
| **Visual concept** | one central metaphor/image | the aesthetic glue for the whole film |
| **Research** | a wall/library of reference imagery | grounds the concept in a real era/world |
| **Thumbnails / storyboards** | 2D continuity of shots in aspect ratio | the shooting sequence, drawn |
| **Animatics** | timed, moving pre-vis of boards | links sound + image; optimizes shooting time |
| **Concept illustration** | key painted views of set/scene | can define an entire film's look from one frame |
| **Computer / white models** | 3D volume of a set | test structure before it is built |
| **Hand / digital drafting** | scaled construction drawings | the actual design; "the details are in the set design" |

The whole is a **budget-and-schedule** process too: the **set list** (headings = sets, sub-headings = props/graphics/VFX) drives **DBD** ("draw, build, dress") time and the **Fast Track** flow chart. That management layer is real production-design craft but only lightly transfers to a generative backend — captured here as context, not detail.

## Research: living inside the reference

Research is "a powerful way to define the visual concept." The art department becomes the production's image repository — walls "plastered" with **icons, indexes, symbols, and metaphors** of the concept, so the designers "live within them while we design." The exemplar is *Forrest Gump*: Rick Carter's concept was "real and human," and the research had to be true not just to history but to *how people remembered it* — period newsreels, magazines, a character's life told as a wall-length collage timeline. Reference is not decoration; it is the concept made concrete and searchable.

## Who is designing: the representations

- **Storyboarding** — 2D, bound by the screen's **aspect ratio**, filling boxes with shot continuity; the root of animatics. Explores idea possibilities "in a way CGI cannot."
- **Animatics** — each board cell expanded to its own timed page with plan/elevation/camera/equipment info; timing = budget.
- **Concept illustrating** — a single strong image "can define the look of an entire film" (James Clyne's *TRON: Legacy* sketch; a world "that exists first on a piece of paper").
- **Computer modeling** — explore a set's structure before it's built (*The Terminal*); designer moves closer to the center of information flow.
- **White models** — a fast physical 3D sketch (foamcore) when a napkin beats a render; reveals volume and the need for **wild walls**.
- **Hand / digital drafting** — set designers (draftspersons) "are responsible for the actual design"; quarter-scale and full-scale detail. Tools: **Rhino**, **Photoshop**, **SketchUp** (the "great democratizer"; **d-vis** / **pre-vis** / **post-vis**, with Advanced Camera Tools exposing focal length, aspect ratio, and lens position).

Digital assets ride on disciplined **nomenclature** — "IMG_1243.jpg is not a file name." Searchable **metadata/tags** (category, set ID, set name, date, initials) make the archive *immediate*; this is the same file-naming discipline every generative pipeline needs for its outputs.

## Studio application

- **The visual concept is the plan-phase intent the whole image backend serves.** A single central metaphor — the *idea* of a set — is exactly what the planned **Production Designer** seat must land *before* [`build_prompt`](../../../sequitur/prompt.py) renders any [`Shot`](../../../sequitur/shot.py) for [`ImageStudio`](../../../sequitur/image.py). The seat's job is to hold one coherent concept across every prompt, the way the concept "optically binds" a film.
- **This grounds the seat above the [`Director`](../../../sequitur/crew/director.py)'s [`Brief`](../../../sequitur/crew/role.py).** The `Brief` carries *scene* and *mood*; the visual concept is the art-department *overlay* on top of that — the central image the machine-readable [`Screenwriter` descriptor](../../../sequitur/crew/screenwriting.py) *classifies* but cannot *narrate*, mirroring how a treatment tells a story the taxonomy only tags ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)).
- **Research = reference conditioning.** The "wall of images" the department lives inside is the studio's reference-set for the backend: the concept made into a searchable bank of icons/indexes/symbols that a future image-to-image or reference-guided mode of [image.py](../../../sequitur/image.py) draws on.
- **pre-vis / d-vis IS what `ImageStudio` is.** Rizzo's design-visualization ("sets and environments created before they're built") and concept illustration ("a world that exists first on a piece of paper") describe the studio's render loop exactly — one [`build_prompt`](../../../sequitur/prompt.py) call is a concept illustration. The golden-rectangle / aspect-ratio / fractal-density concerns become literal composition tokens in that prompt.
- **Nomenclature discipline transfers directly.** Rizzo's searchable file-naming maps onto the studio's output store — named, tagged, immediate — the archive hygiene a generative seat depends on.

Next: [Ch. 5 — The Physical Design](ch05-the-physical-design.md) — how the visual concept becomes buildable scenery, space, and construction.
