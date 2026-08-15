# Chapter 2 — The Responsibilities, the Relationships, and the Setup

> Abridged from Michael Rizzo, *The Art Direction Handbook for Film & Television* (2nd ed., Routledge/Focal Press), Ch. 2.
> **Scope:** the three axes of the art director's job — the **hierarchy of responsibilities** (who the seat answers to), the **relationships** (the departments it interfaces), and the **setup** (the roster of seats it hires and what each owns). This is the department the studio's planned Production Designer seat sits atop.

## Hierarchy of responsibilities

Rizzo orders the art director's loyalties as four widening "responsibilities," from the closest creative bond outward to the business of the studio. The through-line is that the art director is "a servant to many masters," in constant "push-me-pull-you" allegiance to creative, political and financial forces at once.

| Order | To whom | The duty |
|---|---|---|
| **First** | the **Production Designer** | be a credible ally and emissary; defend the vision; manage the **set budget** — linked to the script's "visual shopping list" — with the Construction Coordinator; be *always ready*: know the script and every revision cold, keep expense data at your fingertips |
| **Second** | the **Art Department** | leader-protector — hire only the best, keep the "machine well-oiled"; the **art department coordinator** is the key interface and most valuable player; own the archiving and server infrastructure |
| **Third** | the **Director** | the "other boss," holding the primary vision for the look; *read* the director (verbal / "actor's director" vs. exceedingly visual); **amalgamate** the director's and designer's visions while staying neutral — translate and maintain the unity of both "primary" visions through **active listening** |
| **Fourth** | the **Studio / UPM / film-as-product** | a straightforward business relationship: **economies of scale**, efficiency, budget adherence, avoiding bottlenecks; plus watchdog duty to the union (deal memos and paperwork in order) |

The Third responsibility carries the chapter's key design idea: when the director's and designer's visions diverge, the art director's job is **not** to inject a third (however brilliant) but to hold both primary visions coherent — "a servant to many masters."

## The relationships

The art department is the "imagery hub" of production — "keeper of the visual concept" and a strategic guide for every other department (Rizzo's "wheel of art-department influence"). Running it is **relationship marketing**: an exchange of services, ideas and value meant to build long-term, reusable working relationships, because "life and work continue beyond any particular film project."

| Department / seat | What the interface is for |
|---|---|
| **Head Accountant & staff** | money flow — payroll, fast vendor-check turnaround; Rizzo makes it a first-day PR stop |
| **Locations Manager & staff** | logistics of locations-as-sets: which locations satisfy the concept, access, parking, what can and can't be done; joint community PR |
| **UPM / Production Supervisor / Production Office** | the other nerve centre, where all final decisions are made; the rule — *never bring the producer your problem; bring them their problem, with solutions* |
| **First Assistant Director & staff** | the shooting crew and the **hot set** are the 1st AD's domain, not the art director's; the art director supervises the *extended* art department on set (on-set dresser, prop person, carpenter, scenic artist) and keeps the 1st AD updated |
| **Pre-visualization / VFX Supervisor & staff** | the merging art-dept ↔ VFX relationship; pre-vis has become a "third master" whose needs are often out of step with construction's — the art director brokers the merger |

## The setup: the art-department roster

The art director builds the department by hiring and supervising a roster of seats. Rizzo's organising framing: the **Production Designer and Art Director define the concept's *structure*; the Set Decorator provides its context, subtext and texture** — the visual narrative that turns "impressive but empty icons" into a set that speaks.

| Seat | Owns |
|---|---|
| **Art Department Coordinator** | logistics (a "logistical angel"), the department's tone, research-anything speed, and **clearances** |
| **Archivist / Digital Asset Manager (DAM)** | cataloguing and trafficking the thousands of images the department generates; the server |
| **Digital Artists / Set Designers** | 2D/3D imagery and drafting (Photoshop, Rhino, Vectorworks); "the computer won't make a bad designer good, but it makes a good designer faster" |
| **Set Decorator** | context, subtext, texture — the visual narrative; "the most valuable player" in the department |
| **Leadman** | the decorator's on-the-ground man; the swing gang who physically dress the set |
| **Greensman** | greens and landscape dressing — an extension of set-dressing to the outdoors |
| **Prop Master** | everything an actor touches — hand props; **hero props go past the Art Director before any extreme close-up** |
| **Construction Coordinator** | the physical, structural build; the head carpenter's crew; the Lead Scenic Artist's paint, texture and aging |
| **Mechanical Special Effects (SFX)** | mechanical scenery; heavy overlap with construction ("Special Effects Supervisor") |
| **Stunts** | breakaway scenery and props; straddles below-the-line and the directing department |
| **Transportation ("transpo")** | picture / hero vehicles; tightly tied to the locations department |

The recurring lesson: the art director's supervision reaches "into many creative areas" — the concept is controlled "down to the design of a matchbook" by whoever owns each seat, all kept coherent by lists, schedules and consistent decision-making.

## Studio application

- **This chapter is the org chart the planned Production Designer seat presides over.** Rizzo's roster is a map of *responsibilities that must be owned somewhere* before an image is rendered. In the studio those responsibilities collapse onto one seat feeding [`ImageStudio`](../../../sequitur/image.py): concept (Production Designer), decoration and subtext (Set Decorator), props and texture all become *elements of a single prompt* the seat composes via [`build_prompt`](../../../sequitur/prompt.py) rather than separate crews.
- **The "hierarchy of responsibilities" is the seat's reconciliation order.** Rizzo's First→Fourth loyalty stack maps onto the crew's decision flow: the planned seat answers first to its own visual concept, then to the [`Director`](../../../sequitur/crew/director.py) — the "other boss" holding the shot's intent — reconciling both into the [`Brief`](../../../sequitur/crew/role.py) the way Rizzo's art director holds the designer's and director's visions coherent without injecting a third.
- **"The Set Decorator provides subtext" is the seat's prompt-detailing remit.** The structural concept (period, palette, space) is the frame's spine; the decorator-level detail — props, wear and the "local reality" that carry subtext — is exactly the descriptive layer a generative prompt needs so the frame stops reading as an "empty icon." Both live in the same `build_prompt` payload.
- **The VFX / pre-vis "third master" is already the studio's native condition.** Rizzo's art department is straining to merge with a digital pipeline; the studio *is* the merged pipeline — `ImageStudio` is a generative backend, so the planned Production Designer seat is precisely the one Ch. 2 is reaching toward. See the image-backend seam ([storyline 0006](../../../context/storyline/0006-renderer-seam-and-image-backend.md)) and the crew's behaviour contract ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)).

> **Overlap flag:** Rizzo Ch. 2 (the art department's *relationships and setup*) overlaps [Directing Ch. 23 — Planning the Visual Design](../../directing/reference/ch23-planning-the-visual-design.md). Directing gives the **single chapter of principle** — how a director thinks about visual design; Rizzo gives the **whole department and process** — who answers to whom, which departments interface, and every seat that must be filled. Ground the studio's *seat* on Rizzo; ground the *director-facing rationale* on Directing Ch. 23.

Next: [Ch. 3 — Visual History](ch03-visual-history.md) — the period, era and style vocabulary the concept needs (arc B owns this chapter).
