"""Functional QA for Hanyu Trainer: headless Chromium clicks through the app
and asserts real behavior (not just screenshots).

Usage:  python3 scripts/qa_func.py
Exit code 0 = all green.
"""
import re
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import sync_playwright

PORT = 8135
CJK = re.compile(r"[\u4e00-\u9fff]")
PASS, FAIL = [], []


def check(name, cond, extra=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name, extra)


def main():
    srv = ThreadingHTTPServer(
        ("127.0.0.1", PORT),
        partial(SimpleHTTPRequestHandler, directory="."))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(f"http://127.0.0.1:{PORT}/index.html")
        pg.wait_for_timeout(1000)

        # 1. version badge + default state
        check("footer shows v6", "v6" in (pg.text_content("footer") or ""))
        check("stats HSK1 scope", "HSK 1" in pg.text_content("#stats")
              and "/ 171" in pg.text_content("#stats"))

        # 2. flashcards: pinyin-first, nothing revealed, no characters
        pg.click('#tabbar button[data-tab="cards"]')
        hz_html = pg.inner_html("#c-hz")
        check("cards: no characters shown initially", not CJK.search(hz_html))
        check("cards: pinyin shown", bool(pg.text_content("#c-hz").strip()))
        check("cards: meaning hidden", pg.text_content("#c-cz").strip() in ("?", ""))
        pg.click("#c-show")
        check("cards: meaning revealed after Ukázat",
              len(pg.text_content("#c-cz").strip()) > 1)
        pg.click("#c-yes")
        check("cards: XP gained", "⚡ 10 XP" in pg.text_content("#stats"))

        # 3. pool hint visible + level changes pool
        check("cards: pool hint shows count",
              "Balík:" in pg.text_content("#c-pool"))
        pg.select_option("#c-level", "L1")
        pg.wait_for_timeout(300)
        check("cards: L1 shrinks pool",
              "Balík: 57 slov" in pg.text_content("#c-pool"))
        pg.select_option("#c-level", "L3")

        # 4. mix drill: 2 rounds
        pg.click('#tabbar button[data-tab="mix"]')
        pg.click("#d-start")
        pg.wait_for_timeout(600)
        check("mix: round 1/12", "Kolo 1 / 12" in pg.text_content("#d-pos"))

        # 5. tones drill: 4 options, advances
        pg.click("#moreBtn")
        pg.wait_for_timeout(200)
        pg.click('#moreMenu .sheet button[data-tab="tones"]')
        pg.click("#t-start")
        pg.wait_for_timeout(600)
        check("tones: 4 options",
              pg.locator("#t-opts button").count() == 4)
        check("tones: pair label", "pár 1–3" in pg.text_content("#t-pos"))
        pg.locator("#t-opts button").nth(1).click()
        pg.wait_for_timeout(3200)
        check("tones: advances to round 2",
              "Kolo 2 / 12" in pg.text_content("#t-pos"))

        # 6. dictionary: search filters, row has no characters, tap toggles known
        pg.click('#tabbar button[data-tab="dict"]')
        pg.wait_for_timeout(300)
        rows = pg.locator("#dlist .drow").count()
        check("dict: rows rendered", rows > 100, f"({rows})")
        check("dict: zero characters in list",
              not CJK.search(pg.inner_text("#dlist") or ""))
        pg.fill("#dq", "kafe")
        pg.wait_for_timeout(300)
        n1 = pg.locator("#dlist .drow").count()
        check("dict: search filters", 0 < n1 < rows, f"({n1})")
        pg.fill("#dq", "")
        pg.click('#dhskrow .chip[data-h="2"]')
        pg.wait_for_timeout(300)
        check("dict: HSK2 chip", "138 slov" in pg.text_content("#dcount"))
        pg.click('#dhskrow .chip[data-h="1"]')
        first_btn = pg.locator("#dlist .drow .dbtn").first
        before = first_btn.text_content()
        first_btn.click()
        check("dict: known toggle flips",
              first_btn.text_content() != before)

        # 7. settings: HSK switch changes scope, theme toggles
        pg.click("#moreBtn")
        pg.wait_for_timeout(200)
        pg.click('#moreMenu .sheet button[data-tab="set"]')
        pg.select_option("#s-hsk", "2")
        pg.wait_for_timeout(500)
        check("settings: HSK2 scope 309",
              "/ 309" in pg.text_content("#stats"))
        pg.select_option("#s-hsk", "1")
        pg.select_option("#s-theme", "dark")
        pg.wait_for_timeout(300)
        check("settings: dark theme applies",
              pg.eval_on_selector("html", "e=>e.dataset.theme") == "dark")
        pg.select_option("#s-theme", "system")

        check("no JS pageerrors", not errors, str(errors[:2]))
        b.close()
    srv.shutdown()
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILED:", FAIL)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
