#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o arquivo estatico story.json usado no GitHub Pages.
Rode apos adicionar/remover pastas ou midias em Story/:
    python gerar_story_json.py
"""
import os
import re
import json
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
STORY_DIR = os.path.join(ROOT, 'Story')
OUT = os.path.join(ROOT, 'story.json')

IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.heic'}
VIDEO_EXT = {'.mp4', '.mov', '.webm', '.m4v', '.avi'}


def natural_key(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]


def build():
    items = []
    if not os.path.isdir(STORY_DIR):
        return items
    for name in sorted(os.listdir(STORY_DIR), key=natural_key):
        folder = os.path.join(STORY_DIR, name)
        if not os.path.isdir(folder):
            continue
        media = []
        for filename in sorted(os.listdir(folder), key=natural_key):
            ext = os.path.splitext(filename)[1].lower()
            if ext in IMAGE_EXT or ext in VIDEO_EXT:
                url = 'Story/%s/%s' % (
                    urllib.parse.quote(name),
                    urllib.parse.quote(filename)
                )
                kind = 'video' if ext in VIDEO_EXT else 'image'
                media.append({'url': url, 'type': kind})
        if media:
            items.append({'name': name, 'media': media})
    return items


def main():
    payload = build()
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print('story.json gerado com %d destaques' % len(payload))


if __name__ == '__main__':
    main()