from __future__ import annotations

import argparse
import sys
from typing import Any

from mediaexplorer.paths import CONFIG_DIR
from mediaexplorer.ytdlp import (
    DownloadError,
    YoutubeDL,
    missing_ytdlp_message,
    readonly_options,
    ytdlp_available,
)


CONFIG_PATH = CONFIG_DIR / "yt-dlp.conf"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List available media formats without downloading.",
    )
    parser.add_argument("url", help="Media URL to inspect")
    return parser.parse_args()


def format_filesize(value: Any) -> str:
    if not isinstance(value, int) or value <= 0:
        return "unknown"

    size = float(value)
    units = ("B", "KiB", "MiB", "GiB")
    unit = units[0]

    for unit in units:
        if size < 1024 or unit == units[-1]:
            break
        size /= 1024

    if unit == "B":
        return f"{int(size)} {unit}"

    return f"{size:.1f} {unit}"


def format_resolution(media_format: dict[str, Any]) -> str:
    if media_format.get("vcodec") in (None, "none"):
        return "audio only"

    width = media_format.get("width")
    height = media_format.get("height")
    if isinstance(width, int) and isinstance(height, int):
        return f"{width}x{height}"

    resolution = media_format.get("resolution")
    if isinstance(resolution, str) and resolution:
        return resolution

    return "unknown"


def format_type(media_format: dict[str, Any]) -> str:
    has_audio = media_format.get("acodec") not in (None, "none")
    has_video = media_format.get("vcodec") not in (None, "none")

    if has_audio and has_video:
        return "Combined"
    if has_audio:
        return "Audio"
    if has_video:
        return "Video"

    return "Unknown"


def display_formats(info: dict[str, Any]) -> bool:
    formats = info.get("formats")
    if not isinstance(formats, list) or not formats:
        print("Error: format lookup returned no usable formats.", file=sys.stderr)
        return False

    print(f"{'ID':<8}{'EXT':<8}{'RESOLUTION':<16}{'TYPE':<12}{'SIZE'}")

    for media_format in formats:
        if not isinstance(media_format, dict):
            continue

        format_id = str(media_format.get("format_id") or "unknown")
        extension = str(media_format.get("ext") or "unknown")
        resolution = format_resolution(media_format)
        media_type = format_type(media_format)
        size = format_filesize(
            media_format.get("filesize") or media_format.get("filesize_approx"),
        )

        print(f"{format_id:<8}{extension:<8}{resolution:<16}{media_type:<12}{size}")

    return True


def main() -> int:
    args = parse_args()

    if not ytdlp_available():
        print(missing_ytdlp_message().replace("uv sync", "`uv sync`"), file=sys.stderr)
        return 1

    if not CONFIG_PATH.is_file():
        print(f"Error: missing config file: {CONFIG_PATH}", file=sys.stderr)
        return 1

    options = readonly_options()

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(args.url, download=False)
    except DownloadError as exc:
        print(f"Error: format lookup failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return 1

    if not isinstance(info, dict):
        print("Error: format lookup returned no usable result.", file=sys.stderr)
        return 1

    if not display_formats(info):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
