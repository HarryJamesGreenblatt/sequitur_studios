# Chapter 7 — How to Direct the Eyes

> Abridged from Francis Glebas, *Directing the Story: Professional Storytelling and Storyboarding Techniques for Live Action and Animation* (Routledge/Focal Press), Ch. 7.
> **Scope:** the two visual jobs of every shot — telling the eye *where* to look and *what* it is looking at — and the design grammar (elements, principles, effects) the director uses to lead attention to the story point and control how the frame *feels*.

## Core idea

To make a film legible a director must do two things for the audience, in order: **direct the eyes where to look**, then let them **recognise what they are looking at**. Beginners fixate on the *content* of an image (does it look like the thing?) and stay blind to its *structure* — where things sit on the frame, the pattern of light and dark, the flow of the eye. Structure has no form of its own; it is the *form of the content*, and it "speaks" more powerfully than content because it works below the threshold of awareness. Directing the eye is therefore a structural craft, and it is decided at the moment the shot is *staged and composed* — not fixed later. The real staging question is never "where do I put the camera?" but "how do I stage this to be clear and to produce the mood that enhances the story?"

## Three ways to direct the eye

The director controls attention through three nested choices, from coarse to fine:

1. **Point the camera** — choosing *what part* of the scene the audience can see at all.
2. **The frame** — what it *includes* and what it *cuts off* (offscreen space is a decision, not an accident).
3. **Composition within the frame** — the designed arrangement of elements that leads the eye to the focal point and loops it back.

## Seeing is active — make objects read

The audience is not passively watching; seeing is a hunt (or, in a modern idiom, *shopping*) — the eye scans and ignores most of what it sees until something interesting catches it. Viewers seek not just *what* a thing is but *what it means to them*. So the director must present objects so they **read easily**:

- **Characteristic viewpoint / silhouette** — show an object from the angle that gives its most recognisable outline. People read from the front or side, rarely from directly above or below. A "dynamic" high angle chosen for its own sake usually just confuses; choose the angle because it supports the story.
- **Enough traits, not all of them** — present only enough identifying features to suggest the thing; the audience's mind fills in the blanks. Objects need not even exist in reality (the *flux capacitor*) — suggest what it is and does, and the viewer goes along for the ride.

## The design equation

The whole toolkit reduces to one formula:

> **Elements + Principles = Effects**

| **Elements** (what is on the frame) | **Principles** (how they are organised) | **Effects** (illusions the viewer completes) |
|---|---|---|
| points, lines, planes, edges, shapes, values, sizes, colours | balance, position, dominance, unity, alternation & repetition, contrast & similarity, symmetry, rhythm | light, depth, volume, form, motion, temperature, atmosphere |

- **Elements** are the raw marks actually on the frame.
- **Principles** subordinate many elements to a greater order. **Contrast is the most important principle** — when everything is similar, contrast is what makes a difference visible. Crucially, the principles are **not just visual**: they apply to *every* aspect of film — performance, lighting, story design, and sound design.
- **Effects** are the illusions the flat screen manufactures once elements are organised by principles. Good design is grounded in the body's own rhythms, balance, and directions — let the body be the guide (it needs negative space to move, it balances and counterbalances, it reaches upward against gravity).

## The two enemies: boredom and confusion

Every design failure is one of these two. Use the principles to fight both.

| **Boredom** (too little order broken) | **Confusion** (too little order imposed) |
|---|---|
| evenness — no variation of interest | bad tangents that flatten space and snag the eye |
| predictable repetition | chaos with no organising idea |
| dead symmetry | crowding with no breathing room / negative space |
| — | high contrast and "spottiness" that is hard to read |
| — | no centre of attention — the eye doesn't know where to look |

Fixes: the *simplest* change (a tonal gradation, a shifted angle) begins interest; provide transitions and **cluster darks together** to avoid spottiness; leave breathing room; and always give the eye a clear centre of attention plus *time to read it*.

## Composition: diversity with unity

Composition is the positioning and rhythm of all parts around a centre of interest. Plato's summary holds: **composition is diversity with unity** — diversity supplies interest (against boredom), unity supplies belonging and order (against confusion). Three working guidelines follow:

1. **Create a centre of attention.** The eye goes to the area of **greatest contrast**. Force it with dominance and contrast, with selective **focus** (sharp figure against a soft-focus field — a strong figure/ground pop), or with **light** (silhouette a figure against a light ground, or light it against a dark ground; backlight for a separating halo). *Every shot is a close-up of what you want to say* — even a shot as wide as the universe.
2. **Keep the eye moving inside the frame.** The eye scans automatically; give it **pathways** — use elements as arrows. Ideally build a **loop** that travels the frame and returns to the focal point.
3. **Block the exits.** Kill any unintentional arrow or pathway that leads the eye *out* of the frame.

