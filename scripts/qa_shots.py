"""Visual QA screenshots for Hanyu Trainer (reusable).

Serves the trainer dir over http, captures every tab on desktop + mobile.
Usage:  python3 scripts/qa_shots.py
Output: qa/<viewport>_<tab>.png
"""
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import sync_playwright

PORT = 8129
NAV_TABS = ["home", "cards", "mix", "fix"]
MENU_TABS = ["tones", "match", "listen", "sent", "speak", "anki", "set"]
VIEWPORTS = {
    "desktop": {"width": 1280, "height": 800},
    "mobile": {"width": 390, "height": 844},
}


def main():
    srv = ThreadingHTTPServer(
        ("127.0.0.1", PORT),
        partial(SimpleHTTPRequestHandler, directory="."))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    import os
    os.makedirs("qa", exist_ok=True)
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for vp, size in VIEWPORTS.items():
            pg = b.new_page(viewport=size)
            msgs = []
            pg.on("pageerror", lambda e: msgs.append(str(e)))
            pg.goto(f"http://127.0.0.1:{PORT}/index.html")
            pg.wait_for_timeout(1200)
            for tab in NAV_TABS:
                pg.click(f'#tabbar button[data-tab="{tab}"]')
                pg.wait_for_timeout(500)
                pg.screenshot(path=f"qa/{vp}_{tab}.png", full_page=True)
                print("shot", f"qa/{vp}_{tab}.png")
            for tab in MENU_TABS:
                pg.click('#moreBtn')
                pg.wait_for_timeout(300)
                pg.click(f'#moreMenu .sheet button[data-tab="{tab}"]')
                pg.wait_for_timeout(500)
                pg.screenshot(path=f"qa/{vp}_{tab}.png", full_page=True)
                print("shot", f"qa/{vp}_{tab}.png")
            if msgs:
                errors.append((vp, msgs))
            pg.close()
        b.close()
    srv.shutdown()
    print("JS pageerrors:", errors if errors else "NONE")


if __name__ == "__main__":
    main()
