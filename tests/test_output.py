"""Smoke tests for the output-store seam — produced bytes -> a durable reference.

Exercises the ``LocalFolderOutputStore`` backend against a temporary root (never the
real OneDrive-synced store), so the data plane (file bytes or a rendered path under a
``production / layer / name`` key) is covered offline. Asserts against the public
package surface. Run directly (``python tests/test_output.py``) or via pytest.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur import LocalFolderOutputStore, OutputStore  # noqa: E402
from sequitur import GraphOutputStore  # noqa: E402


class _StubGraphStore(GraphOutputStore):
    """A GraphOutputStore that records the upload path instead of hitting the network."""

    def __init__(self) -> None:
        super().__init__(drive_id="drive-1", root_path="Sequitur Studios/output")
        self.uploaded: tuple[str, bytes] | None = None
        self.downloaded: str | None = None

    def _upload(self, item_path: str, data: bytes) -> dict:  # type: ignore[override]
        self.uploaded = (item_path, data)
        return {"webUrl": "https://contoso.sharepoint.com/" + item_path}

    def _download(self, share_url: str) -> bytes:  # type: ignore[override]
        self.downloaded = share_url
        return b"resolved-bytes"



def test_backend_satisfies_the_protocol() -> None:
    # runtime_checkable: the concrete backend structurally implements the seam.
    with tempfile.TemporaryDirectory() as d:
        assert isinstance(LocalFolderOutputStore(d), OutputStore)


def test_put_bytes_files_them_under_the_key() -> None:
    with tempfile.TemporaryDirectory() as d:
        store = LocalFolderOutputStore(d)
        ref = store.put(b"poster-bytes", production="HeistNoir", layer="plan", name="poster.png")
        assert Path(ref) == Path(d) / "HeistNoir" / "plan" / "poster.png"
        assert Path(ref).read_bytes() == b"poster-bytes"


def test_put_a_rendered_path_copies_it_in() -> None:
    with tempfile.TemporaryDirectory() as d:
        scratch = Path(d) / "scratch.mp4"
        scratch.write_bytes(b"daily-bytes")
        store = LocalFolderOutputStore(Path(d) / "store")
        ref = store.put(scratch, production="HeistNoir", layer="shoot")
        # Name defaults to the source filename; the scratch source is left intact.
        assert Path(ref) == Path(d) / "store" / "HeistNoir" / "shoot" / "scratch.mp4"
        assert Path(ref).read_bytes() == b"daily-bytes"
        assert scratch.exists()


def test_explicit_name_overrides_the_source_filename() -> None:
    with tempfile.TemporaryDirectory() as d:
        scratch = Path(d) / "scratch.mp4"
        scratch.write_bytes(b"x")
        store = LocalFolderOutputStore(Path(d) / "store")
        ref = store.put(scratch, production="P", layer="shoot", name="shot_001.mp4")
        assert Path(ref).name == "shot_001.mp4"


def test_bytes_without_a_name_is_an_error() -> None:
    with tempfile.TemporaryDirectory() as d:
        store = LocalFolderOutputStore(d)
        try:
            store.put(b"x", production="P", layer="plan")
        except ValueError:
            pass
        else:  # pragma: no cover - the assertion is the failure signal
            raise AssertionError("storing raw bytes without a name should raise")


def test_default_root_reads_the_env_pointer() -> None:
    # Absent an explicit root, the store resolves OUTPUT_STORE_ROOT from the env.
    saved = os.environ.get("OUTPUT_STORE_ROOT")
    with tempfile.TemporaryDirectory() as d:
        try:
            os.environ["OUTPUT_STORE_ROOT"] = d
            assert LocalFolderOutputStore().root == Path(d)
        finally:
            if saved is None:
                os.environ.pop("OUTPUT_STORE_ROOT", None)
            else:
                os.environ["OUTPUT_STORE_ROOT"] = saved


def test_graph_backend_satisfies_the_protocol() -> None:
    # runtime_checkable: the Graph backend structurally implements the same seam.
    # __init__ touches no network, so an explicit drive id constructs offline.
    assert isinstance(GraphOutputStore(drive_id="drive-1", root_path=""), OutputStore)


def test_graph_put_bytes_uploads_under_the_key_and_returns_the_url() -> None:
    store = _StubGraphStore()
    ref = store.put(b"poster-bytes", production="HeistNoir", layer="plan", name="poster.png")
    assert store.uploaded == (
        "Sequitur Studios/output/HeistNoir/plan/poster.png",
        b"poster-bytes",
    )
    # The ref is the authoritative webUrl string, not a local path (0038's "URL later").
    assert ref == "https://contoso.sharepoint.com/Sequitur Studios/output/HeistNoir/plan/poster.png"


def test_graph_put_a_rendered_path_reads_and_uploads_it() -> None:
    with tempfile.TemporaryDirectory() as d:
        scratch = Path(d) / "scratch.mp4"
        scratch.write_bytes(b"daily-bytes")
        store = _StubGraphStore()
        store.put(scratch, production="HeistNoir", layer="shoot")
        assert store.uploaded == (
            "Sequitur Studios/output/HeistNoir/shoot/scratch.mp4",
            b"daily-bytes",
        )
        assert scratch.exists()  # the scratch source is left intact


def test_graph_bytes_without_a_name_is_an_error() -> None:
    store = _StubGraphStore()
    try:
        store.put(b"x", production="P", layer="plan")
    except ValueError:
        pass
    else:  # pragma: no cover - the assertion is the failure signal
        raise AssertionError("storing raw bytes without a name should raise")


def test_local_fetch_reads_the_bytes_back() -> None:
    with tempfile.TemporaryDirectory() as d:
        store = LocalFolderOutputStore(d)
        ref = store.put(b"poster-bytes", production="P", layer="plan", name="poster.png")
        assert store.fetch(ref) == b"poster-bytes"


def test_graph_fetch_resolves_a_share_url_via_the_shares_endpoint() -> None:
    store = _StubGraphStore()
    data = store.fetch("https://contoso.sharepoint.com/x/poster.png")
    assert data == b"resolved-bytes"
    assert store.downloaded == "https://contoso.sharepoint.com/x/poster.png"


def test_graph_fetch_reads_a_local_path_directly() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "ref.png"
        p.write_bytes(b"local-ref")
        assert _StubGraphStore().fetch(p) == b"local-ref"


def test_fetch_reference_reads_a_local_path() -> None:
    from sequitur import fetch_reference

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "ref.png"
        p.write_bytes(b"reference-bytes")
        assert fetch_reference(p) == b"reference-bytes"


def test_fetch_reference_resolves_a_url_through_the_store() -> None:
    # A share-URL reference is resolved to bytes via the store's fetch (fetch-then-condition).
    from sequitur import fetch_reference

    store = _StubGraphStore()
    data = fetch_reference("https://contoso.sharepoint.com/x/ref.png", store=store)
    assert data == b"resolved-bytes"
    assert store.downloaded == "https://contoso.sharepoint.com/x/ref.png"


def test_get_output_store_selects_the_backend() -> None:
    from sequitur.config import get_output_store

    saved = {k: os.environ.get(k) for k in ("OUTPUT_STORE_BACKEND", "OUTPUT_STORE_ROOT", "GRAPH_DRIVE_ID")}
    try:
        with tempfile.TemporaryDirectory() as d:
            os.environ["OUTPUT_STORE_ROOT"] = d
            os.environ.pop("OUTPUT_STORE_BACKEND", None)
            assert isinstance(get_output_store(), LocalFolderOutputStore)  # default
            os.environ["OUTPUT_STORE_BACKEND"] = "graph"
            os.environ["GRAPH_DRIVE_ID"] = "drive-1"
            assert isinstance(get_output_store(), GraphOutputStore)  # opted in
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all output-store tests passed")
