# Chapter 5 — The Physical Design

> Abridged from Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed., Routledge/Focal Press), Ch. 5.
> **Scope:** how a screenplay becomes a **buildable scene** — the two sources of design (the art department's creations vs. the locations department's finds), the **location-vs-build** decision, the sequence of scouts that distils a **set list**, and the design intent behind interior and exterior sets. Abridged **surgically**: the *design intent that shapes a scene's look* is kept; the hammer-and-nails construction trade is dropped, because only the former transfers to a generative image backend.

## Two sources, one set list

Cinema design comes from **two sources**, and both take their direction from the screenplay:

| Source | Produces |
|---|---|
| **Art department** (design team) | scenery *created* — concept art, drafting, models, onstage builds |
| **Locations department** (scouting) | scenery *found* — real places that can be shot as-is or retrofitted |

Each source produces a "shopping list"; the two are compared and reconciled into the film's **first set list**. That set list — the enumerated inventory of every place the story must be shot — is the pivot artifact this whole chapter serves.

### Location vs. build

The recurring decision is whether to **retrofit an existing location** or **build it onstage**. It is an ongoing negotiation between the locations and design departments, but the **final call belongs to the design department**. Cost, control, schedule, and believability all weigh in: a real location is cheaper and instantly authentic but hard to control and return; a stage build is total control at a price. Some things can only be built — location shooting in and around the White House, for example, is simply *not an option*, which forced *My Fellow Americans* (1996) to construct an accurate façade from research alone.

## The scouts: distilling the set list

The set list is refined through a staged sequence of scouts (*rekkies*) across pre-production. Each pass narrows the list and transfers responsibility down the design chain.

| Scout | Who | Purpose |
|---|---|---|
| **First** | Locations Manager + Production Designer | cull dozens of options to a handful; win the Director's confidence; begin permissions |
| **Second** | Production Designer → Art Director | confirm choices, hand creative/managerial control to the Art Director |
| **Third** | Set designers | fact-finding: measure docks, elevators, doors, room dimensions for retrofitted scenery |
| **Fourth (Tech Scout)** | all department heads | the last formal scout — codifies the final onstage + locations set list and the shooting schedule |
| **Fifth** | Set designer + construction foreman | last-minute location changes; salvage and re-retrofit what already exists |

The through-line: **scouting, measuring, and photographing** the physical world is the counterpoint to the design *concept* developed in [Ch. 4](../source/CH-04.md). Together they resolve into the **master set list** and the construction budget.

## Interior vs. exterior sets — design for the camera

The chapter's craft lesson is not construction; it is that scenery is designed **for the camera and for production value, not for literal reality**.

- **Interior** (holding cell, *Murder in the First*): the cell was placed **centre-stage as a cage to scrutinise the character** — chosen "for greatest production value as opposed to the reality of where a prisoner might have been held." Walls were built *wild* (removable) so a Steadicam could swing a wall open and circle the cage in one unbroken move. The set is a **staging decision**, not a replica.
- **Exterior** (White House, *My Fellow Americans*): where the real location is off-limits, believability is *reverse-engineered from research* — reference photos, period books, a topographic survey of the site, and orientation to the sun's position for correct daylight. A "brief glimpse of believability" is enough; the set is built only to the depth the shot will see.

## Construction: idea becomes reality

Once models and drafting are approved, **blueprints commit the design to physical form**, and from that point **changes are expensive** — "wiser to wait a day for a firm decision than to rush plans into the shop and pay for the consequences." The build proceeds under **total quality management** (the Japanese *kaizen*, continuous improvement): sweat the small stuff by proxy, focus intense attention on the **hero items**. This is the phase where a plan stops being reversible.

## The digital bridge

The chapter closes on the seam to the twenty-first century. Digital set designers model in Rhino and draft in AutoCAD; on *Minority Report* (2002), Alex McDowell deliberately hired a **digital aesthetic** and even authored reference "Bibles" defining the city so any artist could answer a design question. A 3D model is **life-size at every scale** and lets an illustrator skip perspective setup and go straight to texture and mood. The physical and digital departments are not rivals — a digital modeller catches structural problems a paper draftsperson misses, and "a good digital designer must have training in handcraft." What the computer adds is **speed of change**. That same trajectory — from physical build toward a model that previews the scene in one step — is where the studio's generative backend picks up (see [Ch. 7 — CGI and Digital Filmmaking](ch07-cgi-and-digital-filmmaking.md)).

## Studio application

- **This grounds the planned Production Designer seat — but be honest about what transfers.** A generative backend has **no physical build, no location scout, no construction budget**. The entire location-vs-build economy — retrofit, wild walls, sun declination, hero magnolias trucked from Georgia — has *no analogue* in [`ImageStudio`](../../../sequitur/image.py). What survives the jump is **design intent**, not construction.
- **The set list is the plan-phase artifact that does transfer.** Rizzo's "enumerate every place the story must be shot, then reconcile into one list" is exactly the **scene inventory** the studio builds before rendering — the same enumeration the production pipeline performs in [`production.py`](../../../sequitur/production.py) and hands to [`render.py`](../../../sequitur/render.py). The set list is the pre-image of the studio's board.
- **"Location vs. build" collapses into a look-consistency decision.** Where a physical crew chose retrofit-vs-onstage, the studio chooses **reuse a reference keyframe vs. generate fresh** — the [`ImageStudio`](../../../sequitur/image.py) docstring already names its higher-leverage use as producing a *reference keyframe the video studio conditions a shot on*. Same decision, different currency: continuity of look instead of continuity of a built set.
- **"Design for the camera, not literal reality" is prompt intent, verbatim.** The holding cell staged as a *cage to scrutinise the character* is precisely the kind of expressive, production-value-first framing a [`Brief`](../../../sequitur/crew/director.py) carries and [`build_prompt`](../../../sequitur/prompt.py) composes — the studio never describes "where a prisoner would really be held," it describes the shot that reads. This is the Production Designer's contribution to the [Director's](../../../sequitur/crew/director.py) reconcile, and it overlaps the borrowed [Directing Ch. 23 — Planning the Visual Design](../../directing/reference/ch23-planning-the-visual-design.md) (Rizzo gives the *department and its process*; Rabiger gives the *principle*).
- **"Blueprints commit; changes are expensive" is the cheap-iteration argument inverted.** Rizzo's whole construction discipline exists because physical commitment is irreversible. A generative backend inverts that constraint — regeneration is nearly free — which is *why* the studio can afford to iterate a look the way an art department never could ([storyline 0006](../../../context/storyline/0006-renderer-seam-and-image-backend.md)).

Next: [Ch. 6 — A Legacy of Historical Techniques](ch06-legacy-of-historical-techniques.md) — the in-camera scenic craft that a generative model now collapses into a single step.
