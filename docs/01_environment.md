# Development Environment

## Primary Development Platform

All development is performed inside:

- WSL2 (Ubuntu)
- VS Code connected to WSL
- Bash Shell

Do not assume Windows-native execution unless explicitly instructed.

## Core Toolchain

### Python

Python is managed through UV.

```bash
uv venv
uv sync
uv run python main.py
```

### AI Assistant

Primary coding assistant:

- Codex

### Virtual Environments

Projects use `.venv` inside the project root.

Expected interpreter:

```bash
/home/nygi/projects/project_name/.venv/bin/python
```

Verify using:

```bash
which python
```

## Preferred Project Location

```bash
~/projects/
```

Avoid active development in `/mnt/c/` except for transfer or backup.

## VS Code

Open from WSL:

```bash
code .
```

Expected indicator:

```text
WSL: Ubuntu
```
