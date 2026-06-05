from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from mediaexplorer import ytdlp


def test_bundled_ffmpeg_options_omitted_when_not_bundled(tmp_path: Path) -> None:
    bundled = tmp_path / "ffmpeg"
    with patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled):
        assert ytdlp.bundled_ffmpeg_options() == {}


def test_bundled_ffmpeg_options_set_when_bundled(tmp_path: Path) -> None:
    bundled = tmp_path / "ffmpeg"
    bundled.write_text("", encoding="utf-8")
    bin_dir = tmp_path / "bin"

    with (
        patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled),
        patch.object(ytdlp, "FFMPEG_BIN_DIR", bin_dir),
    ):
        assert ytdlp.bundled_ffmpeg_options() == {"ffmpeg_location": str(bin_dir)}


def test_readonly_options_skip_ffmpeg_location_without_bundle(tmp_path: Path) -> None:
    bundled = tmp_path / "ffmpeg"
    with patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled):
        options = ytdlp.readonly_options()

    assert "ffmpeg_location" not in options


def test_base_download_options_skip_ffmpeg_location_without_bundle(tmp_path: Path) -> None:
    bundled = tmp_path / "ffmpeg"

    def hook(_status: dict) -> None:
        return None

    with patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled):
        options = ytdlp.base_download_options(hook)

    assert "ffmpeg_location" not in options
