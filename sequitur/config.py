"""Configuration and secrets loading for Sequitur Studios."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"

# Load .env from the project root if present. Real keys live here, never in code.
load_dotenv(ROOT / ".env")


def get_api_key() -> str:
    """Return the Gemini API key from the environment, or fail loudly."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key or key == "your-key-here":
        raise RuntimeError(
            "No Gemini API key found. Copy .env.example to .env and set "
            "GEMINI_API_KEY to your Sequitur Studios key."
        )
    return key
