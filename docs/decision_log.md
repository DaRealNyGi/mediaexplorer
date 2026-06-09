# Decision Log

## Accepted Decisions

### Use UV

Decision:
Use UV for dependency management and command execution.

Reason:
UV keeps project setup reproducible and avoids manual virtual environment drift.

Current commands:

```bash
uv sync
uv run python scripts/test.py
uv run pytest -q
```

### Use WSL

Decision:
Use WSL2 Ubuntu as the primary development environment.

Reason:
The verified project setup, paths, shell commands, and FFmpeg behavior are based
on WSL.

Primary path:

```text
/home/nygi/projects/mediaexplorer
```

### Keep UI Subprocess-Based

Decision:
The v0.3 Tkinter UI calls existing CLI scripts as subprocesses.

Reason:
This preserves stable CLI behavior and avoids duplicating yt-dlp or FFmpeg
logic in the UI.

### Use Tkinter For v0.3

Decision:
Use Tkinter for the v0.3 UI stabilization release.

Reason:
Tkinter provides a low-dependency desktop UI path and avoids adding PySide6 or
another larger GUI dependency during stabilization.

### Use Shared Modules

Decision:
Shared behavior belongs in:
- `src/mediaexplorer/paths.py`
- `src/mediaexplorer/validation.py`
- `src/mediaexplorer/ytdlp.py`

Reason:
Centralized path handling, health-check helpers, and yt-dlp options reduce
duplication and keep CLI/UI behavior consistent.

### Do Not Commit FFmpeg

Decision:
FFmpeg binaries and `tools/ffmpeg` should not be committed.

Reason:
Bundled binaries are large environment artifacts. The project can use local
bundled binaries or system FFmpeg on `PATH`.

### Require Health Check Before Releases

Decision:
Run the project health check before release-quality changes are considered
complete.

Current expected result:

```text
11/11 required project components present
```

Release-quality validation should also include:

```bash
uv run pytest -q
```
