# MediaExplorer v0.3 Roadmap

## Status

Tkinter UI stabilization implemented.

## Guiding Principle

v0.3 improves usability without breaking the verified v0.2.1 stable behavior.
The UI remains a subprocess wrapper around the existing CLI scripts and does
not duplicate yt-dlp or FFmpeg logic.

## Implemented In v0.3

### Tkinter UI Launch

`main.py` launches the Tkinter UI:

```bash
uv run python main.py
```

Direct sidecar launch remains available for development:

```bash
uv run python ui_client/app.py
```

### UI Actions

Implemented UI actions:
- Health Check
- Metadata Lookup
- Format Listing
- Playlist Inspection
- Video Download
- Audio Extraction

Health Check runs `scripts/test.py` and does not require a URL.

### Output Folder Display

The UI shows the fixed project output folder:

```text
downloads/
```

Custom output folder support is not implemented in v0.3.

## Known v0.3 Limitations

### YouTube Bot Checks

Some YouTube URLs, especially Shorts or bot-protected videos, may fail with:

```text
Sign in to confirm you're not a bot.
```

For v0.3, MediaExplorer should surface this error clearly but should not add
cookies or authenticated extraction support.

### UI Output Copying

The output panel displays command stdout and stderr, but output copy behavior
may need improvement in a later release.

## Deferred To v0.4+

- Batch Processing UI
- Cancel button
- Streaming output
- Custom output folder
- Format picker
- Metadata export
- Download history
- Channel exploration
- Authenticated cookies support

Authenticated cookies support requirements:
- Must be opt-in.
- Must not store cookies or browser session data in the repo.
- Must not commit cookies, tokens, or auth files.

## Rules For v0.3

- Preserve v0.2.1 stable behavior.
- Run health check before and after changes.
- Run pytest before considering changes complete.
- Every feature requires syntax, happy-path, and failure-path validation.
- Do not commit media files.
- Do not commit tools/ffmpeg.
- Do not work outside `/home/nygi/projects/mediaexplorer`.
