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

## Quick Reference

See:
`docs/quick_reference.md`

## Metadata

```bash
uv run python scripts/info.py URL
```

## Format Listing

```bash
uv run python scripts/formats.py URL
```

## Video Download

```bash
uv run python scripts/download.py URL
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

## Current Features

- Metadata inspection
- Format listing
- Batch processing
- Playlist inspection
- Video download
- Audio extraction
- FFmpeg integration
- Health checking

## Current v0.2 Status

- formats.py complete
- batch.py complete
- playlist.py complete
