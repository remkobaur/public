#!/usr/bin/env python3
"""Copy specific folders from one local git repo to another and commit.

Usage examples:
  python _Tools/copy_folders_between_repos.py \
    --source C:/path/to/source_repo \
    --dest C:/path/to/dest_repo \
    --folders folderA folderB/subdir \
    --commit-message "Sync folders" \
    --force

This script copies folders (relative to the source repo root) into the
destination repo, stages changes there and commits. It operates on local
paths only.
"""
from pathlib import Path
import argparse
import shutil
import os
import fnmatch
import subprocess
import sys
from typing import Optional


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


def copy_folder(src: Path, dst: Path, force: bool = False, ignore_patterns=None, ignore_exts=None):
    if not src.exists():
        raise FileNotFoundError(f"Source folder not found: {src}")

    ignore_patterns = ignore_patterns or []
    ignore_exts = set(ignore_exts or [])

    def is_ignored_rel(rel_path: str):
        # normalise to forward slashes for pattern matching
        rp = rel_path.replace('\\', '/')
        for pat in ignore_patterns:
            if fnmatch.fnmatch(rp, pat) or rp.startswith(pat.rstrip('/')):
                return True
        return False

    # If destination exists and force==True, remove it first
    if dst.exists() and force:
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    # Walk source and copy files, honoring ignores
    for root, dirs, files in os.walk(src):
        rel_root = os.path.relpath(root, start=str(src))
        if rel_root == '.' or rel_root == '.\\':
            rel_root = ''
        # filter directories in-place so os.walk skips them
        dirs[:] = [d for d in dirs if not is_ignored_rel(os.path.join(rel_root, d).replace('\\', '/'))]
        target_dir = dst.joinpath(rel_root)
        target_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            rel_file = os.path.join(rel_root, f).replace('\\', '/').lstrip('/')
            if is_ignored_rel(rel_file):
                continue
            if ignore_exts:
                _, ext = os.path.splitext(f)
                if ext in ignore_exts:
                    continue
            src_file = Path(root) / f
            shutil.copy2(src_file, target_dir / f)



def git_commit(dest_repo: Path, message: str, author: Optional[str] = None, git_dry_run: bool = False):
    # Stage changes (use a dry-run add to show what would be added when requested)
    if git_dry_run:
        print("[git dry-run] git add -n -A")
        res = run(["git", "-C", str(dest_repo), "add", "-n", "-A"], check=False, capture=True)
        if res.stdout:
            print(res.stdout)
        if res.stderr:
            print(res.stderr, file=sys.stderr)
        print("[git dry-run] commit skipped")
        return

    run(["git", "-C", str(dest_repo), "add", "-A"]) 
    # Commit
    cmd = ["git", "-C", str(dest_repo), "commit", "-m", message]
    if author:
        cmd.extend(["--author", author])
    # Allow commit to fail gracefully if nothing to commit
    try:
        run(cmd)
    except subprocess.CalledProcessError:
        # git returns exit code 1 if there are no changes to commit
        print("No changes to commit or commit failed.")




def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Copy folders from one repo to another and commit them")
    p.add_argument("--source", required=True, help="Path to source repo root")
    p.add_argument("--dest", required=True, help="Path to destination repo root")
    p.add_argument("--folders", required=True, nargs="+", help="Folders (relative to source root) to copy")
    p.add_argument("--files", nargs="+", help="Files (relative to source root) to copy")
    p.add_argument("--commit-message", default="Update folders from source repo")
    p.add_argument("--author", help="Commit author string e.g. 'Name <email>'")
    p.add_argument("--force", action="store_true", help="Remove destination folder before copying (overwrite)")
    p.add_argument("--no-commit", action="store_true", help="Only copy files, do not run git commit")
    p.add_argument("--branch", help="Optional: checkout branch in destination before applying changes")
    p.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    p.add_argument("--ignore", nargs="*", help="Ignore patterns or relative paths (glob syntax)")
    p.add_argument("--ignore-ext", nargs="*", help="Ignore file extensions, e.g. .py .log or py log")
    p.add_argument("--git-dry-run", action="store_true", help="Show git actions (add/commit) without running them")
    p.add_argument("--commit-dialog", action="store_true", help="Open a small GUI dialog to edit the commit message; prefix '[autoupdate]: ' is enforced")
    return p.parse_args(argv)


