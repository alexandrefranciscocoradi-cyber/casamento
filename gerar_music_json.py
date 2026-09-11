#!/usr/bin/env python3
"""Gera music.json com todas as músicas de assets/music/ (ordem alfabética)."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FOLDER = BASE / "assets" / "music"
OUT = BASE / "music.json"

files = sorted(
    str(f.relative_to(BASE)).replace("\\", "/")
    for f in FOLDER.iterdir()
    if f.is_file() and f.suffix.lower() in {".mp3", ".ogg", ".m4a", ".wav"}
)

OUT.write_text(json.dumps(files, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"music.json gerado com {len(files)} música(s): {files}")