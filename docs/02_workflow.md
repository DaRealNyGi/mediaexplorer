# Development Workflow

## Creating New Projects

```bash
mkdir project_name
cd project_name
uv init
uv venv
uv sync
```

## Opening Projects

```bash
cd ~/projects/project_name
code .
```

## Running Applications

Preferred:

```bash
uv run python main.py
```

Alternative:

```bash
source .venv/bin/activate
python main.py
```

## Diagnostics

```bash
pwd
which python
uv --version
uv pip list
```

## Before Debugging

Determine:

1. Current directory
2. Active interpreter
3. Active virtual environment
4. Installed packages
5. Project structure
