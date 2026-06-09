# ChatGPT Context

## Current Version

MediaExplorer v0.3.0

## Repository

https://github.com/DaRealNyGi/mediaexplorer

Owner:
DaRealNyGi

Primary project path:

```text
/home/nygi/projects/mediaexplorer
```

## Architecture Overview

MediaExplorer is a Python media exploration and extraction project built around:
- UV
- yt-dlp
- FFmpeg
- WSL
- Tkinter for the v0.3 UI

Shared package:
- `src/mediaexplorer/paths.py` centralizes project paths and FFmpeg/FFprobe resolution.
- `src/mediaexplorer/validation.py` centralizes health-check helpers.
- `src/mediaexplorer/ytdlp.py` centralizes yt-dlp imports and option builders.

CLI scripts:
- `scripts/test.py`
- `scripts/info.py`
- `scripts/formats.py`
- `scripts/playlist.py`
- `scripts/download.py`
- `scripts/audio.py`
- `scripts/batch.py`

UI:
- `main.py` launches the Tkinter UI.
- `ui_client/app.py` implements the subprocess-based UI.
- The UI calls existing CLI scripts and does not duplicate yt-dlp or FFmpeg logic.

## Current Status

Current release:
- v0.3.0 Tkinter UI Stabilization Release

Current expected validation:
- Health check PASS: 11/11
- Pytest PASS: 43 tests

Current supported workflows:
- Health Check
- Metadata Lookup
- Format Listing
- Playlist Inspection
- Video Download
- Audio Extraction
- Batch Processing through CLI
- Tkinter UI for single-URL workflows

## Major Decisions

- Use WSL as the primary development environment.
- Use UV for dependency and command execution.
- Keep FFmpeg out of git.
- Resolve FFmpeg/FFprobe through shared path logic.
- Keep UI subprocess-based for v0.3.
- Use Tkinter for v0.3 instead of adding a larger GUI framework.
- Keep batch UI deferred to v0.4.
- Require health check and pytest before release-quality changes.

## Known Limitations

- Some YouTube URLs may require authentication and return:

  ```text
  Sign in to confirm you're not a bot.
  ```

- v0.3 does not include cookies or authenticated extraction support.
- UI output copy behavior may need improvement.
- UI output is not streamed live.
- No cancel button exists yet.
- Custom output folders are not supported yet.
- Batch Processing UI is deferred to v0.4.

## Current Priorities

Primary v0.4 planning areas:
- Copyable Output Panel
- Batch Processing UI
- Streaming Output
- Cancel Running Job
- Custom Output Folder
- Metadata Export
- Download History
- Channel Explorer
- Authenticated Extraction Support
