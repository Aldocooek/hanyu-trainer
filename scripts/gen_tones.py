"""Male-voice audio for the tone-pair drill (high-variability training).

Second talker (zh-CN-YunxiNeural, natural speed) for disyllabic words with two
clean tones 1-4. App falls back to Xiaoxiao file, then device TTS.
Usage:  python3 scripts/gen_tones.py
Output: audio/m_<id>.mp3
"""
import asyncio
import os
import re

import edge_tts

VOICE = "zh-CN-YunxiNeural"
OUT = "audio"
T1 = set("āēīōūǖĀĒĪŌŪǕ")
T2 = set("áéíóúǘÁÉÍÓÚǗ")
T3 = set("ǎěǐǒǔǚǍĚǏǑǓǙ")
T4 = set("àèìòùǜÀÈÌÒÙǛ")
TALL = T1 | T2 | T3 | T4


def syl_tone(s):
    c = set(s)
    if c & T1:
        return 1
    if c & T2:
        return 2
    if c & T3:
        return 3
    if c & T4:
        return 4
    return 0


def tone_marks(py):
    """Tones in order, one per toned syllable (pinyin has no spaces in our data)."""
    out = []
    for ch in py:
        t = syl_tone(ch)
        if t:
            out.append(t)
    return out


async def main():
    words = []
    for fn in ["words.js", "words_hsk2.js"]:
        if not os.path.exists(fn):
            continue
        src = open(fn, encoding="utf-8").read()
        words += re.findall(r'\{id:(\d+),hz:"([^"]+)",py:"([^"]+)"', src)
    cands = [(i, h, p) for i, h, p in words
             if len(h) == 2 and len(tone_marks(p)) == 2]
    print("candidates:", len(cands))
    ok = skip = fail = 0
    for wid, hz, _ in cands:
        path = f"{OUT}/m_{wid}.mp3"
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            skip += 1
            continue
        try:
            await edge_tts.Communicate(hz, VOICE).save(path)
            ok += 1
        except Exception as e:  # noqa: BLE001
            fail += 1
            print("FAIL", wid, hz, repr(e)[:120])
    print(f"done: {ok} generated, {skip} skipped, {fail} failed")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    asyncio.run(main())
