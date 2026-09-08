"""Build Anki .apkg deck with bundled audio (reusable for HSK 2+).

Reads words.js + audio/w{id}.mp3, writes hanyu_hsk1_audio.apkg.
Usage:  python3 scripts/build_apkg.py
Requires: pip install genanki
"""
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
DECK = genanki.Deck(2059400110, "Hanyu HSK 1 (cesky) 🔊")


def main():
    src = open("words.js", encoding="utf-8").read()
    items = re.findall(
        r'\{id:(\d+),hz:"([^"]+)",py:"([^"]+)",cz:"([^"]+)",cat:"([^"]+)"\}', src)
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
            guid=f"hanyu1-{wid}"))
    genanki.Package(DECK, media_files=mapped).write_to_file("hanyu_hsk1_audio.apkg")
    print(f"notes: {len(items)}, media: {len(mapped)}")


if __name__ == "__main__":
    main()
