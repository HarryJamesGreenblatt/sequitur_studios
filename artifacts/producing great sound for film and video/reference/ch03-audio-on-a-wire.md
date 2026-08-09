# Chapter 3 — Audio on a Wire

> Abridged from Jay Rose, *Producing Great Sound for Film and Video* (4th ed.),
> Ch. 3.
> **Scope:** analog voltage standards, balanced vs. unbalanced wiring and ground
> loops, impedance, and the digital-audio connector/format zoo. This is the most
> *hardware*-bound chapter; the studio tie is deliberately thin — it belongs to
> the physical signal chain the code never touches.

## Core idea

Two separate rulebooks. **Analog** wiring works if you respect **voltage and
grounding** (impedance rarely matters). **Digital** wiring is noise-free but is a
very high-frequency signal — treat it like **video**, where **impedance and cable
spec are critical** and there's no graceful degradation (wrong cable = instant
dropout, not gradual hiss).

## Analog: levels and balancing

- **Two level standards** that don't mix cleanly: **pro +4 dBu** (~1.23 V,
  XLR/TRS) and **consumer −10 dBV** (~0.32 V, phono/mini). Cross-connecting needs
  an active interface or transformer, not a passive adapter — consumer→pro sits
  near the noise floor; pro→consumer over-drives the input.
- **Balanced wiring** (two twisted conductors, + and −; XLR pin 2 hot / pin 3
  cold / pin 1 shield) rejects hum by comparing the *difference* between wires, so
  interference picked up equally on both cancels. It's the pro standard and the
  cure for **ground-loop** 50/60 Hz hum. **Star-Quad** cable improves rejection
  further (~$15 upgrade, worth it for mics).

## Digital: the connector map

| Standard | Connector | Impedance | Cable |
|----------|-----------|-----------|-------|
| **AES/EBU** | XLR | 110 Ω | true digital (or Cat-5) — **not** a mic cable |
| **S/PDIF** | phono/BNC | 75 Ω | video coax (RG-59) |
| **Toslink** | optical mini | — | fiber (~50 ft max; immune to ground loops) |
| **MADI** | BNC/fiber | — | up to 64 ch on one cable |
| **Dante** | Ethernet | — | audio-over-IP, up to 1,024 ch |

The recurring trap: **AES/EBU looks like a mic XLR but isn't**, and **S/PDIF
looks like an analog phono but isn't** — the impedance mismatch causes instant
dropouts. Match the cable to the spec.

## Studio application

This chapter grounds *hardware*, so its lead is intentionally light:

- **It marks the boundary of the execution plane.** `SpeechRenderer` and the
  future audio renderers deal in **files and formats**, not wires — the physical
  signal chain (mics, preamps, balancing, digital transport) is upstream of any
  generated production and is never modeled in code. The digital-transport
  discipline (match the interface, no graceful degradation) survives in software
  only as the **format-interchange** rule from ch. 2: pick the right container/rate
  for the target and don't assume a wrong one degrades gracefully.
- **Balanced/ground-loop knowledge stays reference-only** — a fact the
  `SoundMixer` role's *human/persona* judgment can cite when reasoning about a
  captured take's noise, not something the heuristic layer computes.