**"Look where I am looking."** The most powerful single device: the eye follows the *eyes of characters*. This is the base grammar of cinema — a character looks, then a cut shows what they see.

## Reading the frame — direction and simplicity

- **Compositional reading order.** The eye scans a picture the way it reads — left-to-right, top-to-bottom (culture-relative). Treat the image like a joke: the "punch line" should land *last*, so orient key reveals to the right. For geography, follow **map orientation** — west left, east right (a plane flying New York→LA points left).
- **Keep movie composition simple.** Movement complicates reading (you can only take in so much of a passing billboard at speed). Use only significant movements; position the camera for clean silhouettes and separation from the background; move the camera *with* the action rather than adding competing motion.
- **Base compositions on simple shapes.** Letter shapes read fast — **C, S, L, T, X, Z** — plus spirals, sunbursts, and (very powerful) **triangles**. Interlock shapes like a jigsaw. Circles are tricky (their strong closure resists integration) — prefer partial circles. Subdivide the frame on **thirds**; avoid halving (usually boring); off-set a centred figure with elements to each side.

## Composition is subtext

Every shape, line, and composition carries a feeling — Glebas names it *analogical morphology* (the composition's shape is analogous to an emotion, which is why different people draw the same emotion abstractly in strikingly similar ways). So **composition is subtext**: like a music score, the images tell you *what* is happening while the compositional structure tells you *how to feel*, and position in the frame encodes **power relationships** between characters. When text and subtext pull against each other, the tension is the point — and the subtext often carries more truth than the text. Compose deliberately: know what you are saying.

## Light and shadow

Ultimately film is light and shadow — stay aware of the dark/light pattern independent of content. **Notan** (Japanese "dark-light") treats a shape and its background as separate but equally important (yin/yang). **Counterchange** weaves the frame by placing light over dark and dark over light; the seam where the values meet is a **value passage**, and shared values unify the composition.

## Studio application

- **"Directing the eyes" is the *why* behind the plan-phase composition enums the camera department already owns.** Glebas's centre-of-attention, arrows/pathways, and shape-based framing are exactly the decisions encoded in [`Composition`](../../../sequitur/crew/camera.py) (`CENTERED` vs `RULE_OF_THIRDS`), [`SubjectView`](../../../sequitur/crew/camera.py), and [`ShotSize`](../../../sequitur/crew/camera.py) — set on the [`Shot`](../../../sequitur/shot.py) *before* the shoot and then executed by the renderer. His "characteristic viewpoint / best silhouette" rule is the intent behind picking a `SubjectView` and `CameraAngle` that make the subject read, not merely one that is "dynamic."
- **The design equation is the studio's argument for staging as a first-class, pre-shoot decision.** Elements + principles + effects map onto what [`prompt.py`](../../../sequitur/prompt.py) has to make legible: it leads with the framed subject, layers camera and lighting language, and drops the moving parts for the still backend — so the "one clear centre of attention" rule is what a good prompt enforces, and a shot that reads as *confusing* (no dominance, competing centres) is a prompt/[`image.py`](../../../sequitur/image.py) legibility failure to catch, not a rendering tuning problem.
- **"Composition is subtext" grounds the [`Director`](../../../sequitur/crew/director.py)'s read of whether an image *means* what the beat needs.** The Director reconciles the crew's owned fields into one `Shot`; this chapter says the reconciler must also judge the frame's *feeling* — does the structure (power position, light/dark pattern, shape) say what the story point says? That judgement is the hook for a persona reconciler over this grounding rather than a purely mechanical merge ([storyline 0016](../../../context/storyline/0016-abridging-the-screenwriters-taxonomy.md)).
- **Light/dark, figure-ground, and counterchange are shared vocabulary with the grade and DP seats.** The notan/value-passage logic here is the compositional half of the same craft the colour and lighting layers execute; keep "cluster the darks, separate the figure, block the exits" as a cross-department legibility check, not a camera-only note.

> **Overlap flag:** Glebas's eye-direction (this chapter) reconciles with **[Grammar of the Shot Ch. 2 — Shot Composition](../../grammar%20of%20the%20shot/reference/ch02-shot-composition.md)** and **[Professional Storyboarding Ch. 7 — Staging](../../professional%20storyboarding/reference/ch07-staging.md)**. Glebas gives the *why* — leading the audience's eye to the story point and using composition as subtext; Grammar of the Shot gives the *compositional grammar* that becomes the [`Composition`](../../../sequitur/crew/camera.py) enum; Professional Storyboarding gives the *pre-visualisation* of that staging. The Director stages for meaning, the DP encodes the grammar, the board previsualises it.

The frame so far is flat — the next chapter pushes the same eye-direction *into depth and across the cut* with perspective, lenses, and proximity ([Ch. 8 — Directing the Eyes Deeper in Space and Time](ch08-directing-the-eyes-deeper-in-space-and-time.md)).
