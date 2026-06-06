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
uv run python main.py
```

Makefile shortcut:

```bash
make ui
```

Direct sidecar launch is also available for development:

```bash
uv run python ui_client/app.py
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
| Health Check | `scripts/test.py` |
| Get Info | `scripts/info.py` |
| List Formats | `scripts/formats.py` |
| Inspect Playlist | `scripts/playlist.py` |
| Download Video | `scripts/download.py` |
| Extract Audio | `scripts/audio.py` |

Media actions run:

```text
<current Python> scripts/<script>.py <URL>
```

with the working directory set to the repository root.

Health Check runs without a URL:

```text
<current Python> scripts/test.py
```

## QuickTime compatible downloads

The **QuickTime compatible** checkbox applies only to **Download Video**. When checked, the UI runs:

```text
<current Python> scripts/download.py <URL> --compatible
```

This prefers H.264/AAC MP4 formats for macOS QuickTime Player compatibility. **Extract Audio** is unchanged.

## Output folder

The UI shows the fixed project output folder:

```text
downloads/
```

The download scripts do not expose a CLI flag for a custom output folder yet, so v0.3 does not include a folder picker.

## Deferred

Batch Processing UI is deferred to v0.4. The existing CLI remains available:

```bash
uv run python scripts/batch.py urls.txt
```

## Output

- Command stdout and stderr appear in the scrollable output panel.
- Status messages and errors are shown below the output.
- Use **Clear** to reset the output panel.
