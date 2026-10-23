#!/usr/bin/env python3
"""Frames portfolio screenshots and clips in the ai-toolkit iPhone frame, store-screenshot style.

  frame_media.py shot  <style.json> <in.jpg> <out.jpg> "<title>" "<subtitle>"
  frame_media.py video <style.json> <in.mp4> <out.mp4> <out-poster.jpg> "<title>" "<subtitle>"
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path.home() / "personal/ai-toolkit/core/skills/store-screenshots"
sys.path.insert(0, str(SKILL / "scripts"))
import frame as F  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

CANVAS = (1206, 2622)
OUT_SHOT_WIDTH = 441
OUT_VIDEO_SIZE = (600, 1304)


def config(style_path):
    cfg = dict(F.DEFAULTS)
    cfg.update(json.loads(Path(style_path).read_text()))
    cfg["devices"] = {"iphone": {"frame": "iphone-17-pro-silver.png", "canvas": list(CANVAS)}}
    return cfg


def layout(cfg, text):
    """Canvas with caption, the resized frame, its screen mask and the device's top-left corner."""
    frame_src = Image.open(F.FRAMES / "iphone-17-pro-silver.png").convert("RGBA")
    block = F.caption_height(cfg, CANVAS, text)
    canvas = F.background(CANVAS, cfg["background"])
    pad = round(CANVAS[1] * 0.055)
    F.caption(ImageDraw.Draw(canvas), cfg, CANVAS, text, pad, paint=True)
    top = pad + block
    max_w, max_h = CANVAS[0] * cfg["device_width"], CANVAS[1] - top - pad
    scale = min(max_w / frame_src.width, max_h / frame_src.height)
    size = (round(frame_src.width * scale), round(frame_src.height * scale))
    frame = frame_src.resize(size, Image.LANCZOS)
    mask, screen_box = F.screen_mask(frame)
    return canvas.convert("RGBA"), frame, mask, screen_box, ((CANVAS[0] - size[0]) // 2, top)


def framed(cfg, text, shot):
    canvas, frame, mask, screen_box, pos = layout(cfg, text)
    device = F.framed_device(shot.convert("RGB"), frame, mask, screen_box)
    canvas.paste(device, pos, device)
    return canvas.convert("RGB")


def shot(style, src, out, title, subtitle):
    cfg = config(style)
    img = framed(cfg, {"title": title, "subtitle": subtitle}, Image.open(src))
    h = round(img.height * OUT_SHOT_WIDTH / img.width)
    img.resize((OUT_SHOT_WIDTH, h), Image.LANCZOS).save(out, "JPEG", quality=80, optimize=True)


def video(style, src, out, poster, title, subtitle):
    cfg = config(style)
    text = {"title": title, "subtitle": subtitle}
    canvas, frame, mask, screen_box, (dx, dy) = layout(cfg, text)
    box = mask.getbbox()
    bx, by, bw, bh = box[0] + dx, box[1] + dy, box[2] - box[0], box[3] - box[1]
    overlay = canvas.copy()
    overlay.paste(frame, (dx, dy), frame)
    hole = Image.new("L", CANVAS, 255)
    hole.paste(0, (dx, dy), mask)
    overlay.putalpha(hole)
    with tempfile.TemporaryDirectory() as tmp:
        over = Path(tmp) / "overlay.png"
        overlay.save(over)
        graph = (f"[0:v]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh}[v];"
                 f"color=c=black:s={CANVAS[0]}x{CANVAS[1]}:r=30[bg];"
                 f"[bg][v]overlay={bx}:{by}:shortest=1[b];[b][1:v]overlay=0:0:shortest=1,"
                 f"scale={OUT_VIDEO_SIZE[0]}:{OUT_VIDEO_SIZE[1]}:flags=lanczos,format=yuv420p")
        duration = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                  check=True, capture_output=True, text=True).stdout.strip()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-t", duration, "-i", str(over),
                        "-filter_complex", graph, "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "27",
                        "-r", "30", "-movflags", "+faststart", "-t", duration, out], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-frames:v", "1", "-q:v", "4", poster], check=True)


if __name__ == "__main__":
    kind, args = sys.argv[1], sys.argv[2:]
    {"shot": shot, "video": video}[kind](*args)
