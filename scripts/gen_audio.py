"""Generate bundled TTS audio for Hanyu Trainer (reusable for HSK 2+).

Voice: Microsoft Edge neural zh-CN-XiaoxiaoNeural (free, no key), rate -10% for learners.
Reads words.js + words_hskN.js, writes audio/w{id}.mp3 (words) + audio/s{idx}.mp3
(sentences, idx = merged SENTENCES order — APPEND ONLY, never reorder).
Idempotent: skips files that already exist.

Usage:
    python3 scripts/gen_audio.py [words|sents|all]
"""
import asyncio
import os
import re
import sys

import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-10%"
OUT = "audio"
DATA_FILES = ["words.js", "words_hsk2.js"]


async def gen(text, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return "skip"
    await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
    return "ok"


async def main(which):
    words, sents = [], []
    for fn in DATA_FILES:
        if not os.path.exists(fn):
            continue
        src = open(fn, encoding="utf-8").read()
        words += re.findall(r'\{id:(\d+),hz:"([^"]+)"', src)
        sents += re.findall(r'full:"([^"]+)"', src)
    tasks = []
    if which in ("words", "all"):
        tasks += [(f"w{wid}", hz, f"{OUT}/w{wid}.mp3") for wid, hz in words]
    if which in ("sents", "all"):
        tasks += [(f"s{i}", full, f"{OUT}/s{i}.mp3") for i, full in enumerate(sents)]
    ok = skip = fail = 0
    for tag, text, path in tasks:
        try:
            r = await gen(text, path)
            ok += r == "ok"
            skip += r == "skip"
        except Exception as e:  # noqa: BLE001 - log and continue
            fail += 1
            print("FAIL", tag, text, repr(e)[:120])
    print(f"done: {ok} generated, {skip} skipped, {fail} failed / {len(tasks)} tasks")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "all"))