def main(argv=None):
    # Accept either an argv list (for CLI-like calls) or a pre-parsed
    # argparse.Namespace so callers can do: args = parse_args(); args.source=...; main(args)
    if isinstance(argv, argparse.Namespace):
        args = argv
    else:
        args = parse_args(argv)
    src_root = Path(args.source).resolve()
    dest_root = Path(args.dest).resolve()

    if not src_root.exists():
        print(f"Source path does not exist: {src_root}")
        sys.exit(2)
    if not dest_root.exists():
        if args.dry_run:
            print(f"[dry-run] Would create destination folder: {dest_root}")
        else:
            print(f"Destination folder not found. Creating: {dest_root}")
            dest_root.mkdir(parents=True, exist_ok=True)
            
    # Optional: checkout branch in dest
    if args.branch:
        if args.dry_run:
            print(f"[dry-run] git -C {dest_root} checkout {args.branch}")
        else:
            run(["git", "-C", str(dest_root), "checkout", args.branch])

    # Prepare ignore lists
    ignore_patterns = args.ignore or []
    ignore_exts = set()
    if args.ignore_ext:
        for ex in args.ignore_ext:
            ex = ex if ex.startswith('.') else '.' + ex
            ignore_exts.add(ex)

    for folder in args.folders:
        src_folder = src_root.joinpath(folder)
        dest_folder = dest_root.joinpath(folder)
        print(f"Copying {src_folder} -> {dest_folder}")
        if args.dry_run:
            continue
        try:
            copy_folder(src_folder, dest_folder, force=args.force, ignore_patterns=ignore_patterns, ignore_exts=ignore_exts)
        except Exception as e:
            print(f"Failed to copy {folder}: {e}", file=sys.stderr)
            sys.exit(1)

    # Copy individual files if provided
    if getattr(args, "files", None):
        for file_rel in args.files:
            src_file = src_root.joinpath(file_rel)
            dest_file = dest_root.joinpath(file_rel)
            print(f"Copying file {src_file} -> {dest_file}")
            rel_file = Path(file_rel).as_posix().lstrip('/')
            # ignore by pattern
            skipped = False
            for pat in ignore_patterns:
                if fnmatch.fnmatch(rel_file, pat) or rel_file.startswith(pat.rstrip('/')):
                    print(f"Ignored by pattern: {rel_file}")
                    skipped = True
                    break
            if skipped:
                continue
            # ignore by extension
            if ignore_exts:
                _, ext = os.path.splitext(file_rel)
                if ext and ext in ignore_exts:
                    print(f"Ignored by extension: {rel_file}")
                    continue
            if args.dry_run:
                continue
            if not src_file.exists():
                print(f"Source file not found: {src_file}", file=sys.stderr)
                sys.exit(1)
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            if dest_file.exists():
                if args.force:
                    if dest_file.is_dir():
                        shutil.rmtree(dest_file)
                    else:
                        dest_file.unlink()
            shutil.copy2(src_file, dest_file)

    if args.no_commit:
        print("Files copied; skipping git commit ( --no-commit ).")
        return

    if args.dry_run:
        print("Dry-run enabled; no git actions performed.")
        return

    # Optionally open GUI to edit commit message
    commit_msg = args.commit_message
    if getattr(args, 'commit_dialog', False):
        commit_msg = get_commit_message_from_dialog(commit_msg)
        if commit_msg is None:
            print("Commit cancelled by user; skipping git commit.")
            return

    try:
        git_commit(dest_root, commit_msg, args.author, git_dry_run=getattr(args, 'git_dry_run', False))
    except Exception as e:
        print(f"Git commit failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Build a Namespace directly so argparse isn't invoked for required CLI args
    args = argparse.Namespace(
        source=Path(r"D:\Git\Craft-Projects").resolve(),
        dest=Path(r"D:\Git\Public\Craft-Projects").resolve(),
        folders=["3D_Print", "Electronics", "Wood_Working"],
        files=["README.md"],
        commit_message="Update public folder <Craft-Projects> from source repo",
        author=None,
        ignore=["*.mtl", "*.obj", "*.rsdoc", "*.stl","*.rsdocx"],
        ignore_ext=["mtl", "obj", "rsdoc", "stl","rsdocx"],
        force=False,
        no_commit=False,
        branch=None,
        dry_run=False,
        git_dry_run=False,
        commit_dialog=True,
    )
    main(args)
