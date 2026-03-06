#!/usr/bin/env python3
"""Generate Config.json from subfolders and sound file names."""

from __future__ import annotations

import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Extend this set if you add other audio file types.
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}


def build_config(root: Path) -> dict:
    sounds = []

    for subdir in sorted(p for p in root.iterdir() if p.is_dir()):
        files = sorted(
            f.name
            for f in subdir.iterdir()
            if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
        )
        if not files:
            continue

        sounds.append(
            {
                "Subfolder": subdir.name,
                "ID":0,
                "Sounds": files,
            }
        )

    return {"Sounds": sounds}


def main(rootPath = None) -> None:
    if not rootPath:
        rootPath = os.path.join(ROOT,'..',"Sounds")
    root_path = Path(rootPath)
    config_path = root_path / "Config.json"
    config = build_config(root_path)
    config_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {config_path}")
    print(f"Subfolders included: {len(config['Sounds'])}")


if __name__ == "__main__":
    rootPath = os.path.join(ROOT,'..',"Sounds")
    main(rootPath)
