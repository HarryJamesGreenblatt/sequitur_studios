# Chapter 7 — Point of View

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy*, Ch. 7.
> **Scope:** the sixth (and, Williams argues, most important) layer — **Point of
> View**: how much the audience knows, and through whom. "Who's driving the car?"

## Core idea

From the outset the writer decides **how much information the audience gets**. POV is
a **decision tree of three questions** — answer all three and you have named the
screenplay's POV. Adjusting it later can be a "page-one rewrite," so decide early.

## The three axes

1. **Limited or Omniscient?** — *scope.* **Limited** confines the audience to what one
   (or, in a Buddy/Romance, two) character(s) know; if the protagonist doesn't see it,
   neither do we (*127 Hours*). **Omniscient** lets the storyteller reveal *any*
   character at *any* time — cross-cut to build tension the hero can't (*The Bourne
   Identity*).
2. **Primary or Secondary?** — *focus.* **Primary** = told through the protagonist
   (*Escape from Alcatraz* stays with Frank Morris). **Secondary** = told through
   another character (*Shawshank* through Red) — lets the writer **withhold/reveal**
   (Andy's 20-year plan lands as an Act-III reveal) and hand the audience backstory the
   protagonist couldn't know.
3. **Objective or Subjective?** — *stance.* **Objective** presumes a universal truth;
   what we're shown is "true" (*Apollo 13*). **Subjective** puts reality in question —
   unreliable narrators, skewed/lying/misinformed perspectives (*Memento*, *Gone Girl*,
   *Shutter Island*).

## The combinations

The three axes multiply into named POVs the writer can craft to match theme and
pathway:

| POV | Reads as | Example |
|-----|----------|---------|
| **Filmmaker Omniscient** | characters have no narrative voice; objective tour | *Airplane!* |
| **Primary Omniscient** | protagonist's biased lens, can go anywhere, often retrospective | *American Beauty*, *A Clockwork Orange* |
| **Primary Limited** | single subjective lens that *feels* authentic/objective | *The Diving Bell and the Butterfly* |
| **Secondary Limited** | the story is *about* the lead, *told by* another (unusual, powerful) | Sherlock via Watson; *Shawshank* via Red |
| **Secondary Omniscient** | a reflective/all-seeing side character narrates | *The Hudsucker Proxy* (Moses), *No Country* |

A subjective element can also **hide inside** an omniscient frame — *A Beautiful Mind*
renders Nash's hallucination as objective "truth" until the reveal.

## Studio application

- **POV is three small enums, not one** — `Scope(LIMITED|OMNISCIENT)`,
  `Focus(PRIMARY|SECONDARY)`, `Stance(OBJECTIVE|SUBJECTIVE)` — whose product yields the
  named POVs above. This is the cleanest enum in the source and the closest analogue to
  the multi-axis grammar in [`crew/camera.py`](../../../sequitur/crew/camera.py)
  (`ShotSize` × `SubjectView` × `CameraAngle`). A `Screenwriter` role owns all three.
- **POV is the *direct upstream of camera coverage* — the sharpest cross-department
  link in the whole taxonomy.** "Limited POV → never cut away from the protagonist;
  omniscient → cross-cut to what the hero can't see" is literally a **shot-selection and
  cut rule**: it constrains the DP's `SubjectView`/coverage and the
  [Editor](../../../sequitur/crew/editorial.py)'s cross-cutting. When the `Director`
  reconciles the crew ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)),
  the Screenwriter's POV field is a *hard constraint* on the shoot crew's proposals, not
  a hint.
- **The objective/subjective axis is a rendering-fidelity switch.** A subjective /
  unreliable POV licenses hallucinated or contradicted imagery (the *A Beautiful Mind*
  trick) — a signal the image/video backends can act on (dream logic, impossible
  geometry) that an objective POV would forbid.
- **Secondary POV is a withholding mechanism the edit executes.** "Tell it through Red
  so the escape is a reveal" is the same withhold-for-suspense logic in
  [Grammar of the Edit Ch. 5](../../grammar%20of%20the%20edit/reference/ch05-when-to-cut.md).
  Screenwriter sets *who narrates*; the Editor times *when the reveal cuts*.

> **Overlap flag (staging note 0015):** POV appears in **both** this source and
> **Directing Ch. 9** ("Cinematic Point of View"). Reconcile the two when this axis is
> encoded — the Taxonomy gives the *classification*, Directing gives the *craft* of
> executing it.

Final layer applied end-to-end in [Ch. 8 — Case Studies](ch08-case-studies.md).
