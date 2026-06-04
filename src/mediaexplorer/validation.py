from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path


def status(label: str, ok: bool, detail: str = "", *, required: bool = False) -> bool:
    marker = "PASS" if ok else "FAIL"
    kind = "required" if required else "info"
    suffix = f" - {detail}" if detail else ""
    print(f"[{marker}] {label} ({kind}){suffix}")
    return ok


def component_exists(path: Path) -> bool:
    return path.exists()


def check_components(components: Mapping[str, Path]) -> list[bool]:
    results: list[bool] = []

    for label, path in components.items():
        exists = component_exists(path)
        results.append(status(label, exists, str(path), required=True))

    return results


def print_component_summary(results: Sequence[bool]) -> bool:
    passed = sum(1 for result in results if result)
    total = len(results)

    print()
    print(f"Summary: {passed}/{total} required project components present.")

    if passed == total:
        print("PASS: Required project components are present.")
        return True

    print("FAIL: One or more required project components are missing.")
    return False
