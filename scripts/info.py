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
        description="Retrieve media metadata without downloading.",
    )
    parser.add_argument("url", help="Media URL to inspect")
    return parser.parse_args()


def format_duration(seconds: Any) -> str:
    if not isinstance(seconds, int):
        return "Unknown"

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}:{minutes:02}:{seconds:02}"

    return f"{minutes}:{seconds:02}"


def format_upload_date(value: Any) -> str:
    if not isinstance(value, str) or len(value) != 8 or not value.isdigit():
        return "Unknown"

    return f"{value[:4]}-{value[4:6]}-{value[6:8]}"


def format_number(value: Any) -> str:
    if not isinstance(value, int):
        return "Unknown"

    return f"{value:,}"


def display_metadata(info: dict[str, Any]) -> None:
    formats = info.get("formats") or []
    available_format_count = len(formats) if isinstance(formats, list) else 0

    print(f"Title: {info.get('title') or 'Unknown'}")
    print(f"Uploader: {info.get('uploader') or 'Unknown'}")
    print(f"Duration: {format_duration(info.get('duration'))}")
    print(f"Upload date: {format_upload_date(info.get('upload_date'))}")
    print(f"View count: {format_number(info.get('view_count'))}")
    print(f"Available formats: {available_format_count}")


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
        print(f"Error: metadata lookup failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return 1

    if not isinstance(info, dict):
        print("Error: metadata lookup returned no usable result.", file=sys.stderr)
        return 1

    display_metadata(info)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
