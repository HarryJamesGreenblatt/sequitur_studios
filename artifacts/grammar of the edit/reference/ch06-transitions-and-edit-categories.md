# Chapter 6 — Video Transitions and Edit Categories

> Abridged from Christopher J. Bowen, *Grammar of the Edit* (4th ed.), Ch. 6.
> **Scope:** the mechanics and meaning of the four transitions (cut, dissolve,
> wipe, fade), the **handles** they require, and the five **edit categories**
> (action, screen-position, form, concept, combined). This is the source for the
> future `movie.py`'s **atomic transition ops** and its **why-this-edit-works**
> patterns.

## Heads, tails, handles (the load-bearing technical concept)

- A clip has a **head frame** (start) and **tail frame** (end); you mark **IN/OUT**
  on a master clip and edit that span in. At a cut, the outgoing clip is the
  **A-side**, incoming is the **B-side**.
- **Handles** = the unused master-clip frames *before* IN (head handle) and *after*
  OUT (tail handle). **Every transition except the cut and some fades needs
  handles** — a 1-second dissolve at 30fps borrows 15 frames from A's tail handle
  and 15 from B's head handle. **No handles ⇒ no dissolve/wipe** (software fakes it
  with a spottable freeze frame).

## The four transitions

| Transition | Meaning / used when | Needs handles? |
|-----------|---------------------|----------------|
| **Cut** | Instantaneous; continuous action, sudden impact, change of info/location. The default ("invisible" if it obeys the six factors). Variants: **punch-in / axial edit** (same lens axis, closer), **smash cut** (abrupt jump). | No |
| **Dissolve** | Gradual blend (superimposition); change of time/location, condense time, calm/somber mood, strong visual link. Audio **cross-fades**. **Match dissolve** links shapes; **soft cut** = few-frame dissolve. | Yes |
| **Wipe** | A line/shape pushes A off, reveals B; fanciful, change of time/location with *no* visual link, scene/act ends. **Natural wipes** ride an in-frame edge; often a **swoosh** SFX. | Yes |
| **Fade** | To/from solid color (usually black); program/act/scene boundaries. **Fade-in** opens, **fade-out** closes; **dip to black / kissing black** between segments. Low-contrast frames fade cleanest. | No (applied to timeline frames) |

## The five edit categories (why an edit works)

Each is evaluated against Ch. 5's six factors:

1. **Action edit** (movement/continuity edit) — a **straight cut on continuous
   action**; the movement motivates the cut and must **match** across it (hence
   "match cut"). Cut partway through the action (one-third out / two-thirds in), and
   start the incoming shot ~3–5 frames early — the eye reorients and "loses" them.
2. **Screen position edit** (directional/placement edit) — subject placement
   **directs the eye across the frame**; the classic shot/reverse dialogue (A frame-
   left looking right → B frame-right looking left). Usually a cut.
3. **Form edit** (graphic edit) — match **shape/color/composition** across the cut;
   usually a **match dissolve** (spinning wheels jet→car→bike→wagon; cigarette packs
   → headstones). Nearly always **preconceived** in pre-production.
4. **Concept edit** (dynamic/idea/intellectual montage) — **juxtaposition creates
   implied meaning** not stated in the story (marriage question → prison-shackles
   shot). Powerful but risky: unclear meaning reads as confusion.
5. **Combined edit** — a single edit that satisfies **two or more** of the above at
   once (e.g. an action edit that is also a screen-position edit) — the most
   seamless and sophisticated.

## Studio application

The atomic op-set and pattern library for a future **`movie.py`** (provisional —
no code yet):

- **Handles are a genuine constraint on fixed-length Omni shots.** Because
  dissolves/wipes *require* handle frames, an assembler working from ~10s clips must
  either (a) request **coverage longer than the used span** so every shot ships with
  head/tail handles, or (b) restrict itself to **cuts and fades**, which need none.
  This is a concrete instruction back to the **shots→scenes→acts** generator:
  *generate handle padding* if transitions beyond cuts are wanted.
- **The four transitions are the assembler's output vocabulary**, each with a
  machine-checkable "used when" (cut = continuous/impact; dissolve = time
  compression/somber link; wipe = fanciful location change; fade = act boundary).
- **The five edit categories are the "why-this-edit" templates** the cut-decision
  engine (Ch. 5) selects among — action edit for continuous motion, screen-position
  for dialogue, form/concept for the deliberate, preconceived meaning-making that
  must be **planned upstream** (pre-production), not discovered in post.
- **Form & concept edits argue for pre-production authorship.** Since these are
  "preconceived," the studio's pre-production layer should be able to *mark intended
  match/concept edits* in the plan so production generates the matching shapes and
  post executes them — a clean seam between the phases.
- **Act/scene structure lives in the fade.** Fades and dips-to-black are the
  natural encoders of the **shots→scenes→acts** boundaries the assembler must honor.
