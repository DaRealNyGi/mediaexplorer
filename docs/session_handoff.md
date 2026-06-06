# MediaExplorer Session Handoff

## Current Status

MediaExplorer v0.3 Tkinter UI stabilization.

GitHub Repository:
https://github.com/DaRealNyGi/mediaexplorer

Branch:
main

Health Check:
11/11 required project components present

Pytest:
43 tests passing

---

## Verified Features

* Health Check (`scripts/test.py`)
* Metadata Lookup (`scripts/info.py`)
* Format Listing (`scripts/formats.py`)
* Playlist Inspection (`scripts/playlist.py`)
* Video Download (`scripts/download.py`)
* Audio Extraction (`scripts/audio.py`)
* Batch Processing (`scripts/batch.py`)
* Tkinter UI launched by `uv run python main.py`

---

## Shared Architecture

src/mediaexplorer/

* paths.py
* validation.py
* ytdlp.py

Purpose:

* paths.py = central path definitions
* validation.py = health-check helpers
* ytdlp.py = yt-dlp imports and shared option builders

The Tkinter UI remains subprocess-based and calls the existing CLI scripts.
It does not duplicate yt-dlp or FFmpeg logic.

---

## Verified Environment

Project Location:

~/projects/mediaexplorer

Python Environment:

uv

Validation Commands:

uv run python scripts/test.py
uv run pytest -q

Git Status:

Repository published to GitHub.

---

## Important Rules

1. Work only inside:

~/projects/mediaexplorer

2. Run before any feature work:

pwd
which python
uv run python scripts/test.py
uv run pytest -q

3. Every feature requires:

* Syntax validation
* Happy-path runtime validation
* Failure-path runtime validation
* Commands executed documented
* Results observed documented

Compilation alone is not validation.

4. Preserve stable behavior before merging changes.

---

## Known UI Limitation

The output panel displays command output, but output copy behavior may need
improvement.

---

## Deferred Work

* Batch Processing UI
* Cancel button
* Streaming output
* Custom output folder
* Format picker
* Metadata export
* Download history
* Channel exploration
* Authenticated cookies support

---

## First Commands Next Session

cd ~/projects/mediaexplorer
git pull
uv run python scripts/test.py
uv run pytest -q
uv run python main.py

Expected:

Health Check:
11/11

Pytest:
Passing

Working Tree:
Clean unless intentionally carrying local work
