"""Build Anki .apkg deck with bundled audio (reusable for HSK 2+).

Reads words.js (level 1) or words_hskN.js + audio/w{id}.mp3.
Usage:  python3 scripts/build_apkg.py [1|2]   (default 1)
Requires: pip install genanki
"""
import sys

import genanki

LVL = sys.argv[1] if len(sys.argv) > 1 else "1"
SRC = "words.js" if LVL == "1" else f"words_hsk{LVL}.js"
OUT = f"hanyu_hsk{LVL}_audio.apkg"
DECK_ID = 2059400110 if LVL == "1" else 2059400110 + int(LVL)
DECK_NAME = f"Hanyu HSK {LVL} (cesky) 🔊"
import re

import genanki

CSS = ".card{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;text-align:center;}"
MODEL = genanki.Model(
    1607392319,
    "Hanyu HSK CZ",
    fields=[{"name": "Hanzi"}, {"name": "Pinyin"}, {"name": "Czech"},
            {"name": "Category"}, {"name": "Audio"}],
    templates=[{
        "name": "Znak -> vyznam",
        "qfmt": '<div style="font-size:64px">{{Hanzi}}</div>{{Audio}}'
                '<div style="color:#888;font-size:13px">{{Category}}</div>',
        "afmt": '{{FrontSide}}<hr><div style="font-size:24px;color:#c0392b">{{Pinyin}}</div>'
                '<div style="font-size:22px">{{Czech}}</div>',
    }],
    css=CSS,
)
DECK = genanki.Deck(DECK_ID, DECK_NAME)


def main():
    src = open(SRC, encoding="utf-8").read()
    items = re.findall(
        r'\{id:(\d+),hz:"([^"]+)",py:"([^"]+)",cz:"([^"]+)",cat:"([^"]+)"(?:,hsk:\d+)?\}', src)
    media = []
    notes = []
    for wid, hz, py, cz, cat in items:
        tag = f"hanyu_w{wid}.mp3"
        notes.append((wid, hz, py, cz, cat, tag))
    import os
    import shutil
    os.makedirs("audio_anki", exist_ok=True)
    mapped = []
    for wid, hz, py, cz, cat, tag in notes:
        dst = f"audio_anki/{tag}"
        if not os.path.exists(dst):
            shutil.copy(f"audio/w{wid}.mp3", dst)
        mapped.append(dst)
        DECK.add_note(genanki.Note(
            model=MODEL,
            fields=[hz, py, cz, cat, f"[sound:{tag}]"],
            guid=f"hanyu{LVL}-{wid}"))
    genanki.Package(DECK, media_files=mapped).write_to_file(OUT)
    print(f"level {LVL}: notes: {len(items)}, media: {len(mapped)}, out: {OUT}")


if __name__ == "__main__":
    main()
