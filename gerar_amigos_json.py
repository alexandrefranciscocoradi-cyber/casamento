#!/usr/bin/env python3
"""Gera amigos.json com todas as imagens de Fotos/Amigos/ (ordem alfabética)."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FOLDER = BASE / "Fotos" / "Amigos"
OUT = BASE / "amigos.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

files = sorted(
    str(f.relative_to(BASE)).replace("\\", "/")
    for f in FOLDER.iterdir()
    if f.is_file() and f.suffix.lower() in EXTS
)

OUT.write_text(json.dumps(files, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"amigos.json gerado com {len(files)} imagem(ns): {files}")