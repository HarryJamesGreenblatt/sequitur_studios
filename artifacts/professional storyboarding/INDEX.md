# Professional Storyboarding — grounding index

Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb*
(Focal Press, 2013 · ISBN 9780240817705). This is the studio's **previsualization**
grounding — the craft of turning a script into a shot-by-shot *visual* plan **before**
anything is shot (or, here, rendered). It sits in the plan phase between the
Screenwriter/Director's decisions and the shoot crew, and it maps unusually cleanly
onto the code: a storyboard **panel** encodes the same grammar the cinematographer
owns (shot size, angle, composition, movement), so a board is effectively a
*pre-rendered* [`Shot`](../../sequitur/shot.py), and board panels are the literal
form of the **reference keyframe** the video studio conditions a shot on
([`ImageStudio`](../../sequitur/image.py)).

> **Abridged (10 ch) — 0018.** The verbatim `source/` (10 curated chapters — the
> book's career/business chapters 11–12 were dropped at import) has been abridged into
> 10 session-ready [`reference/`](reference/) chapters, each ending in a **Studio
> application** section. The chapter → code map below links each reference; the
> **Storyboard Artist** role it grounds does not yet exist in code, so the mappings are
> **provisional leads**.

## Folder layout

- [`extraction/`](extraction/) — the raw `.docx` originals + extracted media. *(gitignored)*
- [`source/`](source/) — pandoc-converted verbatim Markdown, the **ground truth**. *(gitignored)*
- [`reference/`](reference/) — abridged, session-ready references (10 chapters). *(ships)*

## Chapter → (planned) role map

All chapters ground a future **Storyboard Artist** (plan phase / previz). The bold
chapters are the ones that most directly become code — the shot grammar, the staging
decision, the deliverable taxonomy, and the previz workflow.

| Ch | Reference | Grounds |
|----|-----------|---------|
| 1 | [Overview](reference/ch01-overview.md) | the board as the **plan-phase deliverable** — decide shots on paper before paying to render (the analogue of `--dry-run` prompt composition) |
| 2 | [Visual Literacy](reference/ch02-visual-literacy.md) | the compositional vocabulary (line/shape/value/contrast, focal point, depth) overlapping the DP's `Composition`/framing enums in [`crew/camera.py`](../../sequitur/crew/camera.py) |
| 3 | [Drawing for Storyboards](reference/ch03-drawing-for-storyboards.md) | why a keyframe favours **clarity of staging over render polish** — a `ImageStudio` keyframe need only convey composition, not final look |
| 4 | [**Cinema Language**](reference/ch04-cinema-language.md) | the board-artist's shot grammar — where `ShotSize`/`CameraAngle`/`CameraMovement` are **first committed**, upstream of the DP (overlaps *Grammar of the Shot* Ch. 1–3) |
| 5 | [Story Structure](reference/ch05-story-structure.md) | the plan-phase structure the edit `Sequence` later realises (overlaps Taxonomy Ch. 6 · Directing Ch. 5) |
| 6 | [Emotion](reference/ch06-emotion.md) | the affective **intent** that biases the DP/lighting heuristics — a global style contract (overlaps Directing Ch. 10–11) |
| 7 | [**Staging**](reference/ch07-staging.md) | fixes **subject + camera placement before the DP arrives** — the plan-phase source of truth for coverage |
| 8 | [**Storyboard Types**](reference/ch08-storyboard-types.md) | the taxonomy of the **deliverable** + its per-purpose fidelity → `ImageStudio` keyframe usage (thumbnail vs. finished keyframe); **previs = the closest analogue to Sequitur's own pipeline** |
| 9 | [**Storyboarding**](reference/ch09-storyboarding.md) | the plan-phase **workflow**: script breakdown → thumbnail → per-panel `Shot` → keyframe (the `Brief` → `Contribution` → `Director` reconcile → keyframe chain) |
| 10 | [**Advanced Storyboard Techniques**](reference/ch10-advanced-storyboard-techniques.md) | encoding **motion & time** in a still — the board analogue of the video-only faces `build_prompt` adds over `build_image_prompt` |

## Scope note

This source grounds a seat the architecture had gestured at but never modelled: the
**Storyboard Artist / previz** role. Its payoff is unusually concrete because the
studio *is* a generative previs pipeline — where a traditional board is a drawing that
plans a shot, Sequitur renders that plan directly. The chapter that makes this clearest
is **Ch. 8 (Storyboard Types)**: a *continuity board* is the ordered `Shot` list, an
*animatic* is the assembled edit, and *previs* ("rough 3D block-out with accurate
lenses, cut into an animatic") is functionally what [`studio.py`](../../sequitur/studio.py)
plus the edit layer produce.

It **overlaps** several existing sources — but from the board artist's upstream lens:
Cinema Language (Ch. 4) and Staging (Ch. 7) restate *Grammar of the Shot*'s composition
and coverage grammar as decisions made *before* the shoot; Story Structure (Ch. 5)
echoes the Taxonomy's Pathway and Directing's plot/structure; Emotion (Ch. 6) restates
Directing's tone/style as the intent behind each shot. Reconcile these when the
Storyboard Artist role is encoded — it is the plan-phase seat that **commits the shot
grammar first**, and the DP on the shoot executes what the board decided.
