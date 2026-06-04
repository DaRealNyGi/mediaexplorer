# MediaExplorer Stable Baseline (v0.2)

## Verified Features

* [x] Health Check
* [x] Metadata Lookup
* [x] Format Listing
* [x] Playlist Inspection
* [x] Video Download
* [x] Audio Extraction
* [x] Batch Processing

## Verified Environment

* [x] WSL
* [x] UV
* [x] FFmpeg
* [x] yt-dlp

## Architecture

Shared Package:

* [x] src/mediaexplorer/paths.py
* [x] src/mediaexplorer/validation.py
* [x] src/mediaexplorer/ytdlp.py

CLI Scripts:

* [x] scripts/test.py
* [x] scripts/info.py
* [x] scripts/formats.py
* [x] scripts/playlist.py
* [x] scripts/download.py
* [x] scripts/audio.py
* [x] scripts/batch.py

## Validation Standard

A feature is not considered complete until:

1. Syntax validation passes.
2. Happy-path runtime validation passes.
3. Failure-path runtime validation passes.
4. Commands executed are documented.
5. Results observed are documented.

Compilation alone is not sufficient validation.

## Known Limitations

* Batch processing remains a subprocess orchestrator.
* Some scripts still contain script-local validation logic.
* No GUI layer currently exists.
* No database layer currently exists.

## Future Development Rule

Every new feature must preserve the stable baseline before being considered complete.
