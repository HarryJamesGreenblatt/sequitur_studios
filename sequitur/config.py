"""Configuration and secrets loading for Sequitur Studios.

Credentials are **provider-keyed**: each renderer pulls only its own backend's
settings, and none of them knows about the others. Secrets are never stored in
plaintext — they live in **Azure Key Vault** and are fetched at runtime via
``DefaultAzureCredential`` (the ``az login`` identity authorises the vault read).
Only non-secret pointers (vault name, endpoint, deployment) live in ``.env``; an
explicit env var can still override a secret for CI or offline use.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"

# Load .env from the project root if present. Only non-secret pointers live here.
load_dotenv(ROOT / ".env")

KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")


def _key_vault_url() -> str:
    """Resolve the vault URL from the environment (no tenant value in code)."""
    url = os.environ.get("KEY_VAULT_URL")
    if url:
        return url
    name = os.environ.get("KEY_VAULT_NAME")
    if not name:
        raise RuntimeError(
            "No Key Vault configured. Set KEY_VAULT_NAME (or KEY_VAULT_URL) in "
            ".env to the vault holding the backend API keys."
        )
    return f"https://{name}.vault.azure.net/"


@lru_cache(maxsize=1)
def _secret_client():
    """Return a cached Key Vault client authenticated with the local identity."""
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    return SecretClient(vault_url=_key_vault_url(), credential=DefaultAzureCredential())


@lru_cache(maxsize=None)
def _get_secret(name: str) -> str:
    """Fetch a secret value from Key Vault (cached for the process lifetime)."""
    return _secret_client().get_secret(name).value


def get_api_key() -> str:
    """Return the Gemini API key: an explicit env override, else Key Vault."""
    override = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if override and override != "your-key-here":
        return override
    try:
        return _get_secret(os.environ.get("GEMINI_KEY_SECRET", "gemini-api-key"))
    except Exception as exc:  # noqa: BLE001 - surface a single actionable message
        vault = os.environ.get("KEY_VAULT_NAME", "the configured")
        raise RuntimeError(
            "No Gemini API key available. Ensure you are logged in "
            f"(`az login`) and the '{vault}' vault holds a "
            "'gemini-api-key' secret, or set GEMINI_API_KEY to override."
        ) from exc


@dataclass(frozen=True)
class AzureImageConfig:
    """Settings for the Azure Foundry image backend (``gpt-image``)."""

    endpoint: str
    deployment: str
    api_version: str
    api_key: str | None  # None => authenticate with Entra ID (DefaultAzureCredential)


def get_azure_image_config() -> AzureImageConfig:
    """Return Azure Foundry image settings, or fail loudly.

    Only the endpoint (non-secret) is required in ``.env``. The API key is
    fetched from Key Vault (secret ``azure-openai-image-key``); set
    ``AZURE_OPENAI_IMAGE_KEY`` to override it for CI or offline use.
    """
    endpoint = os.environ.get("AZURE_OPENAI_IMAGE_ENDPOINT")
    if not endpoint:
        raise RuntimeError(
            "No Azure image endpoint found. Set AZURE_OPENAI_IMAGE_ENDPOINT in "
            ".env to your Foundry account endpoint (e.g. "
            "https://<account>.openai.azure.com/)."
        )
    api_key = os.environ.get("AZURE_OPENAI_IMAGE_KEY")
    if not api_key:
        api_key = _get_secret(
            os.environ.get("AZURE_IMAGE_KEY_SECRET", "azure-openai-image-key")
        )
    return AzureImageConfig(
        endpoint=endpoint,
        deployment=os.environ.get("AZURE_OPENAI_IMAGE_DEPLOYMENT", "gpt-image-1"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
        api_key=api_key,
    )


# A reliable multilingual neural voice available in the eastus2 region. HD voices
# (e.g. ``en-US-Ava:DragonHDLatestNeural``) can be selected per render.
DEFAULT_SPEECH_VOICE = "en-US-AvaMultilingualNeural"


@dataclass(frozen=True)
class AzureSpeechConfig:
    """Settings for the Azure AI Speech backend (text-to-speech).

    Speech rides the *same* AIServices account as the image backend
    — no new resource, no deployment for standard/HD
    neural voices. ``key`` is that account's key (reused from Key Vault); when it
    is ``None`` the renderer authenticates with Entra ID, which needs the account's
    ARM ``resource_id`` for the Speech SDK's ``aad#…`` token form.
    """

    region: str
    voice: str
    key: str | None
    resource_id: str | None


def get_azure_speech_config() -> AzureSpeechConfig:
    """Return Azure Speech settings, reusing the shared AIServices account.

    Only the non-secret region (default ``eastus2``) is needed in ``.env``. The
    key is the shared account key fetched from Key Vault (secret
    ``azure-openai-image-key`` — the *same* account hosts Speech and gpt-image);
    set ``AZURE_SPEECH_KEY`` to override for CI or offline use. With no key, set
    ``AZURE_SPEECH_RESOURCE_ID`` to authenticate via Entra ID.
    """
    key = os.environ.get("AZURE_SPEECH_KEY")
    if not key:
        try:
            key = _get_secret(
                os.environ.get("AZURE_IMAGE_KEY_SECRET", "azure-openai-image-key")
            )
        except Exception:  # noqa: BLE001 - fall through to Entra auth in the renderer
            key = None
    return AzureSpeechConfig(
        region=os.environ.get("AZURE_SPEECH_REGION", "eastus2"),
        voice=os.environ.get("AZURE_SPEECH_VOICE", DEFAULT_SPEECH_VOICE),
        key=key,
        resource_id=os.environ.get("AZURE_SPEECH_RESOURCE_ID"),
    )


# The public, first-party Azure DevOps AAD application id — the token *audience*
# for the ADO REST API. It is the same for every organisation (a documented
# constant, not a tenant secret), so it is a safe default in code.
ADO_RESOURCE_ID = "499b84ac-1321-427f-aa17-267ca6975798"


@dataclass(frozen=True)
class AzureDevOpsConfig:
    """Settings for the production board backend (Azure DevOps).

    All non-secret: the board is authorised by the caller's Entra identity
    (``DefaultAzureCredential``), so there is no key. ``org_url`` is the studio
    **org** (a studio-wide constant); ``project`` is the selected **Production**
    instance (one ADO project = one Production) — per-production, defaulting to the
    ``ADO_PROJECT`` pointer in ``.env``. Both are tenant-specific infrastructure
    names and live only in ``.env`` (never in shipped code); ``resource_id`` is the
    public ADO app constant.
    """

    org_url: str
    project: str
    resource_id: str = ADO_RESOURCE_ID


def get_ado_config(project: str | None = None) -> AzureDevOpsConfig:
    """Return the production-board settings, or fail loudly.

    ``project`` selects which **Production** to work on (one ADO project = one
    Production instance); when omitted it falls back to the ``ADO_PROJECT`` pointer
    in ``.env`` — the *default active production*. ``ADO_ORG_URL`` (the studio org)
    is a studio-wide constant, not per-production, and always comes from ``.env``.
    """
    org_url = os.environ.get("ADO_ORG_URL")
    project = project or os.environ.get("ADO_PROJECT")
    if not org_url or not project:
        raise RuntimeError(
            "No production board configured. Set ADO_ORG_URL "
            "(https://dev.azure.com/<org>) and ADO_PROJECT in .env, "
            "or pass an explicit project."
        )
    return AzureDevOpsConfig(
        org_url=org_url.rstrip("/"),
        project=project,
        resource_id=os.environ.get("ADO_RESOURCE_ID", ADO_RESOURCE_ID),
    )


def get_output_store_root() -> Path:
    """Return the durable output-store root, or fail loudly.

    ``OUTPUT_STORE_ROOT`` (in ``.env``) points at a OneDrive-synced folder in the
    tenant, so artifacts filed there inherit SharePoint/OneDrive durability for free
    (storyline 0005). It is tenant-specific infrastructure — it lives only in
    ``.env``, never in shipped code.
    """
    root = os.environ.get("OUTPUT_STORE_ROOT")
    if not root:
        raise RuntimeError(
            "No output store configured. Set OUTPUT_STORE_ROOT in .env to a "
            "durable folder (e.g. a OneDrive-synced path) for rendered artifacts."
        )
    return Path(root)


def store_url(path: str | Path) -> str | None:
    """Map a local store path to its shareable **https** URL, or ``None`` if unavailable.

    ``OUTPUT_STORE_ROOT`` is the local (OneDrive-synced) root; the non-secret
    ``OUTPUT_STORE_URL_BASE`` (``.env``) is the SharePoint https URL exposing that same
    root. The path's location *under* the root is URL-encoded and appended, so a filed
    artifact carries a real clickable link instead of a local filepath string. Returns
    ``None`` when the base is unset or the path lies outside the store root.
    """
    from urllib.parse import quote

    base = os.environ.get("OUTPUT_STORE_URL_BASE")
    if not base:
        return None
    try:
        rel = Path(path).resolve().relative_to(get_output_store_root().resolve())
    except (ValueError, RuntimeError):
        return None
    return base.rstrip("/") + "/" + "/".join(quote(part) for part in rel.parts)


@dataclass(frozen=True)
class GraphStoreConfig:
    """Settings for the Microsoft Graph (SharePoint/OneDrive) output store.

    All non-secret: uploads are authorised by the caller's Entra identity
    (``DefaultAzureCredential`` on the Graph scope), so there is no key.
    ``drive_id`` is the target document-library **drive** (the SharePoint site's
    library that backs the same tenant location as ``OUTPUT_STORE_ROOT``);
    ``root_path`` is the folder *within* that drive under which productions are
    filed (empty = the drive root). Both are tenant-specific infrastructure names
    and live only in ``.env``, never in shipped code.
    """

    drive_id: str
    root_path: str = ""


def get_graph_store_config() -> GraphStoreConfig:
    """Return the Graph output-store settings, or fail loudly.

    ``GRAPH_DRIVE_ID`` (in ``.env``) identifies the SharePoint document-library drive
    to upload into; the optional ``GRAPH_STORE_ROOT_PATH`` names a folder within it
    (default: the drive root). Both are tenant-specific and live only in ``.env``.
    """
    drive_id = os.environ.get("GRAPH_DRIVE_ID")
    if not drive_id:
        raise RuntimeError(
            "No Graph output store configured. Set GRAPH_DRIVE_ID in .env to the "
            "SharePoint document-library drive id for durable artifact uploads "
            "(and optionally GRAPH_STORE_ROOT_PATH for a subfolder)."
        )
    return GraphStoreConfig(
        drive_id=drive_id,
        root_path=os.environ.get("GRAPH_STORE_ROOT_PATH", "").strip("/"),
    )


def get_output_store():
    """Return the configured :class:`~sequitur.output.OutputStore` backend.

    ``OUTPUT_STORE_BACKEND`` (in ``.env``) selects the data plane: ``graph`` uses the
    Microsoft Graph store (uploads return authoritative SharePoint **share URLs** —
    storyline 0053/0058), anything else (default) the local OneDrive-synced folder. The
    backend is built lazily so import stays credential-free.
    """
    backend = os.environ.get("OUTPUT_STORE_BACKEND", "local").strip().lower()
    if backend == "graph":
        from .output import GraphOutputStore

        return GraphOutputStore()
    from .output import LocalFolderOutputStore

    return LocalFolderOutputStore()
