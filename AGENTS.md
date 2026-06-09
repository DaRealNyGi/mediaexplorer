# MediaExplorer Agent Instructions

## Project

Repository owner: DaRealNyGi

Repository:
https://github.com/DaRealNyGi/mediaexplorer

Work only in:

```text
/home/nygi/projects/mediaexplorer
```

Do not use this Windows/Dropbox path for project work:

```text
/mnt/c/Users/NyGi/Dropbox/PC/Desktop/Sort/mediaexplorer
```

## Environment

Primary development environment:
- WSL2 Ubuntu
- Bash
- VS Code connected to WSL

Preferred package manager:
- UV

Use:

```bash
uv sync
uv run ...
```

Avoid manual `pip` workflows unless explicitly requested.

## Required Validation Workflow

Before diagnosing or changing behavior, run:

```bash
pwd
which python
git status
uv run python scripts/test.py
uv run pytest -q
```

Before reporting completion, run the validation requested by the task. If no
task-specific validation is requested, run at minimum:

```bash
uv run python scripts/test.py
uv run pytest -q
git status --short
```

Current expected health check:

```text
11/11 required project components present
```

## Git Safety

- Do not commit unless the user explicitly asks.
- Do not push unless the user explicitly asks.
- Do not create tags unless the user explicitly asks.
- Do not reset, checkout, or revert user work without explicit approval.
- Treat uncommitted changes as user-owned unless you made them in the current task.
- Report changed files and validation results at the end of each task.

## Repository Safety

Do not commit:
- Secrets
- Cookies
- Tokens
- Browser session data
- Downloaded media files
- `tools/ffmpeg`
- Generated caches

Authenticated extraction support, if added later, must be opt-in and must not
store authentication material in the repository.

## Architecture Rules

Reuse shared modules:
- `src/mediaexplorer/paths.py`
- `src/mediaexplorer/validation.py`
- `src/mediaexplorer/ytdlp.py`

Keep CLI scripts in `scripts/` as user-facing entry points.

The v0.3 Tkinter UI is subprocess-based and should continue to call existing
CLI scripts unless a future task explicitly approves a different architecture.
Do not duplicate yt-dlp or FFmpeg logic in the UI.

## Reporting Requirements

Final reports should include:
- Files changed or created
- Commands executed
- Validation results
- Known limitations or follow-up risks
- Any skipped validation and why it was skipped
