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
caller hard-wiring a concrete class. Producers (0 media in -> 1 out) live on that
plane, keyed by the :class:`Medium` they create. A second plane holds **operators**
(:class:`Transform`) — medium-preserving decorators over a producer's output (1
media in -> 1 out), keyed by :class:`Operation` — because a transform like a colour
grade preserves its input's medium and so cannot be keyed by an output artifact
kind (storyline 0022). Factories are lazy on both planes, so importing the package
never constructs an API client or requires credentials.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Callable, NamedTuple, Protocol, runtime_checkable


class Medium(Enum):
    """The kind of artifact a renderer produces — the producer-registry key."""

    VIDEO = "video"  # Studio — Gemini Omni Flash
    STILL = "still"  # ImageStudio — Azure Foundry gpt-image
    VOICE = "voice"  # SpeechRenderer — Azure AI Speech
    FILM = "film"  # Cutter — an assembled edit (a reducer: n clips -> one film)


class Operation(Enum):
    """A medium-preserving transform over an existing artifact — the operator key.

    Distinct from :class:`Medium`, which names what a *producer* creates. An
    operation is a *verb*: it decorates a producer's output (1 media in -> 1 out,
    same medium), so it is keyed by what it *does*, not by an artifact kind
    (storyline 0022).
    """

    GRADE = "grade"  # Grader — a colour grade over a rendered clip or still


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
    """The producer contract: a decision in, a new media artifact out (0 media in)."""

    medium: Medium

    def render(
        self, decision, *, out_path: str | Path | None = None
    ) -> RenderResult: ...


@runtime_checkable
class Transform(Protocol):
    """The operator contract: an existing artifact + a decision -> the same medium.

    Unlike a :class:`Renderer` (0 media in -> 1 out, keyed by the :class:`Medium`
    it *produces*), a Transform consumes one already-rendered ``artifact`` and
    returns an artifact of the *same* medium — a Decorator over a producer's output
    (Nystrom's decorated-service refinement of the Service Locator; storyline 0022).
    Taking the input media as an explicit argument makes the 1-media dependency
    visible in the signature rather than hiding it inside the decision.
    """

    operation: Operation

    def apply(
        self, artifact, decision, *, out_path: str | Path | None = None
    ) -> RenderResult: ...


_FACTORIES: dict[Medium, Callable[[], Renderer]] = {}
_OPERATORS: dict[Operation, Callable[[], Transform]] = {}


def register(medium: Medium, factory: Callable[[], Renderer]) -> None:
    """Bind a ``medium`` to a zero-arg ``factory`` that builds its producer."""
    _FACTORIES[medium] = factory


def renderer_for(medium: Medium) -> Renderer:
    """Build the producer registered for ``medium``.

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
    """The media that currently have a producer registered."""
    return tuple(_FACTORIES)


def register_operator(operation: Operation, factory: Callable[[], Transform]) -> None:
    """Bind an ``operation`` to a zero-arg ``factory`` that builds its transform."""
    _OPERATORS[operation] = factory


def operator_for(operation: Operation) -> Transform:
    """Build the transform registered for ``operation`` (lazily, like producers)."""
    try:
        factory = _OPERATORS[operation]
    except KeyError:
        raise LookupError(
            f"No transform registered for operation {operation.value!r}."
        ) from None
    return factory()


def registered_operations() -> tuple[Operation, ...]:
    """The operations that currently have a transform registered."""
    return tuple(_OPERATORS)


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

    def grade() -> Transform:
        from .grader import Grader

        return Grader()

    register(Medium.VIDEO, video)
    register(Medium.STILL, still)
    register(Medium.VOICE, voice)
    register(Medium.FILM, film)
    register_operator(Operation.GRADE, grade)


_register_defaults()
