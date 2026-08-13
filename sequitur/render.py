"""The renderer seam — the studio's execution plane, formalized.

The grammar (crew roles + enums) is the studio's **decision** plane: it chooses
what a shot, an edit, or a line of dialogue should be. A **renderer** is the
swappable **execution** plane thing that turns one of those decisions into a media
artifact. Storyline 0006 named this seam but deferred a formal contract until a
third backend existed to justify it; four now do — video, still, voice, and the
edit executor — so this module makes the contract explicit.

Every renderer:

* declares the :class:`Medium` it produces, and
* exposes ``render(decision, *, out_path=None) -> RenderResult`` — turning a
  medium-specific *decision* (a :class:`~sequitur.shot.Shot`, a line of text, a
  :class:`~sequitur.edit.Sequence`) into ``(raw, ref)``: the backend's native
  result object and a ``ref`` locating the saved bytes (a local ``Path`` today; a
  URL once outputs live in a blob / SharePoint store — storyline 0005).

A medium-keyed registry lets a role *hold* a renderer **by medium** instead of the
caller hard-wiring a concrete class — the seam the coming Colorist / grade renderer
plugs into. Factories are lazy, so importing the package never constructs an API
client or requires credentials.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Callable, NamedTuple, Protocol, runtime_checkable


class Medium(Enum):
    """The kind of artifact a renderer produces — the registry key."""

    VIDEO = "video"  # Studio — Gemini Omni Flash
    STILL = "still"  # ImageStudio — Azure Foundry gpt-image
    VOICE = "voice"  # SpeechRenderer — Azure AI Speech
    FILM = "film"  # Cutter — an assembled edit (a transform renderer)


class RenderResult(NamedTuple):
    """A render's outcome: the backend-native ``raw`` result + a ``ref`` to bytes.

    It is a plain 2-tuple, so legacy ``raw, ref = renderer.render(...)`` unpacking
    keeps working; the named fields simply document the seam. ``ref`` locates the
    saved artifact — a local :class:`~pathlib.Path` now, a URL later.
    """

    raw: object
    ref: Path | str


@runtime_checkable
class Renderer(Protocol):
    """The execution-plane contract: a decision in, a media artifact out."""

    medium: Medium

    def render(
        self, decision, *, out_path: str | Path | None = None
    ) -> RenderResult: ...


_FACTORIES: dict[Medium, Callable[[], Renderer]] = {}


def register(medium: Medium, factory: Callable[[], Renderer]) -> None:
    """Bind a ``medium`` to a zero-arg ``factory`` that builds its renderer."""
    _FACTORIES[medium] = factory


def renderer_for(medium: Medium) -> Renderer:
    """Build the renderer registered for ``medium``.

    Construction is deferred to call time, so a role can ask for a renderer by
    medium and only pay the API-client / credential cost when it actually renders.
    """
    try:
        factory = _FACTORIES[medium]
    except KeyError:
        raise LookupError(
            f"No renderer registered for medium {medium.value!r}."
        ) from None
    return factory()


def registered_media() -> tuple[Medium, ...]:
    """The media that currently have a renderer registered."""
    return tuple(_FACTORIES)


def _register_defaults() -> None:
    """Register the built-in backends behind lazy imports — no import cycle, and
    no heavy dependency is pulled until a render of that medium is requested."""

    def video() -> Renderer:
        from .studio import Studio

        return Studio()

    def still() -> Renderer:
        from .image import ImageStudio

        return ImageStudio()

    def voice() -> Renderer:
        from .speech import SpeechRenderer

        return SpeechRenderer()

    def film() -> Renderer:
        from .cutter import Cutter

        return Cutter()

    register(Medium.VIDEO, video)
    register(Medium.STILL, still)
    register(Medium.VOICE, voice)
    register(Medium.FILM, film)


_register_defaults()
