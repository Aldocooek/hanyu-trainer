"""Generate PWA icons for Hanyu Trainer (reusable).

Orange-red gradient rounded square + white hanzi. Probes system CJK fonts.
Usage:  python3 scripts/make_icons.py
Output: icons/icon-512.png, icon-192.png, icon-180.png, icon-maskable.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

FONTS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
]


def find_font(size):
    for path in FONTS:
        if not os.path.exists(path):
            continue
        for idx in range(6):
            try:
                f = ImageFont.truetype(path, size, index=idx)
                bb = f.getbbox("汉")
                if bb and bb[2] - bb[0] > size * 0.5:
                    print("font:", path, "index", idx)
                    return f
            except Exception:
                continue
    raise SystemExit("no CJK font found")


def gradient(size):
    img = Image.new("RGB", (size, size))
    top, bot = (255, 75, 75), (255, 122, 61)
    for y in range(size):
        t = y / max(size - 1, 1)
        img.paste(tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)),
                  (0, y, size, y + 1))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size, size],
                                           radius=int(size * 0.225), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, mask=mask)
    return out


def make(size, char_scale, name):
    img = gradient(size).convert("RGBA")
    d = ImageDraw.Draw(img)
    f = find_font(int(size * char_scale))
    bb = d.textbbox((0, 0), "汉", font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - w) / 2 - bb[0], (size - h) / 2 - bb[1]),
           "汉", font=f, fill=(255, 255, 255, 255))
    img.convert("RGB").save(name)
    print("wrote", name)


if __name__ == "__main__":
    os.makedirs("icons", exist_ok=True)
    make(512, 0.62, "icons/icon-512.png")
    make(192, 0.62, "icons/icon-192.png")
    make(180, 0.62, "icons/icon-180.png")
    make(512, 0.48, "icons/icon-maskable.png")
