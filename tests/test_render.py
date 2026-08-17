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


def test_image_studio_conditions_a_still_on_reference_images() -> None:
    # References route to the gpt-image EDITS endpoint (the casting-consistency lock,
    # storyline 0055); without them the render takes the plain generation path. An
    # injected client keeps this offline — no endpoint, credential, or network.
    import base64
    import tempfile
    import types

    def _result():
        b64 = base64.b64encode(b"img-bytes").decode()
        return types.SimpleNamespace(data=[types.SimpleNamespace(b64_json=b64)])

    recorded: dict = {}

    class _Images:
        def generate(self, **kw):
            recorded["generate"] = kw
            return _result()

        def edit(self, **kw):
            recorded["edit"] = {**kw, "image_names": [f.name for f in kw["image"]]}
            return _result()

    class _Client:
        images = _Images()

    cfg = types.SimpleNamespace(deployment="gpt-image-1")
    studio = ImageStudio(cfg, client=_Client())

    with tempfile.TemporaryDirectory() as d:
        ref = Path(d) / "nora-locked.png"
        ref.write_bytes(b"reference-bytes")

        conditioned = Path(d) / "scene.png"
        result = studio.render(
            "Nora on the platform at dusk", references=[ref], out_path=conditioned
        )
        # Routed to edit, conditioned on the locked reference — not generate.
        assert "edit" in recorded and "generate" not in recorded
        assert recorded["edit"]["image_names"] == [str(ref)]
        assert result.ref == conditioned and conditioned.read_bytes()

        recorded.clear()
        plain = Path(d) / "plain.png"
        studio.render("a lighthouse in a storm", out_path=plain)
        # No references -> the plain generation path.
        assert "generate" in recorded and "edit" not in recorded


def test_image_studio_derives_references_from_a_shots_cast() -> None:
    # A Shot carrying a cast Character with a locked reference conditions the render
    # automatically — the backend owns its conditioning (storyline 0057), no explicit
    # references argument needed.
    import base64
    import tempfile
    import types

    from sequitur import Actor, Character, Shot

    def _result():
        b64 = base64.b64encode(b"img-bytes").decode()
        return types.SimpleNamespace(data=[types.SimpleNamespace(b64_json=b64)])

    recorded: dict = {}

    class _Images:
        def generate(self, **kw):
            recorded["generate"] = kw
            return _result()

        def edit(self, **kw):
            recorded["edit"] = {**kw, "image_names": [f.name for f in kw["image"]]}
            return _result()

    class _Client:
        images = _Images()

    cfg = types.SimpleNamespace(deployment="gpt-image-1")
    studio = ImageStudio(cfg, client=_Client())

    with tempfile.TemporaryDirectory() as d:
        ref = Path(d) / "nora-locked.png"
        ref.write_bytes(b"reference-bytes")
        nora = Character(name="Nora", candidates=[Actor(look="weathered", reference=str(ref))])
        nora.select(nora.candidates[0])
        shot = Shot(scene="a platform at dusk", cast=[nora])

        out = Path(d) / "scene.png"
        studio.render(shot, out_path=out)
        # The shot's locked cast reference conditioned the render via the edit endpoint.
        assert "edit" in recorded and recorded["edit"]["image_names"] == [str(ref)]
        assert out.read_bytes()


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
