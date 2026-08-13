"""Smoke tests for the renderer seam — the execution-plane protocol + registry.

Asserts against the *public* package surface (``sequitur``). Constructs only the
dependency-free backend (``Cutter``); the API-client backends are checked at the
class level so this test needs no credentials. Run directly
(``python tests/test_render.py``) or via pytest.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import (  # noqa: E402
    Cutter,
    ImageStudio,
    Medium,
    RenderResult,
    Renderer,
    SpeechRenderer,
    Studio,
    register,
    registered_media,
    renderer_for,
)


def test_each_backend_declares_its_medium() -> None:
    assert Studio.medium is Medium.VIDEO
    assert ImageStudio.medium is Medium.STILL
    assert SpeechRenderer.medium is Medium.VOICE
    assert Cutter.medium is Medium.FILM


def test_render_result_is_a_raw_ref_pair() -> None:
    r = RenderResult("native-result", Path("out.mp4"))
    raw, ref = r  # unpacks like the legacy 2-tuple callers still expect
    assert raw == "native-result" and ref == Path("out.mp4")
    assert r.raw == "native-result" and r.ref == Path("out.mp4")


def test_registry_covers_every_medium() -> None:
    assert set(registered_media()) == set(Medium)


def test_renderer_for_builds_and_satisfies_the_protocol() -> None:
    # Cutter needs no API client, so it can be built and structurally checked here.
    cutter = renderer_for(Medium.FILM)
    assert isinstance(cutter, Cutter)
    assert isinstance(cutter, Renderer)  # runtime_checkable structural match


def test_registry_is_overridable() -> None:
    sentinel = object()
    register(Medium.FILM, lambda: sentinel)
    try:
        assert renderer_for(Medium.FILM) is sentinel
    finally:
        register(Medium.FILM, Cutter)  # restore the default factory


def test_unknown_medium_raises() -> None:
    register(Medium.FILM, Cutter)  # ensure a clean baseline
    empty = Medium.FILM
    # A medium with no factory reports clearly.
    from sequitur.render import _FACTORIES

    saved = _FACTORIES.pop(empty)
    try:
        raised = False
        try:
            renderer_for(empty)
        except LookupError:
            raised = True
        assert raised
    finally:
        _FACTORIES[empty] = saved


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
