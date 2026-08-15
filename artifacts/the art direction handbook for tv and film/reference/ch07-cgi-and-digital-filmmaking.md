# Chapter 7 — CGI and Digital Filmmaking

> Abridged from Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed., Routledge/Focal Press), Ch. 7.
> **Scope:** digital art direction — the shift of design intent from *physical* to *digital*, and the pipeline that produces a photo-real view of a set **before anything physical exists**. This is the direct bridge to a generative image backend: matte painting → digital set extension → fully synthetic scene, all conceived in the art department.

## The through-line: paint over a plate

Rizzo opens on **rotoscoping** — Max Fleischer's 1917 technique of drawing onto live-action footage on frosted glass — and jumps to its digital heir: *A Scanner Darkly* / *Waking Life*, where illustrators traced stylized line and color over QuickTime video on Wacom tablets, with **interpolation** / **tweening** filling the in-between frames. The lineage is the point: **draw over a captured plate** is the oldest digital-adjacent move, and it is exactly the *image-to-image* gesture a generative model makes. **TRON** (1982) then marks the first CGI vehicles — compositing 12–15 **wedges** (layers) per frame over a black-flocked set — a film the Academy disqualified for "cheating by using computers."

## The physical → digital design-intent ladder

The chapter's core transfer for a generative backend is that the *design intent* survives as the technique moves from physical to digital. Rizzo (via Alex McDowell) narrates the ladder:

| Technique | Era | What transfers to prompting |
|---|---|---|
| **Glass matte / in-camera miniature** | traditional | a painted extension of the frame — the seed of "set extension" |
| **Rear projection** | mid-century | a plate behind the actors — background as a separate layer |
| **2D matte painting / composite** | optical era | a painted world joined to live action |
| **2½D / 3D miniature tracked to camera** | digital transition | background elements that follow the move |
| **CGI set / fully synthetic scene** | digital | the whole environment authored, not shot |

Crucially these techniques don't *disappear* — they become "fundamental elements tracked into camera moves." The most effective work **mixes methodologies** (sophisticated VFX + in-camera sleight-of-hand); the in-camera solution is "almost always the most economical." For a prompt, this ladder is a spectrum: a shot can be a *painted extension of a real plate* or a *fully synthetic scene*, and the seat chooses where on it a shot sits.

## The digital art department (Alex McDowell)

McDowell's account is the chapter's payload — it describes, in physical-production terms, precisely what a generative image backend does:

- **Photo-real concept views produced before anything physical exists.** Concept artists render "a specific camera lens and position … complete with atmosphere, lighting, color, and set dressing" — the director sees the set's look "in enough time to affect the content of the film." One such view *is* a `build_prompt` render.
- **Matte paintings and set extensions conceptualized in-house**, plus the 3D elements and animations (the *Minority Report* Hovership, Maglev, Spyders) — the art department, not a downstream VFX house, drives the look.
- **The designer at the center of the information flow.** A networked team + a **server/archive** with strict **file-naming** puts the Production Designer "back at the center of the flow of information that will determine and control the look of a film."
- **50/50 analog + digital.** The pencil "will probably always be more relevant for the design of period and decay"; digital wins for the futuristic. Both feed the same concept.

## Pre-visualization (Colin Green, Doug Chiang)

**Pre-vis** builds "a digital version of everything you see in the movie" to answer physical questions cheaply: on *Panic Room* the impossible crane move was solved by building the shot in the computer and feeding the data to a motion-control camera. The goal *shifted over time* — from "save money / be efficient" to "give the director a tool to direct a better film." Doug Chiang's *Polar Express* merged 2D and 3D into one streamlined process (**2½D**), integrating set design with lighting "before Zemeckis finished writing." Three visualization phases recur:

| Phase | What it is |
|---|---|
| **d-vis** (design visualization) | sets/environments created in the design phase |
| **pre-vis** | what the camera sees; real + CG combined, before the shoot |
| **post-vis** | integrating final elements after the shoot |

## Merged / cross-media

Victor Martinez reframes "mixed media" as **cross-media**: an active exchange between hand and computer that "transcends any original gesture by either." McDowell is blunter — there is **no such thing as a traditional art director**; the seat's job is to "coordinate all aspects of the design process with full peripheral vision," knowing what 2D/3D tools *can do* without needing every package. Film "is an art that is constantly reinventing itself." This is the standing rationale for a seat that speaks both physical and generative languages.

## Studio application

- **[`ImageStudio`](../../../sequitur/image.py) IS the digital art department's concept-view generator.** McDowell's "photo-real view at a specific lens and position, with atmosphere, lighting, color, and set dressing, before anything physical exists" is one [`build_prompt`](../../../sequitur/prompt.py) → [`ImageStudio.render`](../../../sequitur/image.py) call. This chapter is the clearest ground for the planned **Production Designer** seat over the image backend.
- **The physical→digital ladder is the prompt's own spectrum.** Matte painting → set extension → fully synthetic is the range a single prompt spans; the seat decides whether a [`Shot`](../../../sequitur/shot.py) is a painted extension of a plate or a wholly authored scene — the "mix methodologies" discipline in generative terms.
- **"Atmosphere, lighting, color" is the Colorist's language, landed at plan time.** The look McDowell's concept artists lay over a lens view is exactly the [`Look`/`Cast`/`TonalRange` vocabulary](../../../sequitur/crew/colorist.py) — the plan-phase `Look` intent flows from the Production Designer prompt into the Colorist's [`grade.py`](../../../sequitur/grade.py) execution downstream ([storyline 0020](../../../context/storyline/0020-grounding-color-the-colorists-handbook.md)).
- **Rotoscope / paint-over → reference-conditioned generation.** "Draw over a captured plate" (Fleischer → *A Scanner Darkly*) is the lineage of an image-to-image mode for [image.py](../../../sequitur/image.py) — a future backend seam where a plate or reference conditions the render.
- **"No traditional art director" grounds the seat's remit.** The Production Designer over [image.py](../../../sequitur/image.py) must coordinate both physical description and generative tokens, reconciling with the [`Director`'s `Brief`](../../../sequitur/crew/director.py) — a planned seat, not yet in code, whose mandate this chapter defines.

Next: [Ch. 8 — Navigating Paperwork and Daily Shooting-Process Tasks](ch08-paperwork-and-daily-shooting-tasks.md) — art-department logistics and shooting-day tasks.
