from __future__ import annotations

import shutil
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

FFMPEG_CANDIDATES = (
    FFMPEG_BIN_DIR / "ffmpeg.exe",
    FFMPEG_BIN_DIR / "ffmpeg",
)
FFPROBE_CANDIDATES = (
    FFMPEG_BIN_DIR / "ffprobe.exe",
    FFMPEG_BIN_DIR / "ffprobe",
)


def first_existing_path(candidates: tuple[Path, ...], fallback: Path) -> Path:
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return fallback


BUNDLED_FFMPEG_EXE = first_existing_path(FFMPEG_CANDIDATES, FFMPEG_CANDIDATES[0])
BUNDLED_FFPROBE_EXE = first_existing_path(FFPROBE_CANDIDATES, FFPROBE_CANDIDATES[0])


def resolve_executable(candidates: Path | tuple[Path, ...], command_name: str) -> Path:
    if isinstance(candidates, Path):
        candidate_paths = (candidates,)
    else:
        candidate_paths = candidates

    bundled_path = first_existing_path(candidate_paths, candidate_paths[0])
    if bundled_path.exists():
        return bundled_path

    system_path = shutil.which(command_name)
    if system_path:
        return Path(system_path)

    return bundled_path


FFMPEG_EXE = resolve_executable(FFMPEG_CANDIDATES, "ffmpeg")
FFPROBE_EXE = resolve_executable(FFPROBE_CANDIDATES, "ffprobe")

INFO_SCRIPT = SCRIPTS_DIR / "info.py"
FORMATS_SCRIPT = SCRIPTS_DIR / "formats.py"
DOWNLOAD_SCRIPT = SCRIPTS_DIR / "download.py"
AUDIO_SCRIPT = SCRIPTS_DIR / "audio.py"
BATCH_SCRIPT = SCRIPTS_DIR / "batch.py"
PLAYLIST_SCRIPT = SCRIPTS_DIR / "playlist.py"
