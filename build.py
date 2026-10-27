#!/usr/bin/env python3
"""Builds the offline PWA in docs/ from src/diary.html (the same file is published as the claude.ai artifact)."""
import hashlib, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
body = (ROOT / "src/diary.html").read_text(encoding="utf8")
head = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#19211F">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
html = head + body + "\n</body>\n</html>\n"
out = ROOT / "docs"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(html, encoding="utf8")
for f in ["manifest.webmanifest", "icon-192.png", "icon-512.png"]:
    shutil.copy(ROOT / "pwa" / f, out / f)
version = hashlib.sha256(html.encode()).hexdigest()[:10]
sw = (ROOT / "pwa/sw.js").read_text(encoding="utf8").replace("__VERSION__", version)
(out / "sw.js").write_text(sw, encoding="utf8")
(out / ".nojekyll").write_text("")
print("built docs/ version", version)
