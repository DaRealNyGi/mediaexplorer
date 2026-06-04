# Codex Operating Rules

## Environment Awareness

Always determine:

```bash
pwd
which python
```

before diagnosing environment issues.

## WSL Assumptions

Assume:

- Linux
- Bash
- WSL2

unless explicitly told otherwise.

## Python Rules

Prefer:

```bash
uv sync
uv run
```

over manual pip workflows.

## Debugging Order

1. Verify current directory
2. Verify interpreter
3. Verify virtual environment
4. Verify dependencies
5. Verify project structure
6. Inspect code

## Code Changes

Before modifying code:

- Understand project structure
- Inspect relevant files
- Explain proposed change
- Minimize unnecessary edits
