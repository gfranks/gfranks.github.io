#!/usr/bin/env python3
"""Puts each app's raw screens in the ai-toolkit iPhone frame for the phones on the site.

  python3 -I tools/frame_screens.py [app ...]

Reads each app's "screens" from content/apps.json and the raw screenshots from SOURCES, and writes
assets/devices/<app>/<file>.webp: the framed phone on a transparent background, HEIGHT px tall. Apps with
"screenStyle": "store" use their finished App Store images instead, unframed and as tall.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = Path.home() / "personal/ai-toolkit/core/skills/store-screenshots"
sys.path.insert(0, str(SKILL / "scripts"))
import frame as F  # noqa: E402
from PIL import Image, features  # noqa: E402

HEIGHT = 1100
PERSONAL = Path.home() / "personal"
SOURCES = {
    "arkive": PERSONAL / "Arkive/store-screenshots/input/iphone",
    "pyllar": PERSONAL / "Pyllar/store-screenshots/input/iphone",
    "tyde": PERSONAL / "Tyde/AppStoreScreenshots/raw",
    "whispercourt": PERSONAL / "WhisperCourt/store-screenshots/input/iphone",
    "candidly": PERSONAL / "Candidly/store-screenshots/output/iphone",
}


def save_webp(image, path):
    if features.check("webp"):
        image.save(path, "WEBP", quality=82, method=6)
        return
    if not shutil.which("cwebp"):
        raise SystemExit("Needs Pillow with WebP support or cwebp (brew install webp).")
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "device.png"
        image.save(png)
        subprocess.run(["cwebp", "-quiet", "-q", "82", "-alpha_q", "90", "-m", "6", str(png), "-o", str(path)], check=True)


def main(ids):
    apps = json.loads((ROOT / "content" / "apps.json").read_text())["apps"]
    frame = Image.open(F.FRAMES / "iphone-17-pro-silver.png").convert("RGBA")
    mask, screen_box = F.screen_mask(frame)
    size = (round(frame.width * HEIGHT / frame.height), HEIGHT)
    for app in apps:
        if ids and app["id"] not in ids:
            continue
        out = ROOT / "assets" / "devices" / app["id"]
        out.mkdir(parents=True, exist_ok=True)
        for screen in app["screens"]:
            shot = Image.open(SOURCES[app["id"]] / f'{screen["file"]}.png').convert("RGB")
            if app.get("screenStyle") == "store":
                device = shot.resize((round(shot.width * HEIGHT / shot.height), HEIGHT), Image.LANCZOS)
            else:
                device = F.framed_device(shot, frame, mask, screen_box).resize(size, Image.LANCZOS)
            save_webp(device, out / f'{screen["file"]}.webp')
            print(f'{app["id"]}/{screen["file"]}.webp')


if __name__ == "__main__":
    main(sys.argv[1:])
