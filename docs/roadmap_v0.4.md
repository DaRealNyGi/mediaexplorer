# MediaExplorer v0.4 Roadmap

## Status

Planning

## Goal

v0.4 should improve the v0.3 Tkinter UI without breaking existing CLI behavior
or duplicating yt-dlp/FFmpeg logic.

## Roadmap Items

### Copyable Output Panel

Description:
Improve the UI output panel so command output is easy to select, copy, and use
when reporting errors or saving results.

Priority:
High

Status:
Planned

Dependencies:
- Current Tkinter output panel
- Manual UI smoke testing

### Batch Processing UI

Description:
Add UI support for selecting a URL list file and running existing
`scripts/batch.py` modes.

Priority:
High

Status:
Deferred from v0.3

Dependencies:
- File picker design
- Batch mode selector
- Existing `scripts/batch.py`
- Clear long-running job feedback

### Streaming Output

Description:
Show subprocess stdout and stderr incrementally while a command is running.

Priority:
High

Status:
Planned

Dependencies:
- Subprocess execution updates
- Thread-safe UI queue handling
- Manual validation with downloads and audio extraction

### Cancel Running Job

Description:
Allow users to stop an active UI subprocess.

Priority:
Medium

Status:
Planned

Dependencies:
- Streaming output or process handle tracking
- Safe subprocess termination behavior
- Clear canceled-job status messages

### Custom Output Folder

Description:
Allow users to choose where downloads and extracted audio are saved.

Priority:
Medium

Status:
Planned

Dependencies:
- CLI support for custom output paths
- Shared path or option handling
- Tests for default and custom output behavior

### Metadata Export

Description:
Export metadata lookup results to JSON and CSV without downloading media.

Priority:
Medium

Status:
Planned

Dependencies:
- Metadata extraction helpers
- Output schema decision
- File naming and output path rules

### Download History

Description:
Track completed downloads with title, URL, output path, date, and mode.

Priority:
Medium

Status:
Planned

Dependencies:
- Storage decision, likely SQLite
- Non-invasive integration with download/audio scripts
- Privacy and cleanup guidance

### Channel Explorer

Description:
Inspect creator or channel metadata in a read-only workflow.

Priority:
Low

Status:
Planned

Dependencies:
- yt-dlp channel metadata behavior
- Read-only UI and CLI design
- Guardrails against accidental bulk downloads

### Authenticated Extraction Support

Description:
Optionally support cookies or authenticated extraction for URLs that require
sign-in or bot verification.

Priority:
Low

Status:
Planned for v0.4+ investigation

Dependencies:
- Security design
- User opt-in flow
- Documentation for local-only auth files
- Rules preventing cookies, tokens, or browser session data from being stored
  or committed in the repository
