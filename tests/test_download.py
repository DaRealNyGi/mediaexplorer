from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import download  # noqa: E402


def test_parse_args_default_compatible_false(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["download.py", "https://example.com/watch"])
    args = download.parse_args()

    assert args.url == "https://example.com/watch"
    assert args.compatible is False


def test_parse_args_compatible_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["download.py", "https://example.com/watch", "--compatible"],
    )
    args = download.parse_args()

    assert args.url == "https://example.com/watch"
    assert args.compatible is True
