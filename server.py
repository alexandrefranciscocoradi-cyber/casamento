#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor do site do casamento.
Serve os arquivos estáticos e um endpoint /api/story que lista
automaticamente as pastas de destaques (Story/<nome do destaque>)
e suas medias (imagens e videos), sem nomes fixos em codigo.
"""
import os
import re
import json
import sys
import mimetypes
import http.server
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
STORY_DIR = os.path.join(ROOT, 'Story')
PORT = 8080

IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.heic'}
VIDEO_EXT = {'.mp4', '.mov', '.webm', '.m4v', '.avi'}


def natural_key(name):
    """Ordena '2' antes de '10' (ordem natural)."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.rstrip('/') == '/api/story':
            return self._serve_story()
        return super().do_GET()

    def _serve_story(self):
        payload = self._build_story()
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _build_story(self):
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

    def guess_type(self, path):
        mime, _ = mimetypes.guess_type(path)
        if path.lower().endswith('.mov'):
            return 'video/quicktime'
        return mime or 'application/octet-stream'


if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
    server.daemon_threads = True
    print('Servidor rodando em http://localhost:%d' % PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass