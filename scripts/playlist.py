from __future__ import annotations

import argparse
import sys
from typing import Any

from mediaexplorer.paths import CONFIG_DIR
from mediaexplorer.ytdlp import (
    DownloadError,
    YoutubeDL,
    missing_ytdlp_message,
    playlist_options,
    ytdlp_available,
)


CONFIG_PATH = CONFIG_DIR / "yt-dlp.conf"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List playlist entries without downloading.",
    )
    parser.add_argument("url", help="Playlist URL to inspect")
    parser.add_argument(
        "--mode",
        choices=("info",),
        default="info",
        help="Playlist processing mode",
    )
    return parser.parse_args()


def entry_url(entry: dict[str, Any]) -> str:
    url = entry.get("webpage_url") or entry.get("url")
    if not isinstance(url, str) or not url:
        return "Unknown"

    if url.startswith("http://") or url.startswith("https://"):
        return url

    return f"https://www.youtube.com/watch?v={url}"


def display_playlist(info: dict[str, Any]) -> bool:
    entries = info.get("entries")
    if not isinstance(entries, list):
        print("Error: playlist lookup returned no usable entries.", file=sys.stderr)
        return False

    usable_entries = [entry for entry in entries if isinstance(entry, dict)]
    skipped_entries = len(entries) - len(usable_entries)

    if not usable_entries:
        print("Error: playlist contains no usable entries.", file=sys.stderr)
        return False

    print("Playlist:")
    print(info.get("title") or "Unknown")
    print()
    print("Items:")
    print(len(entries))
    print()

    for index, entry in enumerate(usable_entries, start=1):
        print(f"[{index}] {entry.get('title') or 'Unknown'}")
        print(entry_url(entry))
        print()

    print(f"Usable entries: {len(usable_entries)}")
    print(f"Skipped entries: {skipped_entries}")
    return True


def main() -> int:
    args = parse_args()

    if not ytdlp_available():
        print(missing_ytdlp_message().replace("uv sync", "`uv sync`"), file=sys.stderr)
        return 1

    if not CONFIG_PATH.is_file():
        print(f"Error: missing config file: {CONFIG_PATH}", file=sys.stderr)
        return 1

    options = playlist_options()

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(args.url, download=False)
    except DownloadError as exc:
        print(f"Error: playlist lookup failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: unexpected failure: {exc}", file=sys.stderr)
        return 1

    if not isinstance(info, dict):
        print("Error: playlist lookup returned no usable result.", file=sys.stderr)
        return 1

    if not display_playlist(info):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
