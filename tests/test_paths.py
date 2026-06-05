from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import mediaexplorer.paths as paths


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


class TestBundledExecutableCandidates:
    def test_candidate_order_prefers_verified_exe_paths(self) -> None:
        assert [path.name for path in paths.FFMPEG_CANDIDATES] == ["ffmpeg.exe", "ffmpeg"]
        assert [path.name for path in paths.FFPROBE_CANDIDATES] == ["ffprobe.exe", "ffprobe"]

    def test_prefers_exe_candidate_when_present(self, tmp_path: Path) -> None:
        exe = tmp_path / "ffmpeg.exe"
        extensionless = tmp_path / "ffmpeg"
        exe.write_text("", encoding="utf-8")
        extensionless.write_text("", encoding="utf-8")

        resolved = paths.first_existing_path((exe, extensionless), exe)

        assert resolved == exe

    def test_supports_extensionless_candidate_when_exe_missing(self, tmp_path: Path) -> None:
        exe = tmp_path / "ffmpeg.exe"
        extensionless = tmp_path / "ffmpeg"
        extensionless.write_text("", encoding="utf-8")

        resolved = paths.first_existing_path((exe, extensionless), exe)

        assert resolved == extensionless

    def test_falls_back_to_exe_candidate_when_bundled_missing(self, tmp_path: Path) -> None:
        exe = tmp_path / "ffmpeg.exe"
        extensionless = tmp_path / "ffmpeg"

        resolved = paths.first_existing_path((exe, extensionless), exe)

        assert resolved == exe
        assert not resolved.exists()


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
