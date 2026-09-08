# Hanyu Trainer — čínština HSK 1 (171 slov, česky)

Co máš v `chinese-trainer/`:
- `index.html` — web trenér (otevři dvojklikem, nebo hoď na mobil). Zvuk = nahraný neuronový hlas (offline MP3), záloha = hlas zařízení.
- `words.js` — databáze 171 slov (zjednodušené znaky + pinyin s tóny + čeština) + 30 vět na skládání
- `audio/` — 201× MP3 (171 slov + 30 vět), hlas Xiaoxiao, celkem 1,65 MB
- `hanyu_hsk1_audio.apkg` — hotový Anki balíček SE ZVUKEM (doporučeno)
- `hanyu_hsk1_cz.csv` — import do Anki bez zvuku (středník `;`, UTF-8 s BOM)
- `scripts/gen_audio.py` — vygeneruje audio znovu (i pro budoucí HSK 2)
- `scripts/build_apkg.py` — vyrobí .apkg z words.js + audio/
- `scripts/qa_shots.py` — screenshot QA (desktop + mobil, všech 6 záložek)
- `NAVOD.md` — tenhle soubor

## 1) Web trenér (doporučeno na začátek)
1. Otevři `index.html` v Chrome / Safari (desktop i mobil).
2. Záložky:
   - 🃏 **Kartičky:** vidíš znak → 🔊 přehraj → 👁 ukaž pinyin + význam → ✓ Umím / ✕ Ještě ne. Ukládá se ti postup.
   - 🧩 **Spojovačka 4×4:** vlevo čínsky, vpravo česky — přesně Duolingo styl, co jsi chtěl.
   - 🔊 **Poslech:** přehraje slovo, vybíráš ze 4 českých významů. Nemusíš mluvit.
   - 🧱 **Věty:** dostaneš česky „Piju kávu." a klikáním skládáš 我 / 喝 / 咖啡.
   - 🎤 **Výslovnost (beta):** řekneš slovo do mikrofonu, telefon ho ohodnotí — vše on-device, viz sekce 8.
   - 📥 **Anki:** stažení .apkg se zvukem / CSV + seznam všech slov (klik = přehrát).
3. Zvuk: primárně nahrané MP3 (neuronový hlas Xiaoxiao, tempo −10 % pro studenty). Když soubor chybí, záloha = `speechSynthesis` s `zh-CN`. Na iPhonu/Androidu funguje po prvním kliknutí. Nic neinstaluješ, žádný klíč.

Tvoje startovní slova už tam jsou: 我 wǒ (já), 我们 wǒmen (my), 你 nǐ (ty), 咖啡 kāfēi (káva), 妈妈 māma (máma), 爸爸 bàba (táta).

## 2) Anki (open-source flashcards)
Anki: https://apps.ankiweb.net/
- **Android:** AnkiDroid — zdarma v Google Play
- **iPhone:** AnkiMobile — placená (~$25). Zdarma alternativa: AnkiWeb v prohlížeči.
- **PC/Mac:** Anki zdarma.

Nejrychlejší: **`hanyu_hsk1_audio.apkg`** — stáhni, otevři v Anki (PC: dvojklik, Android: otevři soubor → AnkiDroid). Všech 171 karet má zvuk v sobě, nic nenastavuješ.

### Import CSV do mobilu (2 min)
1. CSV si pošli do mobilu (e-mail / Drive) nebo ho stáhni přímo v mobilu ze záložky 📥 Anki.
2. AnkiDroid: `⋮ → Importovat` → vyber `hanyu_hsk1_cz.csv`. PC Anki: `Soubor → Importovat`.
3. Nastav: **Oddělovač: středník (;)**, **Kódování: UTF-8**.
4. Typ: **Basic**. Sloupce: 1 → Přední (znaky), 2+3 → Zadní (pinyin + čeština).
5. Importuj. Uvidíš znak, po otočení pinyin + význam.

Poznámka ke zvuku v Anki: CSV nemá MP3 (balík by měl ~50 MB a řešil by se přes Anki hlas nebo AwesomeTTS plugin). Výslovnost proto trénuj tady v trenéru tlačítkem 🔊 — je to stejných 171 slov.

## 3) Doporučený režim (100–200 slov)
- Den 1–3: jen Kartičky (20 nových denně) + Poslech.
- Den 4+: přidej Spojovačku a 5 vět denně.
- V Anki si nech 20 nových karet / den → 171 slov ≈ 9 dní.
- Pak mi řekni a přidám dalších 100 slov (HSK 2) + víc vět ze slov, co už umíš.

## 4) Spuštění jako mini-server (volitelné)
Dvojklik na `index.html` stačí. Kdybys chtěl URL pro mobil na stejné Wi-Fi:
```
cd chinese-trainer
python3 -m http.server 8000
```
Pak v mobilu otevři `http://TVUJ-PC-IP:8000`.

