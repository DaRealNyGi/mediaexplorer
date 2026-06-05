from __future__ import annotations

import shlex
from collections.abc import Callable
from pathlib import Path
from typing import Any

from mediaexplorer import paths as media_paths
from mediaexplorer.paths import BUNDLED_FFMPEG_EXE, DOWNLOADS_DIR

try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError
except ImportError:  # pragma: no cover - exercised only when dependency is missing
    YoutubeDL = None  # type: ignore[assignment]
    DownloadError = Exception  # type: ignore[assignment,misc]


def ytdlp_available() -> bool:
    return YoutubeDL is not None


def missing_ytdlp_message() -> str:
    return "Error: yt-dlp is not installed. Run uv sync and try again."


def bundled_ffmpeg_options() -> dict[str, Any]:
    if BUNDLED_FFMPEG_EXE.exists():
        return {"ffmpeg_location": str(BUNDLED_FFMPEG_EXE)}
    return {}


def parse_ytdlp_config_text(text: str) -> dict[str, Any]:
    options: dict[str, Any] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = shlex.split(line, comments=False)
        if not parts:
            continue

        flag = parts[0]
        if flag == "--remote-components" and len(parts) >= 2:
            components = options.setdefault("remote_components", [])
            if not isinstance(components, list):
                components = []
                options["remote_components"] = components
            components.append(parts[1])
        elif flag in ("-o", "--output") and len(parts) >= 2:
            options["outtmpl"] = parts[1]

    return options


def load_ytdlp_config_options(config_path: Path | None = None) -> dict[str, Any]:
    path = media_paths.CONFIG_YTDLP_FILE if config_path is None else config_path
    if not path.is_file():
        return {}

    return parse_ytdlp_config_text(path.read_text(encoding="utf-8"))


def merge_ytdlp_options(
    base: dict[str, Any],
    *,
    config_path: Path | None = None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    options = dict(base)
    options.update(load_ytdlp_config_options(config_path))
    if overrides:
        options.update(overrides)
    return options


def readonly_options() -> dict[str, Any]:
    return merge_ytdlp_options(
        {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        },
        overrides=bundled_ffmpeg_options(),
    )


def playlist_options() -> dict[str, Any]:
    options = readonly_options()
    options.update(
        {
            "extract_flat": True,
            "ignoreerrors": True,
        },
    )
    return options


def is_playlist_info(info: dict[str, Any]) -> bool:
    info_type = info.get("_type")
    if info_type == "playlist":
        return True
    if info_type == "video":
        return False

    entries = info.get("entries")
    return isinstance(entries, list) and bool(entries)


def base_download_options(
    progress_hook: Callable[[dict[str, Any]], None] | None = None,
    *,
    ytdlp_progress: bool = False,
) -> dict[str, Any]:
    overrides: dict[str, Any] = {
        "noplaylist": True,
        "continuedl": True,
        "retries": 3,
        **bundled_ffmpeg_options(),
    }

    if progress_hook is not None:
        overrides["progress_hooks"] = [progress_hook]

    if not ytdlp_progress:
        overrides["noprogress"] = True

    return merge_ytdlp_options(
        {
            "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        },
        overrides=overrides,
    )


def video_format_selector(*, compatible: bool = False) -> str:
    if compatible:
        return "bv*[vcodec*=avc1]+ba[acodec*=mp4a]/b[ext=mp4]/best"
    return "bv*+ba/b"


def video_download_options(
    progress_hook: Callable[[dict[str, Any]], None],
    *,
    compatible: bool = False,
) -> dict[str, Any]:
    options = base_download_options(progress_hook)
    options.update(
        {
            "format": video_format_selector(compatible=compatible),
            "merge_output_format": "mp4",
        },
    )
    return options


def audio_extract_options(
    progress_hook: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    options = base_download_options(progress_hook)
    options.update(
        {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
            ],
        },
    )
    return options
