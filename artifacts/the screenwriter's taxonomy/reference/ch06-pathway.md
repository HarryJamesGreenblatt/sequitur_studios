# Chapter 6 — Pathway

> Abridged from Eric R. Williams, *The Screenwriter's Taxonomy*, Ch. 6.
> **Scope:** the fifth layer — **Pathway**, the *trajectory* along which the audience
> moves through the story. Where Voice is the vehicle, Pathway is the road.

## Core idea

Regardless of genre, every story sends its protagonist along a **pathway** — a
subconscious atlas that guides the audience. The **traditional** pathway (most
Hollywood films) has **five elements**:

1. **One central protagonist** goes through a change (*except Romance* — two equal
   protagonists).
2. **Audience and protagonist learn at the same time.**
3. The protagonist follows the **Hero's Journey** (leave home → adventure → learn →
   return).
4. The central payoff is **protagonist battling antagonist.**
5. In the end the **hero is victorious and rewarded** (even in death).

Every other pathway **breaks at least one** of these five. There are **20 pathways**
in seven families. (Note: several were historically miscalled "genres" — *Noir*,
*Screwball* — but they fix trajectory, not Story/Character/Atmosphere, so they are
pathways.)

## The 20 pathways, by divergence family

| Family | Pathways | Breaks the traditional rule of… |
|--------|----------|---------------------------------|
| **Defeated underdog** | Noir · Tale of Madness · Rags-to-Riches-to-Rags | #4/#5 — the real foe is a *larger force* (society, insanity); the hero is destroyed / survival is the only "win" |
| **Underdog + subverted journey** | Melodrama | #1/#5 — protagonist rarely changes; catharsis happens *in the audience*, not the hero |
| **Subverted journey** | Chase/Hunt · Road Movie | #3 — the hero never returns home; is prey, or perpetually in transit |
| **Multiple protagonists** | Buddy Movie · Screwball Comedy · Reunite the Gang · Unlikely Ensemble | #1 — story split across several leads at odds with one another |
| **Multiple protagonists + unknowing audience** | Reunion · Gang Falls Apart | #1/#2 — audience plays "catch up"; joins relationships already in progress |
| **All-knowing audience** | Coming of Age · Lost Innocence | #2 — audience *remembers* rather than learns; watches an awakening |
| **Noncharacter antagonists** | Fish Out of Water · Human vs. Nature/Self/Society/Technology | #4 — the "antagonist" is nonsentient: environment, disaster, the self, society, a machine |

**Craft notes worth keeping:**

- **Noir** = sustain distrust/despair via *location, mounting situation, or isolation*
  — the hero loses even when he wins (*Casablanca*).
- **Melodrama** hooks with Hero's-Journey expectations, then veers into tragedy once
  the audience is invested (*Million Dollar Baby* turns at ~p.90).
- **Multi-protagonist pathways run long** — pages divide across leads; map each
  character's arc (and, for *Gang Falls Apart*, the *order* of each demise).
- **Noncharacter-antagonist pathways** escalate *circumstance*, not a villain (same
  ridge in Act I and III, but the starving hero now can't climb it).

## Studio application

- **Pathway is a closed ~20-value enum with a built-in derivation rule.** Because each
  pathway is defined as "*which of the 5 traditional elements it breaks,*" the enum can
  carry that metadata — a `Screenwriter` role owns `Pathway`, and each value knows its
  divergence flags (single-vs-multi protagonist, audience-ahead-vs-together,
  returns-home, sentient-vs-nonsentient antagonist, hero-wins).
- **Those divergence flags are exactly the fields the shoot/post crews need.** "Multiple
  protagonists" tells the DP/Editor to allocate coverage and screen time across leads;
  "audience knows more than the protagonist" is a *dramatic-irony* setting the
  [Editor](../../../sequitur/crew/editorial.py) can exploit (reveal timing); "nonsentient
  antagonist" tells the Sound/Production-Design departments the "threat" is
  environmental. Pathway is the story layer's instruction to the **edit's sequence
  shape** — the plan-phase counterpart of the [`Sequence`](../../../sequitur/edit.py)
  the post layer assembles.
- **Pathway pairs with POV to prevent a "pendulum" of protagonist focus.** A
  multi-protagonist pathway + a chosen [Point of View](ch07-point-of-view.md) (e.g.
  secondary-limited) is what stops an agent from snapping camera/edit attention to
  whichever character is momentarily loudest — the story-layer echo of the
  proximity-weighted target-selection discipline used in the studio's dynamics work.
- **Melodrama's "hook then veer" is a pacing directive.** "Traditional for ~90 pages,
  then turn" is a *time-motivation* cue the cut-decision engine
  ([Grammar of the Edit Ch. 5](../../grammar%20of%20the%20edit/reference/ch05-when-to-cut.md))
  can honor — pathway sets the macro rhythm, the editor executes the micro cuts.

Next: [Point of View](ch07-point-of-view.md) — who drives the vehicle down the pathway.
