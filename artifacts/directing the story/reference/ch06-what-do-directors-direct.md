# Chapter 6 — What Do Directors Direct?

> Abridged from Francis Glebas, *Directing the Story: Professional Storytelling and Storyboarding Techniques for Live Action and Animation* (Routledge/Focal Press), Ch. 6.
> **Scope:** the director's core remit — to **capture the audience's attention and then protect it** — and the perceptual toolkit for doing so: contrast and motion, the map-is-not-the-territory filter, misdirection (ventriloquism / hypnosis), and the power of suggestion (gestalt closure).

## Core idea

The first — and defining — job of the director is to **capture and direct the audience's attention**, then guard it from distraction. Everything else follows. Attention is a scarce commodity: the mind is a filter that *deletes, generalizes, and distorts* the flood of sensory information so it doesn't overload, and it can consciously hold only one thing at a time. A director therefore works like a **ventriloquist and a hypnotist** — pointing the eye where it should go, misdirecting it away from the machinery, and letting the audience's own imagination do the heavy lifting. What the director directs is not actors or cameras first; it is **perception**.

## Getting attention

What stands out gets seen. The reliable attractors:

- **Motion, contrast, brightness, pointing-at, and loudness** — anything that breaks the pattern.
- **Strong contrast** especially; the mind notices sharp change but can miss changes that are too gradual.
- **Social pointing** — look up in a crowd and others follow your gaze; you have directed their attention with nothing but your own.

A dose of **controlled ambiguity** is the deliberate counter-move: sometimes you *withhold* clarity (is the character guilty? did the event even happen?) to keep the audience puzzling — too much spoils the soup, but a measured withhold is a tool (*Atonement*, *Last Year at Marienbad*).

## The map is not the territory

We never deal with the world directly — only with our **maps** of it (images, sounds, words, symbols). The brain filters to survive, organizing everything into **patterns**, and we notice even small breaks in a pattern. Two consequences for the director:

- **The camera and microphone have no filter.** They record everything indiscriminately — the dog barking half a mile away that your ear tuned out. Because the equipment doesn't know what matters, *you* must see and listen with trained sensitivity and decide exactly what to present.
- **Selective attention is fragile.** It is affected by fatigue, interest, state of mind, and expectation. "Multitasking" is really fast attention-switching, and it splits the very focus you are trying to hold.

## Misdirection: ventriloquism and hypnosis

Keeping the structure invisible is a misdirection craft. The ventriloquist offers three moves the director borrows:

1. **Contrast** the voices (self vs. figure) so each is distinct.
2. **Throw the voice** — the figure "speaks" without the operator's mouth moving.
3. **Move the figure's lips** to point the audience's eyes at it, engaging it as if it were alive.

Directing is the same two-sided act: **direct attention to the thing that "speaks,"** and **misdirect it away from the apparatus**. Like a hypnotist, the director controls the flow outside the viewer's conscious control — the conscious mind follows the story while the unconscious absorbs everything at the edges (the same scene in shadow versus sunlight *feels* different without anyone noticing why).

The **Ericksonian** techniques Glebas draws out are the storyteller's persuasion tools:

- **"What if…?" presented as true** — the writer is a masterful liar; the truth being sold is not the events but the *emotions*.
- **Embedded / narrative questions** set off unconscious searches — the audience hunts for answers from what it already knows.
- **Presupposition** — something assumed beforehand; a powerful lever to mislead or surprise when it turns out false.
- **Implication** — letting the listener reach a conclusion never stated; makes dialogue believable and slips under resistance (the audience convinces itself).

## Keeping attention

Novelty holds attention only briefly — new-and-exciting eventually causes **burnout** (the art-museum effect). What actually sustains attention is a **narrative question about something we care about**, punctuated by **rest** and a **change of pace or scenery**. Escalate, then breathe.

## The power of suggestion (gestalt)

The director's greatest ally is the audience's own mind. **Gestalt** perception organizes experience into wholes greater than the sum of the parts, and — crucially — **the mind fills in the blanks** (we complete "Shave and a haircut…", we read "The Mind F lls in the Bl nks" without stumbling). Suggestion exploits this:

- **Suggest, don't show all.** A dark cave the audience can't see into holds *every* fear at once; reveal the bats and the arachnophobe relaxes. Their imagination is more frightening — and more personal — than any reveal.
- **It is also an economy.** You don't need crowds of thousands when the mind supplies them; *Bambi*'s vast forest is ~98% intimate close-ups, the rest built in the viewer's head. Sound suggests as powerfully (three chords for "man" in *Bambi*; helicopters implied by flashing lights and rotor noise in *Do the Right Thing*).
- A single **symbol** can say more than words (the quarter on the hatcheck plate out-earns the dime).

## Studio application

- **This chapter *is* the Director seat's charter.** "Capture attention, then protect it" is the remit of the [`Director`](../../../sequitur/crew/director.py) reconciler: every department's grammar proposal is judged by whether it points the eye at the one thing that matters this beat and hides the apparatus. It grounds the Director `PersonaJudgment` (the **B** tier) — the persona whose whole job is guarding the viewer's attention ([storyline 0014](../../../context/storyline/0014-the-crew-behaviour.md)).
- **"One idea at a time" is a hard constraint on shot composition.** The speaking metaphor gates what a [`Shot`](../../../sequitur/shot.py) may carry — contrast, motion, brightness, and pointing are exactly the [camera](../../../sequitur/crew/camera.py) choices that make a single subject read. When the [`prompt`](../../../sequitur/prompt.py) builder assembles a shot, "does this frame say *one* clear thing?" is the acceptance test.
- **"Suggest, don't show all" is a rendering-economy directive.** Withholding — a threat implied by sound and shadow rather than shown — is both a suggestion tactic and a budget one; it tells the [image](../../../sequitur/image.py) and [speech](../../../sequitur/speech.py) backends to *imply* rather than fully render, and it is the plan-phase intent the [Editor](../../../sequitur/crew/editorial.py) honours by cutting away before the reveal.
- **"Narrative question → delayed answer" is the shared spine with Ch. 5.** The withholding schedule the Director sets here is what the [`Sequence`](../../../sequitur/edit.py) executes as reveal timing — attention management at the macro level, cut timing at the micro level.

Next: [Ch. 12 — The BIG Picture: Story Structures](ch12-story-structures.md) — from the shot-by-shot management of attention up to the macro shapes that give a whole film its skeleton.
