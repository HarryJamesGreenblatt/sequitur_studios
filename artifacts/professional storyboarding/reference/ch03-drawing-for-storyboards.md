# Chapter 3 — Drawing for Storyboards

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 3.
> **Scope:** the mechanics of fast, readable drawing — a stroke alphabet, the disciplined rough, and shortcut shapes — all in service of *clarity over polish*.

## Core idea

Storyboards are disposable, produced by the thousand under tight deadlines, so the whole chapter is a doctrine of **economy in service of clarity**: draw only what communicates the action, as fast as possible, and no more. "Communication, not illustration" is the rule — if the drawing isn't *clear*, no amount of fancy rendering saves it, and time spent polishing a single figure is time stolen from the director. The skill being taught is not beautiful draftsmanship but the ability to state a pose, a prop, and a staging instantly with a handful of confident, recognisable shapes.

Everything flows from a small stroke vocabulary and a disposable-first mindset. Master a few marks until they are wobble-free and automatic, then build every object from simple primitives and silhouettes. The rough exists to solve *placement and staging* — where characters and objects sit within the environment relative to the story point — not to render surface. Detail is the last, optional step, added only if the job (and the director) demands it.

## The stroke alphabet — SICO

Everything reduces to four marks: **S-curves, straight lines (I), C-curves, and ellipses (O)**. Drill them like a golf swing — ghost the stroke above the paper, drop the pencil, aim for one smooth line. To change a line's angle, **spin the paper, not your stroke**. Combine them into 3–5-sided compound shapes. Carry a sketchbook everywhere and log constant pencil mileage; good or bad is irrelevant, the point is the mileage.

## The art of the rough

- **Know why you're roughing.** A pitch board may need no rough; an agency/overseas-animation board must be clean/"on model" enough for outsiders to read. The director's taste (tight vs. loose) also decides. Match the rough's finish to its use.
- **The storyboard artist's rough solves staging, not figure quality.** Expect to rearrange characters many times before finishing — so draw **"easy to draw, painless to erase."** Never over-invest in a rough figure; getting attached is a waste of time and heartbreaking when it's moved.
- **"Marble slabs," not feathers.** Rough figures should be distinct masses with clear size, boundaries, and obedience to perspective — not fuzzy, ambiguous blobs. A good rough lets a director see *exactly* what's happening: how tall the character is, body type, pose, even foreshortening — all before any face, clothing, or shading exists.
- **Stage with the whole body.** Rough at a level where **body language alone** carries the emotion; then any facial expression added later is "icing." Beginners over-rely on the face, which burdens weak expression-drawing and limits storytelling. (Trick: draw the figure headless/armless first, add those last.) Keep rough proportions honest — the standard adult is ~eight heads tall, with landmarks (crotch at 4, navel at 3, knees just above 6) as freehand checks.

## Shortcut shapes

- **Silhouette does the work.** A clear outline conveys an object's thickness, roundness, and identity with no interior detail. Block the primitive form (cylinder, cube, sphere) → add structure → finish with minimal detail. Don't over-render.
- **Figures:** simplify bodies, hands, faces to read the pose/expression, not the detail. "Star people" (or a tapered block for male, diamond-torso for female) are complete-enough characters from a few lines.
- **Poses:** break the figure into **head → torso → hips → limbs**, drawn top-down; offsetting torso and hips creates weight and flexibility.
- **Hands:** a box plus five sausages. **Heads:** a sphere with axis lines (nose "carrot") to aim the gaze and angle. **Eyes:** pupils + eyebrows alone can carry expression and eyeline; an oval pupil points the look. Speed here is what lets you communicate ideas at all.

## Studio application

- **This chapter is the *rationale* for keyframe fidelity, not a code spec.** It is the least directly code-bearing chapter, and its lesson is exactly why an [`ImageStudio`](../../../sequitur/image.py) reference keyframe needs to convey only *staging and shot intent* — who is where, at what size, in what pose and framing — and **not** final rendered look. The board panel is deliberately "communication, not illustration"; the conditioning keyframe serves the same role, so effort should buy *clarity of composition*, not polish.
- **"Clarity over polish" governs how much the prompt should specify.** A [`Shot`](../../../sequitur/shot.py) and its [prompt](../../../sequitur/prompt.py) should nail the readable essentials — subject, pose, staging, [framing](../../../sequitur/crew/camera.py) — the way a rough nails placement, and leave surface detail to the render, rather than over-describing texture the way an artist would waste time over-rendering a rough.
- **Body language before the face — a note for the crew's intent.** The rough's discipline (stage emotion through the whole body first) is a useful prior for any future Storyboard-Artist [`Contribution`](../../../sequitur/crew/role.py): describe the *pose and staging* that carry the beat, letting expression be a refinement. This dovetails with performance grounding in [Directing Ch. 19 — Acting Fundamentals](../../directing/reference/ch19-acting-fundamentals.md) and the storyteller's-voice framing in [The Screenwriter's Taxonomy Ch. 5 — Voice](../../the%20screenwriter's%20taxonomy/reference/ch05-voice.md).
