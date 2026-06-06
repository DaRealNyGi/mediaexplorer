# MediaExplorer v0.3 Roadmap

## Status

Planning

## Guiding Principle

v0.3 should improve usability without breaking the verified v0.2 stable baseline.

## Priority 1: Launcher Menu

Goal:
Create a simple command-line menu so users only need:

uv run python main.py

Menu options:
- Health Check
- Metadata Lookup
- Format Listing
- Playlist Inspection
- Video Download
- Audio Extraction
- Batch Processing

Acceptance Criteria:
- Existing scripts are reused.
- No duplicated yt-dlp logic.
- User can choose actions from a numbered menu.
- Health check still passes 12/12.

## Priority 2: GUI Evaluation

Goal:
Evaluate PySide6 vs Tkinter.

Preferred direction:
PySide6, unless it adds too much setup friction.

Acceptance Criteria:
- Short recommendation written before implementation.
- No GUI code until framework is approved.

## Priority 3: Metadata Export

Goal:
Export media metadata to JSON and CSV.

Acceptance Criteria:
- Works with single URL.
- Later can support batch mode.
- Does not download media.

## Priority 4: Download History

Goal:
Track completed downloads.

Possible storage:
SQLite.

Acceptance Criteria:
- Records title, URL, output path, date, and mode.
- Does not interfere with current download/audio scripts.

## Priority 5: Channel Exploration

Goal:
Inspect creator/channel metadata.

Acceptance Criteria:
- Read-only first.
- No bulk downloads by default.

## Known v0.3 Limitation: YouTube Bot Checks

Some YouTube URLs, especially Shorts or bot-protected videos, may fail with:

```text
Sign in to confirm you're not a bot.
```

For v0.3, MediaExplorer should surface this error clearly but should not add
cookies or authenticated extraction support.

## Future Roadmap: v0.4+

Optional cookies or authenticated extraction support may be considered for
v0.4 or later.

Requirements:
- Must be opt-in.
- Must not store cookies or browser session data in the repo.
- Must not commit cookies, tokens, or auth files.

## Rules For v0.3

- Preserve v0.2 stable baseline.
- Run health check before and after changes.
- Every feature requires syntax, happy-path, and failure-path validation.
- Do not commit media files.
- Do not commit tools/ffmpeg.
- Do not work outside /home/nygi/projects/mediaexplorer.
