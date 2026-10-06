"""Keep the hosted demo apps awake.

  python scripts/keep_alive.py            # check everything
  python scripts/keep_alive.py --mode http
  python scripts/keep_alive.py --mode browser

http    : plain GET with retries (enough for Render, whose free tier sleeps
          after ~15 min without traffic; a cold start can take ~60 s).
browser : headless Chromium visit via Playwright (Streamlit Community Cloud
          only counts real browser sessions, and shows a wake-up button
          after ~12 h of no visitors).

Add an app by adding one line to APPS.
"""
import argparse
import sys
import time
import urllib.request

APPS = [
    # (name, url, mode)
    ("Next Restaurant (Render)", "https://next-restaurant.onrender.com/", "http"),
    ("Newsvendor (Streamlit)", "https://newsvendorproblem.streamlit.app/", "browser"),
]

HTTP_TIMEOUT = 90   # seconds per attempt (covers a Render cold start)
HTTP_TRIES = 3
WAKE_BUTTON = "get this app back up"


def check_http(name, url):
    for attempt in range(1, HTTP_TRIES + 1):
        start = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "keep-alive-check"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                ok = r.status == 200
                print(f"[{'OK' if ok else 'FAIL'}] {name}: HTTP {r.status} in {time.time() - start:.1f}s")
                if ok:
                    return True
        except Exception as e:  # noqa: BLE001 - report any failure and retry
            print(f"[WARN] {name}: attempt {attempt}/{HTTP_TRIES} failed after {time.time() - start:.1f}s: {e}")
        time.sleep(10)
    print(f"[FAIL] {name}: no healthy response")
    return False


def check_browser(name, url):
    from playwright.sync_api import TimeoutError as PWTimeout, sync_playwright

    start = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            button = page.get_by_role("button", name=WAKE_BUTTON, exact=False)
            try:
                button.wait_for(state="visible", timeout=15_000)
                print(f"[INFO] {name}: app was asleep, clicking wake-up button")
                button.click()
            except PWTimeout:
                pass  # already awake
            page.wait_for_selector('iframe[title="streamlitApp"], [data-testid="stApp"]',
                                   state="attached", timeout=120_000)
            print(f"[OK] {name}: app is up ({time.time() - start:.1f}s)")
            return True
        except Exception as e:  # noqa: BLE001
            print(f"[FAIL] {name}: {e}")
            return False
        finally:
            browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["all", "http", "browser"], default="all")
    args = ap.parse_args()
    results = []
    for name, url, mode in APPS:
        if args.mode not in ("all", mode):
            continue
        results.append((check_http if mode == "http" else check_browser)(name, url))
    return 0 if results and all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
