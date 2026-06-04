from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = PROJECT_ROOT / "config"
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TOOLS_DIR = PROJECT_ROOT / "tools"

FFMPEG_DIR = TOOLS_DIR / "ffmpeg"
FFMPEG_BIN_DIR = FFMPEG_DIR / "bin"
FFMPEG_EXE = FFMPEG_BIN_DIR / "ffmpeg.exe"
FFPROBE_EXE = FFMPEG_BIN_DIR / "ffprobe.exe"

INFO_SCRIPT = SCRIPTS_DIR / "info.py"
FORMATS_SCRIPT = SCRIPTS_DIR / "formats.py"
DOWNLOAD_SCRIPT = SCRIPTS_DIR / "download.py"
AUDIO_SCRIPT = SCRIPTS_DIR / "audio.py"
BATCH_SCRIPT = SCRIPTS_DIR / "batch.py"
PLAYLIST_SCRIPT = SCRIPTS_DIR / "playlist.py"
