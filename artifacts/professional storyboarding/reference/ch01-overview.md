# Chapter 1 — Overview

> Abridged from Sergio Paez & Anson Jew, *Professional Storyboarding: Rules of Thumb* (Focal Press, 2013), Ch. 1.
> **Scope:** what a storyboard *is* and *does* as a craft artifact — its history, its practical purpose as an "edit on paper," and (briefly) who makes them and how they are employed.

## Core idea

A storyboard is a **pre-visualisation of the finished film drawn cheaply, before anything expensive is committed** — a sequence of panels that hit the major action and story points so the whole team can see the movie *as a whole* before it exists. Its defining virtue is economy: because production (especially animation, effects, and action) is ruinously expensive, cutting or changing a shot *after* it is shot burns money. Storyboarding moves those decisions upstream, letting you edit, reorder, and discard on paper for near-zero cost. That is the entire value proposition — a storyboard is a rough draft of the movie whose job is to fail cheaply so the real production doesn't fail expensively.

Historically this is the leap from *concept sketch* to *storyboard*. Early film shot scenes like filmed theatre — fixed wide, static camera — until a common visual language (cross-cutting, reverse angles, POV, Eisenstein's montage) emerged. Disney's studio formalised the board proper: individual shots drawn on separate cards and pinned up so the director could approve, revise, or cut and see the sequence working as a *whole* rather than as isolated gags. That whole-film view — and the money it saves — is why the practice spread from animation into live action, and now into games, web, and mobile.

## What a board is (and is not)

- **A communication tool, not fine art.** Boards serve a small internal audience — director, DP, actors, effects — for the *duration of a production only*. They are disposable, redrawn and thrown away by the thousand. Read, not polish, is the goal.
- **A whole-film view.** Pinning shots up side by side exposes how a *sequence* reads — pacing, continuity, emotional build — instead of each shot being solved in isolation.
- **An edit before the edit.** Reordering panels is the cheapest possible cut. The board is where the film's structure is stress-tested at the price of a pencil.

## Where boards are used

| Medium | Board usage |
| --- | --- |
| **Animation** | Whole show is boarded; boards drive the entire production. |
| **Live action** | Selective — mainly effects-heavy or action/stunt sequences. |
| **Games / web / mobile** | Growing use for cinematics and interactive sequences. |

## Who draws them (compressed)

Staff vs. freelance, in brief: **staff** boards live mostly in animation TV/features and games (a studio runs many productions at once, so artists move project to project); **freelance** dominates live action, commercials, and advertising (each film is a company that exists only for that shoot, then dissolves). Freelancers charge more per day to offset dry spells and self-funded overhead; staffers trade rate for stability. The business detail matters little to the craft — what matters is that the *board*, not the artist's employment model, is the deliverable.

## Studio application

- **The board is the plan-phase deliverable — decide shots on paper before paying to render.** This chapter's thesis *is* the Sequitur render economy: a paid image/video call is the "expensive shoot," and composing the shot spec first is the cheap edit. It is the exact rationale behind [`--dry-run` prompt composition](../../../sequitur/prompt.py) — assemble and inspect the full prompt from a [`Shot`](../../../sequitur/shot.py) with zero API cost, reorder and revise freely, and only then commit to a render. A storyboard panel is a pre-rendered `Shot`: the point where plan-phase decisions become a concrete visual spec.
- **The board grounds a future Storyboard Artist role in the plan phase.** A storyboard artist's output — a per-shot visual read of the sequence — is precisely a plan-phase [`Contribution`](../../../sequitur/crew/role.py) that would seed the [`Brief`](../../../sequitur/crew/role.py) the [`Director`](../../../sequitur/crew/director.py) reconciles, giving the crew a "whole-film view" to react to before any render call fires (see [the crew behaviour devlog](../../../context/storyline/0014-the-crew-behaviour.md)).
- **Whole-sequence review, not per-shot perfection.** The Disney "pin the cards up" insight maps onto reviewing a whole production's shot list as a unit — catching pacing and continuity problems cheaply — rather than perfecting one keyframe at a time. Cross-links: [Grammar of the Shot Ch. 1 — The Shots](../../grammar%20of%20the%20shot/reference/ch01-the-shots.md).
