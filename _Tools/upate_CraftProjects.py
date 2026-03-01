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
import sys

from HelperClasses import GitManager, FileCopier   


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
            GitManager.run(["git", "-C", str(dest_root), "checkout", args.branch])

    # Prepare ignore lists
    ignore_patterns = args.ignore or []
    ignore_exts = set()
    if args.ignore_ext:
        for ex in args.ignore_ext:
            ex = ex if ex.startswith('.') else '.' + ex
            ignore_exts.add(ex)

    copier = FileCopier(ignore_patterns=ignore_patterns, ignore_exts=ignore_exts)

    for folder in args.folders:
        src_folder = src_root.joinpath(folder)
        dest_folder = dest_root.joinpath(folder)
        print(f"Copying {src_folder} -> {dest_folder}")
        if args.dry_run:
            continue
        try:
            copier.copy_folder(src_folder, dest_folder, force=args.force)
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
            if copier.is_ignored_rel(rel_file):
                print(f"Ignored by pattern: {rel_file}")
                continue
            if copier.is_ignored_ext(file_rel):
                print(f"Ignored by extension: {rel_file}")
                continue
            if args.dry_run:
                continue
            try:
                copier.copy_file(src_root, dest_root, file_rel, force=args.force)
            except Exception as e:
                print(f"Failed to copy file {file_rel}: {e}", file=sys.stderr)
                sys.exit(1)

    if args.no_commit:
        print("Files copied; skipping git commit ( --no-commit ).")
        return

    if args.dry_run:
        print("Dry-run enabled; no git actions performed.")
        return

    # Optionally open GUI to edit commit message
    commit_msg = args.commit_message
    if getattr(args, 'commit_dialog', False):
        commit_msg = GitManager.get_commit_message_from_dialog(commit_msg)
        if commit_msg is None:
            print("Commit cancelled by user; skipping git commit.")
            return

    try:
        GitManager.git_commit(dest_root, commit_msg, args.author, git_dry_run=getattr(args, 'git_dry_run', False))
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
