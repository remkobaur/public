from pathlib import Path
import shutil
import os
import fnmatch
import subprocess
import sys
from typing import Optional


class GitManager:
    @staticmethod
    def get_commit_message_from_dialog(default_msg: str) -> Optional[str]:
        """Show a small tkinter window for multiline commit message input.

        Returns the message string or None if cancelled. Ensures prefix.
        The layout uses grid so the buttons remain visible; a minimum window
        height is enforced to avoid the Text widget hiding the buttons.
        """
        try:
            import tkinter as tk
        except Exception:
            print("Tkinter not available; falling back to default commit message.")
            return default_msg

        prefix = "[autoupdate] [Crafting Projects]: "
        initial = default_msg or prefix
        if not initial.startswith(prefix):
            initial = initial

        root = tk.Tk()
        root.title("Commit message")
        root.minsize(480, 200)

        # Grid layout: label (row0), text (row1, expands), buttons (row2)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        tk.Label(root, text="Edit commit message (prefix '[autoupdate] [Crafting Projects]: ' will be enforced):").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 0))
        text = tk.Text(root, wrap="word", height=8)
        text.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        text.insert("1.0", initial)

        result = {"value": None}

        def do_commit():
            val = text.get("1.0", "end").strip()
            if not val.startswith(prefix):
                val = prefix + val
            result["value"] = val
            root.destroy()

        def do_cancel():
            result["value"] = None
            root.destroy()

        btn_frame = tk.Frame(root)
        btn_frame.grid(row=2, column=0, sticky="e", padx=8, pady=(0, 8))
        tk.Button(btn_frame, text="Commit", width=10, command=do_commit).pack(side="right", padx=(0, 8))
        tk.Button(btn_frame, text="Cancel", width=10, command=do_cancel).pack(side="right")

        root.mainloop()
        return result["value"]

    @staticmethod
    def run(cmd, check=True, capture=False):
        result = subprocess.run(cmd, shell=False, check=False, capture_output=capture, text=True)
        if check and result.returncode != 0:
            print(f"Command failed: {' '.join(cmd)}")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            raise subprocess.CalledProcessError(result.returncode, cmd)
        return result

    @staticmethod
    def git_commit(dest_repo: Path, message: str, author: Optional[str] = None, git_dry_run: bool = False):
        # Stage changes (use a dry-run add to show what would be added when requested)
        if git_dry_run:
            print("[git dry-run] git add -n -A")
            res = GitManager.run(["git", "-C", str(dest_repo), "add", "-n", "-A"], check=False, capture=True)
            if res.stdout:
                print(res.stdout)
            if res.stderr:
                print(res.stderr, file=sys.stderr)
            print("[git dry-run] commit skipped")
            return

        GitManager.run(["git", "-C", str(dest_repo), "add", "-A"])
        # Commit
        cmd = ["git", "-C", str(dest_repo), "commit", "-m", message]
        if author:
            cmd.extend(["--author", author])
        # Allow commit to fail gracefully if nothing to commit
        try:
            GitManager.run(cmd)
        except subprocess.CalledProcessError:
            # git returns exit code 1 if there are no changes to commit
            print("No changes to commit or commit failed.")


