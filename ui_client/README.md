# MediaExplorer UI Client

Optional desktop wrapper for MediaExplorer. This folder is isolated from the core package and can be deleted without affecting the rest of the project.

## What it is

- A Tkinter sidecar that calls the existing CLI scripts as subprocesses.
- It does **not** replace `scripts/` or import from `src/mediaexplorer`.
- It does **not** change existing CLI behavior.
- It inherits script behavior (including `config/yt-dlp.conf` applied by the Python helper layer) because each action runs the same scripts from the repository root.

## Run

From the repository root:

```bash
uv run python ui_client/app.py
```

Makefile shortcut:

```bash
make ui
```

## Validation

```bash
make check
```

Runs UI compile check, pytest, and the project health script.

If yt-dlp warns about a missing JavaScript runtime, install Deno on macOS (`brew install deno`) and rerun `make check`. Deno is optional but improves YouTube extraction reliability; the health check does not require it.

## Actions

The UI exposes the same entry points as the CLI:

| Button | Script |
|--------|--------|
| Get Info | `scripts/info.py` |
| List Formats | `scripts/formats.py` |
| Inspect Playlist | `scripts/playlist.py` |
| Download Video | `scripts/download.py` |
| Extract Audio | `scripts/audio.py` |

Each action runs:

```text
<current Python> scripts/<script>.py <URL>
```

with the working directory set to the repository root.

## QuickTime compatible downloads

The **QuickTime compatible** checkbox applies only to **Download Video**. When checked, the UI runs:

```text
<current Python> scripts/download.py <URL> --compatible
```

This prefers H.264/AAC MP4 formats for macOS QuickTime Player compatibility. **Extract Audio** is unchanged.

## Download folder limitation

The UI includes a download folder picker for convenience, defaulting to `downloads/`.

**Current limitation:** the underlying download scripts do not expose a CLI flag for a custom output folder. They always write to the project `downloads/` directory via `src/mediaexplorer/paths.py`.

Until those scripts add supported output-path flags, changing the folder in the UI has no effect on where files are saved.

## Output

- Command stdout and stderr appear in the scrollable output panel.
- Status messages and errors are shown below the output.
- Use **Clear** to reset the output panel.
