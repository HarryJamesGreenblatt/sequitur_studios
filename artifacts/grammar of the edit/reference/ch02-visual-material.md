# Chapter 2 — Understanding the Visual Material

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 2.
> **Scope:** the shot vocabulary *from the editor's side* — the continuity/matching
> pitfalls each shot carries into the cut — plus the **simple / complex / developing**
> shot categories. The shot *sizes* themselves are already grounded in
> [*Grammar of the Shot* Ch. 1–2](../../grammar%20of%20the%20shot/reference/ch01-the-shots.md)
> (`ShotSize`); this chapter adds what the **assembler** must reason about.

## Core idea

**Coverage** — the same action recorded from multiple viewpoints/magnifications
(master scene technique) — is what lets an audience feel present. The editor
**inherits** these shots without having shot them, so fluency in the shot
vocabulary is a core editorial responsibility: you must know each "word" to
juxtapose them into readable "sentences." A shot type is chosen on the set, but
its *consequences* land in the edit.

## The shot family, editorially (concern per size)

Sizes map 1:1 to the studio's `ShotSize`; what's new here is each one's **main
editorial concern** when cut into a sequence:

| Shot | Editor's main concern in the cut |
|------|----------------------------------|
| **ECU/XCU** (detail) | Needs a wider shot before/after for **context**; soft-focus risk; cryptic if isolated. |
| **BCU/choker** | Awkward, uncommon framing — use with clear purpose; best as a silent **reaction** insert; make-up/mouth-drop risks. |
| **CU** (head) | **Eye-line** — do the eyes look the correct direction (objective) or into the lens (subjective)? Emotional workhorse. |
| **MCU/bust** | **Composition & screen-direction continuity**; background competition; DoF. The single most common shot. |
| **MS/waist** | **Breaking frame**; match **headroom** and **look/nose room** across dialogue coverage. |
| **MLS/cowboy** | Distracting slivers/legs at frame bottom (esp. in motion) — a slight scale-up can rescue. |
| **LS/WS** | Face too small for **emotion**; whole body visible ⇒ easy to spot **continuity mismatches**. |
| **VLS** | Subject can get lost in background — is there enough usable info? |
| **XLS/ELS** | **Horizon level**; stray anachronistic objects (cell tower, wrong signage) in the wide vista. |

Two additional **dialogue-coverage primitives** (beyond the single-subject family):

- **Two-shot (2S)** — two subjects facing camera or each other. Tighter 2S implies
  intimacy/aggression (overlap, "favor" one). Adding people → 3-shot/group/crowd,
  staggered into depth. **Concern:** matching continuity/eye-line across the
  coverage is harder with 2+ people in frame.
- **Over-the-shoulder (OTS/OSS)** — favors one face, the other's head/shoulder makes
  an "L" at the frame edge. Shallow DoF blurs the near shoulder. **Concern (audio):**
  you often **layer in the CU audio** for the back-to-camera subject — exact sync
  isn't needed (mouth unseen), but watch jaw/head motion against the borrowed voice.

## Shot categories: simple → complex → developing

A shot's category depends on which of **four physical components** move *during*
the shot:

1. **Lens** — zoom / focal-length change (glass moves; camera still).
2. **Camera** — pan / tilt (body pivots on a fixed mount).
3. **Mount/support** — dolly, truck, crane/jib, pedestal, drone, gimbal/Steadicam
   (the whole rig travels).
4. **Subject** — the person/object moves.

- **Simple shot** — static frame; no lens/camera/mount motion (subject may move
  little). One viewpoint, one magnification.
- **Complex shot** — one such motion (e.g. a pan, or a zoom) alters the frame
  during recording.
- **Developing shot** — *multiple* components move together (e.g. dolly + pan +
  subject move), continuously re-composing — effectively several shots in one take.

Complexity matters editorially: the more a single take develops, the more it
resists being cut into, because its framing/motion is already in flight.

## Studio application

Grounds what a future **`movie.py`** assembler must *know about the shots handed
to it* — the provisional leads (no code yet):

- **Coverage is the input contract.** Omni-generated coverage (multiple ~10s views
  of one beat) is exactly the master-scene material the assembler receives; it must
  tag each clip by `ShotSize` so wide→tight ordering and reaction inserts are
  selectable.
- **The per-size "concern" column is the assembler's lint.** Eye-line direction,
  headroom/look-room matching, breaking frame, and horizon level are the
  **continuity checks** an agent should evaluate when choosing which coverage to cut
  together (deepened in [Ch. 5](ch05-when-to-cut.md)).
- **Two-shot & OTS are the dialogue-scene building blocks** — the primitives a
  scene-level assembler pairs for shot/reverse-shot; the OTS **audio-layering** note
  is an early hook for the production-dialogue thread (borrowing a clean CU voice
  under a back-to-camera frame).
- **Simple/complex/developing predicts cuttability.** A developing shot is
  self-contained and resists mid-take cuts; the assembler should treat clip
  *category* as a signal for whether a shot is a cut-in candidate or a hold.