## 5) Chytrý trénink (v2) — XP, úrovně, slabá slova
- **XP + levely + streak:** každá správná odpověď = XP (kartička 10, spojovačka 5/pár, poslech 10, věta 15). Level = 1 + každých 100 XP. Streak = dny v řadě. Vše v `localStorage`, žádný login.
- **Vážené opakování chyb:** slova, kde chybuješ, se losují častěji (váha 1 + 3× počet chyb). Správnou odpovědí chyba mizí.
- **Úrovně L1 → L3:** 60 → 120 → všech 171 slov. HSK 2 slot je zamčený, dokud nepřidám balík.
- **Filtry kategorií** už nejsou jen v kartičkách, ale i ve spojovačce a poslechu.
- **Reverzní poslech:** tlačítko Směr otočí cvičení (vidíš česky → vybíráš čínsky). Zdvojnásobí variabilitu bez nových dat.
- **Chytřejší nabídky:** špatné možnosti se berou přednostně ze stejné kategorie (těžší, méně náhodné).

## 6) Duolingo klony — co jsem prošel a co jsem si půjčil
Místo instalace těžkých klonů (většina potřebuje Next.js + databázi + login) jsem z nich vytáhl mechaniky do našeho jednoho souboru:
- `sanidhyy/duolingo-clone` (Lingo, 577 ⭐, MIT) — XP/srdíčka/leaderboard. Půjčeno: XP + levely. Bez serveru a loginu.
- `pretzelai/openlingo` (MIT) — 9 typů cvičení včetně matching pairs a listening s TTS. Potvrdilo naše 4 módy + nápady (word bank, fill-in-blank) do budoucna.
- `adwibha/caliche-cards` (Anki-kompatibilní PWA) — Normal/Write/Multiple-choice/Reverse/Match v jednom balíku, chytřejší nabídky z už probraných karet. Půjčeno: reverzní režim + nabídky ze stejné kategorie.
- `YuriiDorosh/Lexora` — SM-2 opakování, level = 1 + floor(sqrt(xp/50)), streak + streak-freeze shop. Půjčeno: streak logika.
- `mr-fox93/next-lang-ai-app`, `jacklim-gif/StudyFriendly` — mastery 0–5, XP v localStorage bez registrace, level každých 100 XP. Půjčeno: náš level vzorec.
- `HelioFernandes404/openflashcards`, `Liozon/OpenFlashcards` — FSRS + TTS, skládání frází, psaní znaků. Nápad na příště: psací režim pro tóny/pinyin.
- HSK postup (ověřeno): HSK 2.0 je HSK 1 = 150 slov, HSK 2 = +150 (dohromady 300), zkouška jen poslech + čtení, pass 120/200. Cca 6–8 týdnů po HSK 1.

## 7) Zvuk: odkud je a jak ho přegenerovat
- Hlas: **Microsoft Edge neuronové TTS, zh-CN-XiaoxiaoNeural** (zdarma, bez klíče, generováno přes open-source `edge-tts`). Osobní studijní použití.
- Lidské nahrávky zdarma existují (Shtooka — rodilá mluvčí z Pekingu, CC licence, ~1000 slov z HSK 1; lidské věty má Tatoeba, CC, 5 800+ mandarínských vět), ale pokrytí našich slov/vět není kompletní a kvalita kolísá — proto jeden konzistentní neuronový hlas + odkaz na Forvo na dopilování.
- Přegenerování: `pip install edge-tts`, pak `python3 scripts/gen_audio.py all` (přeskakuje hotové). Hlas/tempo se mění nahoře ve skriptu.
- .apkg: `pip install genanki`, pak `python3 scripts/build_apkg.py`.

## 8) Výslovnost: co jde on-device a co ne (výzkum)
Požadavek: telefon poslouchá a hodnotí, **data nikam neodejdou**. Verdikt po průzkumu:
- ✅ **JDE: Transformers.js + Whisper tiny v prohlížeči** — `pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny')`, `{language:'chinese'}`. WASM, mikrofon → přepis → skóre, vše lokálně. Výzkum (Kobe Univ. 2026, 31 studentů): hodnocení Whisperu je z ASR systémů **nejblíž učitelům**; menší model je paradoxně citlivější na chyby (Ballier et al. 2024) — pro skórování výhoda. Naše skóre = podíl správně rozpoznaných znaků (LCS), homofona = správně (stejná metoda jako studie).
- ❌ NEJDE ve statické appce: **Montreal Forced Aligner / Kaldi (vč. GOP)** — serverové C++/Python, bez backendu nespustíš. **Web Speech API rozpoznávání** — posílá zvuk Googlu/Applu (porušilo by soukromí). **Azure/Gladia** — cloud + klíče. **„Open Pronounce"** — pod tímhle jménem žádný standardní open-source nástroj neexistuje; nejbližší reálné věci jsou právě MFA/Kaldi-GOP (server).
- Limity bety: tiny je méně přesný než velké modely (úmysl — přísnější učitel), jednotlivé slabiky těžší než věty, 92 % chyb studentů jsou tóny (Whisper je slyší jako jiné znaky — dobře). Tichá místnost + blízko k mikrofonu = nejlepší výsledky. První stažení modelu ~75 MB (pak cache, pak i offline).

## 9) QA: vzhled ověřen v prohlížeči
`python3 scripts/qa_shots.py` — všech 6 záložek na desktopu (1280) i mobilu (390), 0 JS chyb. Nalezen a opraven 1 problém: fixní patička mohla na úzkém mobilu překrývat tlačítka (padding dna 90 → 130 px).