class FileCopier:
    def __init__(self, ignore_patterns=None, ignore_exts=None):
        self.ignore_patterns = ignore_patterns or []
        self.ignore_exts = set(ignore_exts or [])

    def is_ignored_rel(self, rel_path: str) -> bool:
        rp = rel_path.replace('\\', '/')
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(rp, pattern) or rp.startswith(pattern.rstrip('/')):
                return True
        return False

    def is_ignored_ext(self, file_name: str) -> bool:
        if not self.ignore_exts:
            return False
        _, ext = os.path.splitext(file_name)
        return bool(ext and ext in self.ignore_exts)

    def copy_folder(self, src: Path, dst: Path, force: bool = False):
        if not src.exists():
            raise FileNotFoundError(f"Source folder not found: {src}")

        if dst.exists() and force:
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()

        for root, dirs, files in os.walk(src):
            rel_root = os.path.relpath(root, start=str(src))
            if rel_root in {'.', '.\\'}:
                rel_root = ''

            dirs[:] = [
                directory
                for directory in dirs
                if not self.is_ignored_rel(os.path.join(rel_root, directory).replace('\\', '/'))
            ]

            target_dir = dst.joinpath(rel_root)
            target_dir.mkdir(parents=True, exist_ok=True)

            for file_name in files:
                rel_file = os.path.join(rel_root, file_name).replace('\\', '/').lstrip('/')
                if self.is_ignored_rel(rel_file):
                    continue
                if self.is_ignored_ext(file_name):
                    continue
                src_file = Path(root) / file_name
                shutil.copy2(src_file, target_dir / file_name)

    def copy_file(self, src_root: Path, dest_root: Path, file_rel: str, force: bool = False):
        rel_file = Path(file_rel).as_posix().lstrip('/')
        if self.is_ignored_rel(rel_file):
            print(f"Ignored by pattern: {rel_file}")
            return
        if self.is_ignored_ext(file_rel):
            print(f"Ignored by extension: {rel_file}")
            return

        src_file = src_root.joinpath(file_rel)
        dest_file = dest_root.joinpath(file_rel)

        if not src_file.exists():
            raise FileNotFoundError(f"Source file not found: {src_file}")

        dest_file.parent.mkdir(parents=True, exist_ok=True)
        if dest_file.exists() and force:
            if dest_file.is_dir():
                shutil.rmtree(dest_file)
            else:
                dest_file.unlink()

        shutil.copy2(src_file, dest_file)
        
    def copy_structure_with_extensions(self,src, dst, extensions, skip_folders=None):
        src = os.path.abspath(src)
        dst = os.path.abspath(dst)
        if skip_folders is None:
            skip_folders = []
        skip_folders = [os.path.normpath(f) for f in skip_folders]
        ignored_exts = [ext.lower() for ext in extensions]
        non_meta_ignored_exts = [ext for ext in ignored_exts if ext != '.meta']
        for root, dirs, files in os.walk(src):
            # Remove directories to skip from traversal
            dirs[:] = [d for d in dirs if os.path.relpath(os.path.join(root, d), src) not in skip_folders and d not in skip_folders]

            # Find files in this folder that do NOT match the ignored extensions (excluding .meta for now)
            matching_files = [
                file for file in files
                if not file.lower().endswith('.meta') and not any(file.lower().endswith(ext) for ext in non_meta_ignored_exts)
            ]

            # Prepare set of base names for .cs files that are not ignored
            cs_basenames = set(
                os.path.splitext(file)[0]
                for file in files
                if file.lower().endswith('.cs') and not any(file.lower().endswith(ext) for ext in non_meta_ignored_exts)
            )

            # Determine which subfolders would be created (i.e., contain matching files)
            subfolders_to_create = set()
            for d in dirs:
                subfolder_path = os.path.join(root, d)
                subfolder_files = []
                try:
                    subfolder_files = os.listdir(subfolder_path)
                except Exception:
                    pass
                if any(
                    not f.lower().endswith('.meta') and not any(f.lower().endswith(ext) for ext in non_meta_ignored_exts)
                    for f in subfolder_files
                ):
                    subfolders_to_create.add(d)

            # Find .meta files that match .cs files or subfolders that would be created
            meta_files = []
            if '.meta' not in ignored_exts:
                for file in files:
                    if file.lower().endswith('.meta'):
                        base = os.path.splitext(file)[0]
                        if base in cs_basenames or base in subfolders_to_create:
                            meta_files.append(file)

            # Only create the folder if there are files to copy
            if matching_files or meta_files:
                rel_path = os.path.relpath(root, src)
                dst_dir = os.path.join(dst, rel_path)
                os.makedirs(dst_dir, exist_ok=True)
                for file in matching_files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst_dir, file)
                    shutil.copy2(src_file, dst_file)
                for file in meta_files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst_dir, file)
                    shutil.copy2(src_file, dst_file)
                    
        print(f"Copied folder structure from {src} to {dst}. Ignored extensions: {', '.join(extensions)}. Skipped folders: {', '.join(skip_folders)}")

