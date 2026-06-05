from __future__ import annotations

import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_YTDLP_FILE = CONFIG_DIR / "yt-dlp.conf"
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TOOLS_DIR = PROJECT_ROOT / "tools"

FFMPEG_DIR = TOOLS_DIR / "ffmpeg"
FFMPEG_BIN_DIR = FFMPEG_DIR / "bin"

IS_WINDOWS = sys.platform.startswith("win")

FFMPEG_NAME = "ffmpeg.exe" if IS_WINDOWS else "ffmpeg"
FFPROBE_NAME = "ffprobe.exe" if IS_WINDOWS else "ffprobe"

BUNDLED_FFMPEG_EXE = FFMPEG_BIN_DIR / FFMPEG_NAME
BUNDLED_FFPROBE_EXE = FFMPEG_BIN_DIR / FFPROBE_NAME


def resolve_executable(bundled_path: Path, command_name: str) -> Path:
    if bundled_path.exists():
        return bundled_path

    system_path = shutil.which(command_name)
    if system_path:
        return Path(system_path)

    return bundled_path


FFMPEG_EXE = resolve_executable(BUNDLED_FFMPEG_EXE, "ffmpeg")
FFPROBE_EXE = resolve_executable(BUNDLED_FFPROBE_EXE, "ffprobe")

INFO_SCRIPT = SCRIPTS_DIR / "info.py"
FORMATS_SCRIPT = SCRIPTS_DIR / "formats.py"
DOWNLOAD_SCRIPT = SCRIPTS_DIR / "download.py"
AUDIO_SCRIPT = SCRIPTS_DIR / "audio.py"
BATCH_SCRIPT = SCRIPTS_DIR / "batch.py"
PLAYLIST_SCRIPT = SCRIPTS_DIR / "playlist.py"
