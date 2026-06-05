# MediaExplorer Quick Reference

## Start Here

```bash
cd ~/projects/mediaexplorer
git pull
uv run python scripts/test.py
```

## Health Check

```bash
uv run python scripts/test.py
```

## Get Video Info

```bash
uv run python scripts/info.py "URL"
```

## List Available Formats

```bash
uv run python scripts/formats.py "URL"
```

## Download Video

```bash
uv run python scripts/download.py "URL"
```

Output:

```text
downloads/*.mp4
```

## Download Audio as MP3

```bash
uv run python scripts/audio.py "URL"
```

Output:

```text
downloads/*.mp3
```

## Inspect Playlist

```bash
uv run python scripts/playlist.py "PLAYLIST_URL"
```

Note:
playlist.py is inspection-only and does not download media.

## Batch Processing

Create a text file:

```text
urls.txt
```

Example contents:

```text
# lines starting with # are ignored
https://youtube.com/watch?v=EXAMPLE1
https://youtube.com/watch?v=EXAMPLE2
```

Commands:

```bash
uv run python scripts/batch.py urls.txt
uv run python scripts/batch.py urls.txt --mode info
uv run python scripts/batch.py urls.txt --mode audio
uv run python scripts/batch.py urls.txt --mode download
```

Note:
Default batch mode is info.

## Open Downloads Folder

```bash
explorer.exe downloads
```

## FFmpeg Setup

MediaExplorer resolves FFmpeg through `src/mediaexplorer/paths.py`:

1. Prefer repo-local bundled FFmpeg when `tools/ffmpeg/bin/` contains the binaries.
2. Otherwise fall back to system FFmpeg on `PATH` (`shutil.which`).

You do not need `tools/ffmpeg` if system FFmpeg is installed and on `PATH`.

**Windows** (optional bundle):

```text
tools/ffmpeg/bin/ffmpeg.exe
tools/ffmpeg/bin/ffprobe.exe
```

**macOS/Linux** — use system FFmpeg from `PATH`, or optionally bundle:

```text
tools/ffmpeg/bin/ffmpeg
tools/ffmpeg/bin/ffprobe
```

**yt-dlp:** `config/yt-dlp.conf` no longer sets `--ffmpeg-location`. Python option builders pass `ffmpeg_location` only when bundled FFmpeg exists; otherwise yt-dlp uses system `PATH`.

## Inspect Media File

**Windows:**

```bash
./tools/ffmpeg/bin/ffmpeg.exe -i "downloads/FILENAME.mp4"
```

**macOS/Linux** (system FFmpeg):

```bash
ffmpeg -i "downloads/FILENAME.mp4"
```

**macOS/Linux** (bundled FFmpeg):

```bash
./tools/ffmpeg/bin/ffmpeg -i "downloads/FILENAME.mp4"
```

Look for:

```text
Stream #0:0 Video
Stream #0:1 Audio
```

## Common Rule

Always run this first if something seems broken:

```bash
uv run python scripts/test.py
```
