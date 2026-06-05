from __future__ import annotations

from collections.abc import Callable
from typing import Any

from mediaexplorer.paths import BUNDLED_FFMPEG_EXE, DOWNLOADS_DIR, FFMPEG_BIN_DIR

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
        return {"ffmpeg_location": str(FFMPEG_BIN_DIR)}
    return {}


def readonly_options() -> dict[str, Any]:
    return {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        **bundled_ffmpeg_options(),
    }


def playlist_options() -> dict[str, Any]:
    options = readonly_options()
    options.update(
        {
            "extract_flat": True,
            "ignoreerrors": True,
        },
    )
    return options


def base_download_options(
    progress_hook: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    return {
        "outtmpl": str(DOWNLOADS_DIR / "%(title)s.%(ext)s"),
        **bundled_ffmpeg_options(),
        "progress_hooks": [progress_hook],
        "noplaylist": True,
        "continuedl": True,
        "retries": 3,
    }


def video_download_options(
    progress_hook: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    options = base_download_options(progress_hook)
    options.update(
        {
            "format": "bv*+ba/b",
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
