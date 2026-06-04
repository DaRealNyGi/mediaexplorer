from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

from mediaexplorer.paths import (
    AUDIO_SCRIPT,
    BATCH_SCRIPT,
    CONFIG_DIR,
    DOCS_DIR,
    DOWNLOAD_SCRIPT,
    DOWNLOADS_DIR,
    FFMPEG_DIR,
    FFMPEG_EXE,
    FFPROBE_EXE,
    FORMATS_SCRIPT,
    INFO_SCRIPT,
    PLAYLIST_SCRIPT,
    PROJECT_ROOT,
)
from mediaexplorer.validation import check_components, print_component_summary, status


REQUIRED_COMPONENTS = {
    "docs folder": DOCS_DIR,
    "config folder": CONFIG_DIR,
    "downloads folder": DOWNLOADS_DIR,
    "tools/ffmpeg": FFMPEG_DIR,
    "ffmpeg executable": FFMPEG_EXE,
    "ffprobe executable": FFPROBE_EXE,
    "scripts/info.py": INFO_SCRIPT,
    "scripts/formats.py": FORMATS_SCRIPT,
    "scripts/batch.py": BATCH_SCRIPT,
    "scripts/playlist.py": PLAYLIST_SCRIPT,
    "scripts/download.py": DOWNLOAD_SCRIPT,
    "scripts/audio.py": AUDIO_SCRIPT,
}


def command_output(*args: str) -> str | None:
    try:
        result = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None

    output = result.stdout.strip() or result.stderr.strip()
    return output.splitlines()[0] if output else None


def main() -> int:
    current_directory = Path.cwd()
    uv_path = shutil.which("uv")
    uv_version = command_output("uv", "--version") if uv_path else None
    yt_dlp_spec = importlib.util.find_spec("yt_dlp")

    print("MediaExplorer project health check")
    print("Read-only check: no project files are modified.")
    print()

    status("current directory", current_directory == PROJECT_ROOT, str(current_directory))
    status("Python interpreter", True, sys.executable)
    status("UV availability", uv_path is not None, uv_version or "not found")
    status("yt-dlp availability", yt_dlp_spec is not None)

    print()
    required_checks = check_components(REQUIRED_COMPONENTS)
    if print_component_summary(required_checks):
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
