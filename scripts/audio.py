from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from mediaexplorer.ytdlp import (
    DownloadError,
    YoutubeDL,
    audio_extract_options,
    missing_ytdlp_message,
    ytdlp_available,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "yt-dlp.conf"
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
FFMPEG_BIN = PROJECT_ROOT / "tools" / "ffmpeg" / "bin"
FFMPEG_EXE = FFMPEG_BIN / "ffmpeg.exe"

REQUIRED_COMPONENTS = {
    "config/yt-dlp.conf": CONFIG_PATH,
    "downloads folder": DOWNLOADS_DIR,
    "tools/ffmpeg/bin/ffmpeg.exe": FFMPEG_EXE,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract media audio as an MP3 file.",
    )
    parser.add_argument("url", help="Media URL to extract audio from")
    return parser.parse_args()


def validate_required_components() -> bool:
    missing: list[str] = []

    for label, path in REQUIRED_COMPONENTS.items():
        exists = path.is_file() if path.suffix else path.is_dir()
        if not exists:
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

    options = audio_extract_options(progress_hook)

    try:
        with YoutubeDL(options) as ydl:
            ydl.download([args.url])
    except KeyboardInterrupt:
        print("\nError: audio extraction cancelled.", file=sys.stderr)
        return 1
    except DownloadError as exc:
        print(f"\nError: audio extraction failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\nError: unexpected failure: {exc}", file=sys.stderr)
        return 1

    print("Audio extraction complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
