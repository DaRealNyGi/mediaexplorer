from __future__ import annotations

import argparse
import sys
from typing import Any

from mediaexplorer.paths import CONFIG_DIR, DOWNLOADS_DIR, FFMPEG_EXE
from mediaexplorer.validation import component_exists, executable_available
from mediaexplorer.ytdlp import (
    DownloadError,
    YoutubeDL,
    missing_ytdlp_message,
    video_download_options,
    ytdlp_available,
)


CONFIG_PATH = CONFIG_DIR / "yt-dlp.conf"

REQUIRED_COMPONENTS = {
    "config/yt-dlp.conf": CONFIG_PATH,
    "downloads folder": DOWNLOADS_DIR,
}

REQUIRED_EXECUTABLES = {
    "ffmpeg availability": FFMPEG_EXE,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download media at the highest available quality.",
    )
    parser.add_argument("url", help="Media URL to download")
    return parser.parse_args()


def validate_required_components() -> bool:
    missing: list[str] = []

    for label, path in REQUIRED_COMPONENTS.items():
        if not component_exists(path):
            missing.append(f"{label}: {path}")

    for label, path in REQUIRED_EXECUTABLES.items():
        if not executable_available(path):
            missing.append(f"{label}: {path}")

    if not missing:
        return True

    print("Error: missing required project components:", file=sys.stderr)
    for item in missing:
        print(f"  - {item}", file=sys.stderr)

    return False


def progress_hook(status: dict[str, Any]) -> None:
    state = status.get("status")

    if state == "downloading":
        percent = status.get("_percent_str", "").strip()
        speed = status.get("_speed_str", "").strip()
        eta = status.get("_eta_str", "").strip()

        parts = [part for part in (percent, speed, f"ETA {eta}" if eta else "") if part]
        message = "Downloading"
        if parts:
            message = f"{message}: {' at '.join(parts[:2])}"
            if len(parts) > 2:
                message = f"{message} {parts[2]}"

        print(f"\r{message}", end="", flush=True)
        return

    if state == "finished":
        filename = status.get("filename") or "downloaded file"
        print(f"\nFinished download: {filename}")


def main() -> int:
    args = parse_args()

    if not ytdlp_available():
        print(missing_ytdlp_message().replace("uv sync", "`uv sync`"), file=sys.stderr)
        return 1

    if not validate_required_components():
        return 1

    print(f"Using FFmpeg: {FFMPEG_EXE}")

    options = video_download_options(progress_hook)

    try:
        with YoutubeDL(options) as ydl:
            ydl.download([args.url])
    except KeyboardInterrupt:
        print("\nError: download cancelled.", file=sys.stderr)
        return 1
    except DownloadError as exc:
        print(f"\nError: download failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\nError: unexpected failure: {exc}", file=sys.stderr)
        return 1

    print("Download complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
