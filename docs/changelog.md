# Changelog

## v0.3.0 - Tkinter UI Stabilization Release

### Added

* Tkinter UI launcher
* Health Check action in UI
* Main application launch through:

  ```bash
  uv run python main.py
  ```

### Changed

* UI officially supported
* Documentation updated to reflect UI workflow
* Session handoff and baseline documentation refreshed

### Fixed

* Misleading output-folder selection behavior
* Stale documentation references to pre-UI architecture
* Cross-platform FFmpeg support retained from v0.2.1

### Validation

* Health check PASS (11/11)
* Pytest PASS (43 tests)
* Manual UI smoke tests completed:

  * Health Check
  * Info
  * Formats
  * Playlist
  * Download
  * Audio

### Known Limitations

* Some YouTube URLs may require authentication and return:
  `"Sign in to confirm you're not a bot."`
* Output panel copy behavior may require improvement.
* Batch Processing UI remains deferred to v0.4.

## v0.2.1 - Cross-Platform FFmpeg Compatibility Update

### Added

* Cross-platform FFmpeg executable detection.
* Support for both:

  * `tools/ffmpeg/bin/ffmpeg.exe`
  * `tools/ffmpeg/bin/ffmpeg`
* Support for both:

  * `tools/ffmpeg/bin/ffprobe.exe`
  * `tools/ffmpeg/bin/ffprobe`

### Changed

* Shared path resolution logic now automatically selects the first available FFmpeg/FFprobe executable.
* Shared yt-dlp configuration now uses the resolved FFmpeg executable path.

### Fixed

* Health check failures on WSL installations using bundled Windows FFmpeg binaries.
* Audio extraction failures caused by unresolved FFmpeg paths in mixed Windows/WSL environments.

### Validation

Verified before release:

* Health check: PASS (11/11 required components present)
* Pytest: PASS (38 tests passed)
* Video download: PASS
* Audio extraction: PASS
* FFmpeg merge workflow: PASS
* FFprobe detection: PASS

### Notes

This release improves compatibility between Windows, WSL, and Linux-based MediaExplorer environments without changing existing user workflows.
