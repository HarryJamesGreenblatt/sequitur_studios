# 0011 — The voice layer: SpeechRenderer, the third render backend

> Date: 2026-08-08 · Focus: **build** the `SpeechRenderer` slice designed in `0009`
> — the studio's first *sound* renderer and third render backend. This is a **code**
> entry (the first since `0006`); it turns the "build `SpeechRenderer` first" open
> thread into working, validated code.

## What happened

Built [`sequitur/speech.py`](../../sequitur/speech.py) — `SpeechRenderer`, a thin
Azure AI Speech text-to-speech client that is a sibling of `Studio` (video) and
`ImageStudio` (still). It synthesizes a line of text (or a full `<speak>` SSML
document, auto-detected) to a WAV and returns `(result, path)`, mirroring the other
backends' shape.

1. **No new Azure resource.** Speech rides the *same* existing
   AIServices account that hosts `gpt-image-1`/`sora`, exactly as `0009` predicted.
   The key insight made concrete: an AIServices multi-service account exposes one key
   across all its APIs, so `SpeechRenderer` **reuses the existing Key Vault secret**
   (the Azure image key) — no new secret, no deployment (standard/HD neural
   voices are call-and-go; only Custom Neural Voice deploys, and it stays deferred).

2. **Config parity.** Added `AzureSpeechConfig` + `get_azure_speech_config()` to
   [`config.py`](../../sequitur/config.py), following the `AzureImageConfig` pattern:
   only the non-secret region (default `eastus2`) lives in `.env`; the key is fetched
   from KV (or `AZURE_SPEECH_KEY` override). Entra-ID auth is supported as the
   keyless path (needs `AZURE_SPEECH_RESOURCE_ID` for the Speech SDK's `aad#…` token
   form on the `cognitiveservices.azure.com/.default` scope).

3. **Grounded output contract.** Per Rose Ch. 9 (VO/ADR craft brief) the renderer
   records **dry and clean** — no EQ/compression/reverb baked in; matching presence
   to a shot is a downstream `SoundMixer`/`ReRecordingMixer` concern. Per Ch. 2/12
   the output format is fixed to **48 kHz / 16-bit / mono PCM** (`Riff48Khz16BitMonoPcm`).

4. **Wired + validated.** Exported `SpeechRenderer` from
   [`__init__.py`](../../sequitur/__init__.py); added
   `azure-cognitiveservices-speech` to `requirements.txt` (installed 1.51.1 into the
   `.venv`). A **live synthesis smoke test** wrote a real WAV and a `wave`-module
   check confirmed the contract exactly: **48000 Hz, 1 channel, 16-bit**. Scratch
   file removed; `output/` stays gitignored.

## Decisions

1. **Reuse the account key, not a new secret.** Because Speech and gpt-image share
   the AIServices account, "reuse the KV key" (`0009`) means literally the
   existing Azure image-key secret. This keeps the secret inventory at two and needs
   zero Azure changes to bring the voice layer online.

2. **Renderer stays dumb; the craft lift attaches to the role.** `SpeechRenderer`
   is pure execution-plane text→wav. SSML prosody, ADR presence-matching, and
   session-style direction are the `SoundMixer` role's job (crew engine, `0008`) and
   are *not* in this class — consistent with `image.py`/`studio.py` being thin.

3. **Fix the output format at the SDK boundary.** Rather than post-process, set
   `Riff48Khz16BitMonoPcm` on the `SpeechConfig` so every render is delivery-spec by
   construction — the contract is enforced where the bytes are made.

## Resulting state

- **Three render backends over one studio now:** `Studio` (video, Gemini Omni),
  `ImageStudio` (still, Azure gpt-image), **`SpeechRenderer` (voice, Azure Speech)**.
  The renderer seam (`0006`) now has enough members to justify formalizing a
  `Renderer` protocol — the next natural step.
- The `0009` "build `SpeechRenderer` first" thread is **done and validated live**.
- No new resource/secret/deployment; `.env` gains only optional non-secret pointers
  (`AZURE_SPEECH_REGION`, `AZURE_SPEECH_VOICE`, `AZURE_SPEECH_RESOURCE_ID`).

## Open threads

- **Formalize the `Renderer` protocol** (`0006` deferral now expired) — three
  backends share the `render(...) -> (result, path)` shape; lift it into a protocol.
- **Ground the `SoundMixer` role** (needs the crew engine, `0008`) — attach the
  Rose Ch. 9 craft lift (SSML prosody, ADR presence-matching) to the role that
  *wields* `SpeechRenderer`, not the renderer itself.
- **A small smoke test suite** — the live synth check was ad hoc; a `build_prompt`
  smoke test (and an offline `SpeechRenderer` config test) would guard the grammar
  and the config resolution before the crew-engine refactor.
- Carried: crew engine phase A (`0008`); the provider seams (`0005`); the edit post
  layer (`0007`); toaster-strudel MCP client (`0009`); the reconciliation sweeps.
