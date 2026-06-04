from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    "info": PROJECT_ROOT / "scripts" / "info.py",
    "audio": PROJECT_ROOT / "scripts" / "audio.py",
    "download": PROJECT_ROOT / "scripts" / "download.py",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process a text file of media URLs.",
    )
    parser.add_argument("url_file", help="Text file with one URL per line")
    parser.add_argument(
        "--mode",
        choices=tuple(SCRIPTS),
        default="info",
        help="Processing mode to run for each URL",
    )
    return parser.parse_args()


def load_urls(path: Path) -> list[str]:
    urls: list[str] = []

    for line in path.read_text().splitlines():
        url = line.strip()
        if not url or url.startswith("#"):
            continue
        urls.append(url)

    return urls


def main() -> int:
    args = parse_args()
    url_file = Path(args.url_file)

    if not url_file.is_file():
        print(f"Error: URL file not found: {url_file}", file=sys.stderr)
        return 1

    urls = load_urls(url_file)
    if not urls:
        print(f"Error: no usable URLs found in: {url_file}", file=sys.stderr)
        return 1

    script = SCRIPTS[args.mode]
    successes = 0
    failures = 0
    total = len(urls)

    for index, url in enumerate(urls, start=1):
        print()
        print(f"[{index}/{total}] {args.mode}: {url}", flush=True)

        result = subprocess.run(
            [sys.executable, str(script), url],
            check=False,
            stderr=subprocess.STDOUT,
        )

        if result.returncode == 0:
            successes += 1
            print(f"[PASS] {url}")
        else:
            failures += 1
            print(f"[FAIL] {url}")

    print()
    print(f"Summary: {successes}/{total} URLs succeeded, {failures} failed.")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
