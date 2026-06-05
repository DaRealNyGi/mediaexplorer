from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from mediaexplorer import paths, ytdlp


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


def test_is_playlist_info_recognizes_playlist() -> None:
    assert ytdlp.is_playlist_info({"_type": "playlist", "entries": [{"id": "abc"}]}) is True


def test_is_playlist_info_rejects_single_video() -> None:
    assert ytdlp.is_playlist_info({"_type": "video", "id": "abc", "title": "Example"}) is False


def test_is_playlist_info_uses_entries_when_type_missing() -> None:
    assert ytdlp.is_playlist_info({"entries": [{"id": "abc"}]}) is True
    assert ytdlp.is_playlist_info({"entries": []}) is False
    assert ytdlp.is_playlist_info({}) is False


def test_base_download_options_suppress_ytdlp_progress_by_default() -> None:
    def hook(_status: dict) -> None:
        return None

    options = ytdlp.base_download_options(hook)

    assert options.get("noprogress") is True
    assert options.get("progress_hooks") == [hook]


def test_base_download_options_can_enable_ytdlp_progress() -> None:
    def hook(_status: dict) -> None:
        return None

    options = ytdlp.base_download_options(hook, ytdlp_progress=True)

    assert "noprogress" not in options
    assert options.get("progress_hooks") == [hook]


def test_parse_ytdlp_config_reads_remote_components() -> None:
    options = ytdlp.parse_ytdlp_config_text("--remote-components ejs:github\n")

    assert options == {"remote_components": ["ejs:github"]}


def test_parse_ytdlp_config_reads_output_template() -> None:
    options = ytdlp.parse_ytdlp_config_text("-o downloads/%(title)s.%(ext)s\n")

    assert options == {"outtmpl": "downloads/%(title)s.%(ext)s"}


def test_parse_ytdlp_config_ignores_blank_and_comment_lines() -> None:
    text = """
    # comment
    --remote-components ejs:github

    -o downloads/%(title)s.%(ext)s
    """
    options = ytdlp.parse_ytdlp_config_text(text)

    assert options == {
        "remote_components": ["ejs:github"],
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }


def test_readonly_options_include_remote_components_from_config(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "yt-dlp.conf"
    config_path.write_text("--remote-components ejs:github\n", encoding="utf-8")
    bundled = tmp_path / "ffmpeg"

    with (
        patch.object(paths, "CONFIG_YTDLP_FILE", config_path),
        patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled),
    ):
        options = ytdlp.readonly_options()

    assert options["remote_components"] == ["ejs:github"]


def test_merge_ytdlp_options_explicit_outtmpl_beats_config(tmp_path: Path) -> None:
    config_path = tmp_path / "yt-dlp.conf"
    config_path.write_text(
        "-o downloads/%(title)s.%(ext)s\n",
        encoding="utf-8",
    )

    options = ytdlp.merge_ytdlp_options(
        {"outtmpl": "defaults/%(title)s.%(ext)s"},
        config_path=config_path,
        overrides={"outtmpl": "explicit/%(title)s.%(ext)s"},
    )

    assert options["outtmpl"] == "explicit/%(title)s.%(ext)s"


@pytest.mark.parametrize(
    "builder",
    [
        pytest.param(lambda: ytdlp.readonly_options(), id="readonly"),
        pytest.param(
            lambda: ytdlp.base_download_options(None),
            id="base_download",
        ),
    ],
)
def test_option_builders_include_remote_components_from_repo_config(
    builder,
    tmp_path: Path,
) -> None:
    bundled = tmp_path / "ffmpeg"

    with patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled):
        options = builder()

    assert "remote_components" in options
    assert "ejs:github" in options["remote_components"]


def test_video_format_selector_default() -> None:
    assert ytdlp.video_format_selector() == "bv*+ba/b"
    assert ytdlp.video_format_selector(compatible=False) == "bv*+ba/b"


def test_video_format_selector_compatible() -> None:
    assert (
        ytdlp.video_format_selector(compatible=True)
        == "bv*[vcodec*=avc1]+ba[acodec*=mp4a]/b[ext=mp4]/best"
    )


def test_video_download_options_default_format() -> None:
    def hook(_status: dict) -> None:
        return None

    options = ytdlp.video_download_options(hook)

    assert options["format"] == "bv*+ba/b"
    assert options["merge_output_format"] == "mp4"


def test_video_download_options_compatible_format() -> None:
    def hook(_status: dict) -> None:
        return None

    options = ytdlp.video_download_options(hook, compatible=True)

    assert (
        options["format"]
        == "bv*[vcodec*=avc1]+ba[acodec*=mp4a]/b[ext=mp4]/best"
    )
    assert options["merge_output_format"] == "mp4"


def test_video_download_options_compatible_uses_ffmpeg_resolution(tmp_path: Path) -> None:
    bundled = tmp_path / "ffmpeg"
    bundled.write_text("", encoding="utf-8")
    bin_dir = tmp_path / "bin"

    def hook(_status: dict) -> None:
        return None

    with (
        patch.object(ytdlp, "BUNDLED_FFMPEG_EXE", bundled),
        patch.object(ytdlp, "FFMPEG_BIN_DIR", bin_dir),
    ):
        options = ytdlp.video_download_options(hook, compatible=True)

    assert options["ffmpeg_location"] == str(bin_dir)
