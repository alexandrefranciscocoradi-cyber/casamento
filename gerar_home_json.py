#!/usr/bin/env python3
"""Gera home.json com todas as imagens de Fotos/home/ (ordem alfabética)."""

import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
FOLDER = BASE / "Fotos" / "home"
OUT = BASE / "home.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

files = sorted(
    str(f.relative_to(BASE)).replace("\\", "/")
    for f in FOLDER.iterdir()
    if f.is_file() and f.suffix.lower() in EXTS
)

OUT.write_text(json.dumps(files, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"home.json gerado com {len(files)} imagem(ns): {files}")
