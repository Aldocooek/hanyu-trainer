# 🇨🇳 Hanyu Trainer — čínština HSK 1 (česky)

Interaktivní trenér čínštiny: 171 slov HSK 1 (zjednodušené znaky + pinyin s tóny + čeština) + 30 vět na skládání.

**Živá verze:** https://Aldocooek.github.io/hanyu-trainer/

## Módy
- 🏠 Domů (denní cíl 50 XP, streak, rychlé akce)
- ⚡ Rychlý mix (12 kol všeho) + 🩹 Opravna chyb
- 🃏 Kartičky (flashcards s chytrým opakováním chyb)
- 🧩 Spojovačka 4×4 (Duolingo styl)
- 🔊 Poslech — čínština → čeština i obráceně, bez mluvení
- 🧱 Skládačka vět
- 🎤 Výslovnost (beta) — on-device Whisper tiny, nic se nikam neposílá
- 📥 Anki export (`.apkg` se zvukem + CSV) + návod na import

## v3
Hravý Duolingo design (spodní tab bar, tónové barvy pinyinu, světlá/tmavá/systém), instalovatelná PWA (offline, odznak, připomínka streaku), adaptivní animace + confetti, haptika (Android), pomalý zvuk 0.7×, klávesové zkratky na desktopu.

## Chytrý trénink
- ⚡ XP + levely + 🔥 streak (localStorage, žádný login)
- Vážené losování: slova, kde chybuješ, se ukazují častěji
- Úrovně L1 → L3 (60 → 120 → všech 171 slov), HSK 2 v přípravě
- Zvuk zdarma: nahrané MP3 (neuronový hlas Xiaoxiao, 201 souborů, `scripts/gen_audio.py`), záloha = hlas zařízení (Web Speech API, `zh-CN`)

## Spuštění lokálně
Stačí otevřít `index.html` v prohlížeči. Nebo:
```
python3 -m http.server 8000
```

Podrobný návod (Anki import, režim učení) viz `NAVOD.md`.
