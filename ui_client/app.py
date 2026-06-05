"""Optional Tkinter desktop wrapper for MediaExplorer scripts."""

from __future__ import annotations

import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOWNLOADS_DIR = REPO_ROOT / "downloads"

SCRIPTS = {
    "info": REPO_ROOT / "scripts" / "info.py",
    "formats": REPO_ROOT / "scripts" / "formats.py",
    "playlist": REPO_ROOT / "scripts" / "playlist.py",
    "download": REPO_ROOT / "scripts" / "download.py",
    "audio": REPO_ROOT / "scripts" / "audio.py",
}

BUTTON_LABELS = {
    "info": "Get Info",
    "formats": "List Formats",
    "playlist": "Inspect Playlist",
    "download": "Download Video",
    "audio": "Extract Audio",
}

UI_QUEUE_POLL_MS = 100


def build_script_command(
    script_key: str,
    url: str,
    *,
    quicktime_compatible: bool = False,
) -> list[str]:
    command = [sys.executable, str(SCRIPTS[script_key]), url]
    if script_key == "download" and quicktime_compatible:
        command.append("--compatible")
    return command


def subprocess_popen_kwargs(*, cwd: Path) -> dict:
    kwargs: dict = {
        "cwd": cwd,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "shell": False,
    }
    if sys.platform == "darwin":
        kwargs["close_fds"] = True
    return kwargs


def run_script_subprocess(command: list[str], cwd: Path) -> tuple[int, str, str]:
    with subprocess.Popen(command, **subprocess_popen_kwargs(cwd=cwd)) as process:
        stdout, stderr = process.communicate()
    return process.returncode or 0, stdout or "", stderr or ""


class MediaExplorerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MediaExplorer UI")
        self.root.minsize(640, 480)

        self._active_button: ttk.Button | None = None
        self._running = False
        self._ui_queue: queue.Queue[tuple] = queue.Queue()

        self._build_ui()
        self._poll_ui_queue()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        url_frame = ttk.LabelFrame(main, text="Media URL", padding=8)
        url_frame.pack(fill=tk.X, pady=(0, 8))

        self.url_var = tk.StringVar()
        ttk.Entry(url_frame, textvariable=self.url_var).pack(fill=tk.X)

        folder_frame = ttk.LabelFrame(main, text="Download Folder", padding=8)
        folder_frame.pack(fill=tk.X, pady=(0, 8))

        folder_row = ttk.Frame(folder_frame)
        folder_row.pack(fill=tk.X)

        self.folder_var = tk.StringVar(value=str(DEFAULT_DOWNLOADS_DIR))
        ttk.Entry(folder_row, textvariable=self.folder_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8)
        )
        ttk.Button(folder_row, text="Browse…", command=self._browse_folder).pack(
            side=tk.LEFT
        )

        ttk.Label(
            folder_frame,
            text="Note: scripts currently save to the project downloads/ folder.",
            wraplength=600,
        ).pack(anchor=tk.W, pady=(6, 0))

        options_frame = ttk.LabelFrame(main, text="Download Options", padding=8)
        options_frame.pack(fill=tk.X, pady=(0, 8))

        self.quicktime_compatible_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="QuickTime compatible",
            variable=self.quicktime_compatible_var,
        ).pack(anchor=tk.W)

        button_frame = ttk.Frame(main)
        button_frame.pack(fill=tk.X, pady=(0, 8))

        self.buttons: dict[str, ttk.Button] = {}
        for key, label in BUTTON_LABELS.items():
            btn = ttk.Button(
                button_frame,
                text=label,
                command=lambda k=key: self._run_command(k),
            )
            btn.pack(side=tk.LEFT, padx=(0, 6), pady=2)
            self.buttons[key] = btn

        output_frame = ttk.LabelFrame(main, text="Output", padding=8)
        output_frame.pack(fill=tk.BOTH, expand=True)

        output_toolbar = ttk.Frame(output_frame)
        output_toolbar.pack(fill=tk.X, pady=(0, 6))
        ttk.Button(output_toolbar, text="Clear", command=self._clear_output).pack(
            side=tk.LEFT
        )

        self.output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=16,
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        status_frame = ttk.Frame(main)
        status_frame.pack(fill=tk.X, pady=(8, 0))

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(status_frame, textvariable=self.status_var).pack(anchor=tk.W)

    def _poll_ui_queue(self) -> None:
        while True:
            try:
                message = self._ui_queue.get_nowait()
            except queue.Empty:
                break
            self._handle_ui_message(message)

        self.root.after(UI_QUEUE_POLL_MS, self._poll_ui_queue)

    def _handle_ui_message(self, message: tuple) -> None:
        kind = message[0]

        if kind == "output":
            self._append_output(message[1])
        elif kind == "status":
            self._set_status(message[1])
        elif kind == "release":
            self._release_button()

    def _browse_folder(self) -> None:
        selected = filedialog.askdirectory(
            initialdir=self.folder_var.get() or str(DEFAULT_DOWNLOADS_DIR),
            title="Select download folder",
        )
        if selected:
            self.folder_var.set(selected)

    def _clear_output(self) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.configure(state=tk.DISABLED)
        self.status_var.set("Output cleared.")

    def _append_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)

    def _validate_url(self) -> str | None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Enter a media URL first.")
            self._set_status("Error: URL is required.")
            return None
        return url

    def _run_command(self, script_key: str) -> None:
        if self._running:
            return

        url = self._validate_url()
        if url is None:
            return

        script_path = SCRIPTS[script_key]
        if not script_path.is_file():
            messagebox.showerror(
                "Missing script",
                f"Script not found:\n{script_path}",
            )
            self._set_status(f"Error: missing script {script_path.name}.")
            return

        button = self.buttons[script_key]
        self._active_button = button
        self._running = True
        button.configure(state=tk.DISABLED)

        label = BUTTON_LABELS[script_key]
        self._set_status(f"Running {label}…")
        self._append_output(f"\n{'=' * 60}\n$ {script_path.name} {url}\n{'=' * 60}\n")

        quicktime_compatible = (
            script_key == "download" and self.quicktime_compatible_var.get()
        )

        thread = threading.Thread(
            target=self._execute_script,
            args=(script_key, url, label, quicktime_compatible),
            daemon=True,
        )
        thread.start()

    def _execute_script(
        self,
        script_key: str,
        url: str,
        label: str,
        quicktime_compatible: bool = False,
    ) -> None:
        command = build_script_command(
            script_key,
            url,
            quicktime_compatible=quicktime_compatible,
        )
        try:
            returncode, stdout, stderr = run_script_subprocess(command, REPO_ROOT)
            output = stdout + stderr

            if output:
                self._ui_queue.put(("output", output))
                if not output.endswith("\n"):
                    self._ui_queue.put(("output", "\n"))

            if returncode == 0:
                self._ui_queue.put(("status", f"{label} finished successfully."))
            else:
                self._ui_queue.put(
                    (
                        "status",
                        f"Error: {label} failed (exit code {returncode}).",
                    ),
                )
        except Exception as exc:
            self._ui_queue.put(("output", f"\nError: {exc}\n"))
            self._ui_queue.put(("status", f"Error: {label} failed: {exc}"))
        finally:
            self._ui_queue.put(("release",))

    def _release_button(self) -> None:
        if self._active_button is not None:
            self._active_button.configure(state=tk.NORMAL)
        self._active_button = None
        self._running = False


def main() -> None:
    root = tk.Tk()
    MediaExplorerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
