"""A shared-engine engineering project is not itself a film production."""

import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import urllib.error
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sequitur.production import AzureDevOpsProduction


class _Response(io.BytesIO):
    def __init__(self, value, headers=None):
        super().__init__(json.dumps(value).encode())
        self.headers = headers or {}


def _credential():
    return SimpleNamespace(get_token=lambda scope: SimpleNamespace(token="offline-test"))


def test_catalog_excludes_engine_scrum_and_preserves_production_projects():
    def read(request):
        if "/_apis/projects?" in request.full_url:
            return _Response({"value": [{"id": "engine", "name": "Engine"}, {"id": "film", "name": "Film"}]})
        return _Response({"value": [{"name": "Shot" if "/film/" in request.full_url else "Product Backlog Item"}]})
    with patch("urllib.request.urlopen", side_effect=read):
        assert AzureDevOpsProduction.list_productions(org_url="https://dev.azure.com/example", credential=_credential()) == ["Film"]


def test_catalog_reads_subsequent_project_pages():
    def read(request):
        if "/_apis/projects?" in request.full_url:
            if "continuationToken=" in request.full_url:
                return _Response({"value": [{"id": "second", "name": "Second"}]})
            return _Response({"value": [{"id": "first", "name": "First"}]}, {"x-ms-continuationtoken": "page2"})
        return _Response({"value": [{"name": "Shot"}]})
    with patch("urllib.request.urlopen", side_effect=read):
        assert AzureDevOpsProduction.list_productions(org_url="https://dev.azure.com/example", credential=_credential()) == ["First", "Second"]


def test_catalog_surfaces_access_errors_instead_of_silently_omitting_a_project():
    def read(request):
        if "/_apis/projects?" in request.full_url:
            return _Response({"value": [{"id": "denied", "name": "Denied"}]})
        raise urllib.error.HTTPError(request.full_url, 403, "Forbidden", {}, None)
    with patch("urllib.request.urlopen", side_effect=read):
        try:
            AzureDevOpsProduction.list_productions(org_url="https://dev.azure.com/example", credential=_credential())
        except urllib.error.HTTPError as error:
            assert error.code == 403
        else:
            raise AssertionError("An access failure was hidden")


if __name__ == "__main__":
    for name, run in sorted(list(globals().items())):
        if name.startswith("test_"):
            run()
            print(f"ok {name}")
