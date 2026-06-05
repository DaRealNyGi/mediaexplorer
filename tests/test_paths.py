from __future__ import annotations

import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

import mediaexplorer.paths as paths


def reload_paths() -> None:
    importlib.reload(paths)


class TestResolveExecutable:
    def test_prefers_bundled_when_present(self, tmp_path: Path) -> None:
        bundled = tmp_path / "ffmpeg"
        bundled.write_text("", encoding="utf-8")

        resolved = paths.resolve_executable(bundled, "ffmpeg")

        assert resolved == bundled

    def test_falls_back_to_system_when_bundled_missing(self, tmp_path: Path) -> None:
        bundled = tmp_path / "missing-ffmpeg"
        system = tmp_path / "system-ffmpeg"
        system.write_text("", encoding="utf-8")

        with patch.object(paths.shutil, "which", return_value=str(system)):
            resolved = paths.resolve_executable(bundled, "ffmpeg")

        assert resolved == system

    def test_returns_bundled_path_when_nothing_found(self, tmp_path: Path) -> None:
        bundled = tmp_path / "missing-ffmpeg"

        with patch.object(paths.shutil, "which", return_value=None):
            resolved = paths.resolve_executable(bundled, "ffmpeg")

        assert resolved == bundled
        assert not resolved.exists()


class TestPlatformExecutableNames:
    @pytest.mark.parametrize(
        ("platform", "ffmpeg_name", "ffprobe_name"),
        [
            ("win32", "ffmpeg.exe", "ffprobe.exe"),
            ("darwin", "ffmpeg", "ffprobe"),
            ("linux", "ffmpeg", "ffprobe"),
        ],
    )
    def test_executable_names_match_platform(
        self,
        platform: str,
        ffmpeg_name: str,
        ffprobe_name: str,
    ) -> None:
        with (
            patch.object(paths.sys, "platform", platform),
            patch.object(paths.shutil, "which", return_value=None),
        ):
            reload_paths()

        assert paths.FFMPEG_NAME == ffmpeg_name
        assert paths.FFPROBE_NAME == ffprobe_name
        assert paths.BUNDLED_FFMPEG_EXE.name == ffmpeg_name
        assert paths.BUNDLED_FFPROBE_EXE.name == ffprobe_name

    def teardown_method(self) -> None:
        with patch.object(paths.shutil, "which", return_value=None):
            reload_paths()


class TestHealthCheckFfmpegAvailability:
    def test_ffmpeg_checks_pass_with_system_only(self, tmp_path: Path) -> None:
        system_ffmpeg = tmp_path / "ffmpeg"
        system_ffprobe = tmp_path / "ffprobe"
        system_ffmpeg.write_text("", encoding="utf-8")
        system_ffprobe.write_text("", encoding="utf-8")

        with (
            patch.object(paths, "BUNDLED_FFMPEG_EXE", tmp_path / "tools" / "ffmpeg" / "bin" / "ffmpeg"),
            patch.object(paths, "BUNDLED_FFPROBE_EXE", tmp_path / "tools" / "ffmpeg" / "bin" / "ffprobe"),
            patch.object(paths, "FFMPEG_EXE", system_ffmpeg),
            patch.object(paths, "FFPROBE_EXE", system_ffprobe),
        ):
            from mediaexplorer.validation import check_executables

            results = check_executables(
                {
                    "ffmpeg availability": paths.FFMPEG_EXE,
                    "ffprobe availability": paths.FFPROBE_EXE,
                },
            )

        assert all(results)
