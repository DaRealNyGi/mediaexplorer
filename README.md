# MediaExplorer

## Overview

MediaExplorer is a Python-based media exploration and extraction tool built with:

- Python
- UV
- yt-dlp
- FFmpeg
- WSL

## Environment

Active project:

```bash
/home/nygi/projects/mediaexplorer
```

## Installation

```bash
uv sync
```

## Validation

```bash
uv run python scripts/test.py
```

## Desktop UI

MediaExplorer v0.3 includes a small Tkinter UI that launches the existing CLI
scripts as subprocesses. It does not duplicate yt-dlp or FFmpeg logic.

```bash
uv run python main.py
```

The UI includes Health Check, metadata lookup, format listing, playlist
inspection, video download, and audio extraction. Downloads and extracted audio
save to the project `downloads/` folder.

Batch Processing remains available through the CLI and is deferred in the UI
until v0.4.

## Known Limitations

Some YouTube URLs, especially Shorts or bot-protected videos, may fail with:

```text
Sign in to confirm you're not a bot.
```

For v0.3, MediaExplorer should surface this error clearly but does not add
cookies or authenticated extraction support.

## Quick Reference

See:
`docs/quick_reference.md`

## Roadmap

See:
`docs/roadmap_v0.3.md`

## Metadata

```bash
uv run python scripts/info.py URL
```

## Format Listing

```bash
uv run python scripts/formats.py URL
```

## Video Download

Default mode downloads the best available quality (may use codecs such as AV1 that QuickTime Player does not support).

```bash
uv run python scripts/download.py URL
```

For QuickTime-friendly H.264/AAC MP4 when available:

```bash
uv run python scripts/download.py URL --compatible
```

## Audio Extraction

```bash
uv run python scripts/audio.py URL
```

## Batch Processing

```bash
uv run python scripts/batch.py urls.txt
uv run python scripts/batch.py urls.txt --mode info
uv run python scripts/batch.py urls.txt --mode audio
uv run python scripts/batch.py urls.txt --mode download
```

Default mode is `info`. Blank lines and lines beginning with `#` are skipped.

## Playlist Inspection

```bash
uv run python scripts/playlist.py URL
uv run python scripts/playlist.py URL --mode info
```

`playlist.py` is inspection-only and does not download media.

## Project Structure

```text
docs/
scripts/
src/mediaexplorer/
downloads/
tools/
```

## Shared Package

`src/mediaexplorer/paths.py` centralizes project paths.
`src/mediaexplorer/validation.py` centralizes health-check validation helpers.
`src/mediaexplorer/ytdlp.py` centralizes yt-dlp imports and option builders.

CLI entry points still live in `scripts/`. `batch.py` remains a subprocess orchestrator for the existing CLI scripts.

## Current Application State

- Metadata inspection
- Format listing
- Batch processing
- Playlist inspection
- Video download
- Audio extraction
- FFmpeg integration
- Health checking
- Tkinter UI launched by `uv run python main.py`
- CLI workflows remain supported
