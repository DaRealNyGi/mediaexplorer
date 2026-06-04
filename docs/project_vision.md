# MediaExplorer

## Purpose

MediaExplorer is a Python-based media extraction and exploration platform.

The project uses:

* Python
* UV
* yt-dlp
* FFmpeg
* Deno
* Git
* VS Code
* WSL

## Primary Goals

1. Inspect media metadata
2. Download media
3. Extract audio
4. Convert media formats
5. Explore available formats
6. Support batch processing
7. Provide a GUI interface

## Development Principles

* Modular architecture
* Project-local dependencies
* Reproducible environments
* Clear separation of concerns
* Minimal external assumptions

## Current Architecture

The `src/mediaexplorer/` package contains shared helpers:

* `paths.py` centralizes project paths.
* `validation.py` centralizes health-check validation helpers.
* `ytdlp.py` centralizes yt-dlp imports and option builders.

CLI scripts remain in `scripts/`. `batch.py` orchestrates the existing CLI scripts with subprocesses.

## Initial Features

### Metadata Explorer

Input:

* URL

Output:

* Title
* Uploader
* Duration
* Upload date
* View count
* Available formats

### Media Downloader

Input:

* URL

Output:

* Highest quality media available

### Audio Extractor

Input:

* URL or media file

Output:

* MP3 or selected audio format

## Long-Term Vision

MediaExplorer should evolve into a complete desktop application capable of:

* Exploring media metadata
* Downloading media
* Converting media
* Organizing downloaded assets
* Managing batch operations
* Supporting multiple providers through a unified interface
