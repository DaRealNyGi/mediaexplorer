from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "ui_client"))

from app import (  # noqa: E402
    REPO_ROOT as APP_REPO_ROOT,
    SCRIPTS,
    build_script_command,
    run_script_subprocess,
    subprocess_popen_kwargs,
)


def test_build_script_command_download_without_compatible() -> None:
    command = build_script_command("download", "https://example.com/watch")

    assert command == [sys.executable, str(SCRIPTS["download"]), "https://example.com/watch"]
    assert "--compatible" not in command


def test_build_script_command_download_with_compatible() -> None:
    command = build_script_command(
        "download",
        "https://example.com/watch",
        quicktime_compatible=True,
    )

    assert command == [
        sys.executable,
        str(SCRIPTS["download"]),
        "https://example.com/watch",
        "--compatible",
    ]


def test_build_script_command_audio_ignores_compatible_flag() -> None:
    command = build_script_command(
        "audio",
        "https://example.com/watch",
        quicktime_compatible=True,
    )

    assert command == [sys.executable, str(SCRIPTS["audio"]), "https://example.com/watch"]
    assert "--compatible" not in command


def test_subprocess_popen_kwargs_uses_close_fds_on_macos() -> None:
    with patch.object(sys, "platform", "darwin"):
        kwargs = subprocess_popen_kwargs(cwd=APP_REPO_ROOT)

    assert kwargs["close_fds"] is True
    assert kwargs["shell"] is False
    assert "preexec_fn" not in kwargs


def test_subprocess_popen_kwargs_omits_close_fds_off_macos() -> None:
    with patch.object(sys, "platform", "linux"):
        kwargs = subprocess_popen_kwargs(cwd=APP_REPO_ROOT)

    assert "close_fds" not in kwargs
    assert kwargs["shell"] is False


def test_run_script_subprocess_captures_output() -> None:
    returncode, stdout, stderr = run_script_subprocess(
        [sys.executable, "-c", "print('hello'); import sys; sys.stderr.write('err')"],
        APP_REPO_ROOT,
    )

    assert returncode == 0
    assert stdout == "hello\n"
    assert stderr == "err"
