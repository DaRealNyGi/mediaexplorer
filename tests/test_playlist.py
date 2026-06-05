from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_SCRIPT = PROJECT_ROOT / "scripts" / "playlist.py"


def _load_playlist_module():
    spec = importlib.util.spec_from_file_location("playlist_script", PLAYLIST_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_playlist_script_handles_single_video_url_gracefully(
    capsys: pytest.CaptureFixture[str],
) -> None:
    playlist = _load_playlist_module()
    video_info = {"_type": "video", "id": "abc123", "title": "Example Video"}

    with (
        patch.object(playlist, "ytdlp_available", return_value=True),
        patch.object(
            playlist,
            "CONFIG_PATH",
            PROJECT_ROOT / "config" / "yt-dlp.conf",
        ),
        patch.object(playlist, "YoutubeDL") as youtube_dl_cls,
        patch.object(
            sys,
            "argv",
            ["playlist.py", "https://www.youtube.com/watch?v=abc123"],
        ),
    ):
        youtube_dl_cls.return_value.__enter__.return_value.extract_info.return_value = (
            video_info
        )
        exit_code = playlist.main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "This URL does not appear to be a playlist." in captured.out
    assert "no usable entries" not in captured.err.lower()
