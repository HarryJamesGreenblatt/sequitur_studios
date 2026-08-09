"""The Sequitur Studios speech renderer — a thin, correct wrapper over Azure AI
Speech for turning text into clean, unprocessed voice audio.

This is the third render backend (alongside :class:`~sequitur.studio.Studio` for
video and :class:`~sequitur.image.ImageStudio` for stills) and the first that
produces *sound*. Its two uses, both from the audio brief in storyline 0007/0009,
are **production voice-over/narration** and **ADR/overdub fallback** when a
generated dialogue take is unusable ("keep the diegetic take, or dub it").

The renderer is deliberately dumb. Following the craft brief in Jay Rose,
*Producing Great Sound* (Ch. 9), it records **dry and clean** — no EQ, no
compression, no reverb baked in. Matching a line's *presence* to its shot (mic
distance, room reverb) is a downstream, reversible concern owned by the
``SoundMixer`` / ``ReRecordingMixer`` roles, not this execution-plane renderer.
The output format is fixed to the delivery contract from Ch. 2/12: **48 kHz,
16-bit, mono PCM** in a RIFF/WAV container.

Speech rides the *same* AIServices account as the image backend — there is no new
Azure resource and no deployment for standard/HD neural voices (a deployment
exists only for the Responsible-AI-gated Custom Neural Voice, which is deferred).
"""

from __future__ import annotations

import time
from pathlib import Path

from .config import AzureSpeechConfig, get_azure_speech_config

_AAD_SCOPE = "https://cognitiveservices.azure.com/.default"


class SpeechRenderer:
    """A text-to-speech render session backed by Azure AI Speech.

    render() -> synthesize a line of text (or SSML) to a dry, unprocessed WAV;
    returns (result, path).
    """

    def __init__(self, config: AzureSpeechConfig | None = None) -> None:
        # Imported lazily so the video/image paths and --dry-run need no Speech dep.
        import azure.cognitiveservices.speech as speechsdk

        self._speechsdk = speechsdk
        self.config = config or get_azure_speech_config()

        speech_config = self._authenticate(speechsdk)
        # Rose Ch. 2/12: deliver 48 kHz / 16-bit / mono PCM, dry and unprocessed.
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm
        )
        self._config = speech_config

    def render(
        self,
        text: str,
        *,
        voice: str | None = None,
        out_path: str | Path | None = None,
    ):
        """Synthesize ``text`` to a WAV file. Returns (result, saved_path).

        ``text`` may be plain text or a full ``<speak>`` SSML document (detected
        automatically). Pass ``voice`` to override the configured neural voice —
        including an HD voice such as ``en-US-Ava:DragonHDLatestNeural``.
        """
        speechsdk = self._speechsdk
        self._config.speech_synthesis_voice_name = voice or self.config.voice

        path = Path(out_path) if out_path else self._default_path()
        path.parent.mkdir(parents=True, exist_ok=True)

        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(path))
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self._config, audio_config=audio_config
        )

        is_ssml = text.lstrip().startswith("<speak")
        future = (
            synthesizer.speak_ssml_async(text)
            if is_ssml
            else synthesizer.speak_text_async(text)
        )
        result = future.get()

        if result.reason == speechsdk.ResultReason.Canceled:
            details = result.cancellation_details
            raise RuntimeError(
                f"Speech synthesis canceled: {details.reason} — "
                f"{details.error_details}"
            )
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise RuntimeError(f"Speech synthesis did not complete: {result.reason}")
        return result, path

    # -- internals ---------------------------------------------------------

    def _authenticate(self, speechsdk):
        """Build a SpeechConfig: the shared account key, else Entra ID."""
        if self.config.key:
            return speechsdk.SpeechConfig(
                subscription=self.config.key, region=self.config.region
            )
        if not self.config.resource_id:
            raise RuntimeError(
                "No Speech key available and no AZURE_SPEECH_RESOURCE_ID set for "
                "Entra auth. Ensure you are logged in (`az login`) and the vault "
                "holds the shared account key, or set AZURE_SPEECH_RESOURCE_ID to "
                "the AIServices resource's ARM id."
            )
        from azure.identity import DefaultAzureCredential

        token = DefaultAzureCredential().get_token(_AAD_SCOPE).token
        auth_token = f"aad#{self.config.resource_id}#{token}"
        return speechsdk.SpeechConfig(
            auth_token=auth_token, region=self.config.region
        )

    def _default_path(self) -> Path:
        from .config import OUTPUT_DIR

        return OUTPUT_DIR / f"vo_{int(time.time())}.wav"
