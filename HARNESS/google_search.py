#!/usr/bin/env python3
"""
Google 搜尋（Playwright 無頭 Chromium + 偽裝設定）。
Google 會擋 agent-browser / webwright 預設 Firefox，此腳本為已驗證可用的替代做法。

用法：
    uv run --with playwright python HARNESS/google_search.py "查詢詞"

Chromium 路徑：
    1. 環境變數 CHROMIUM_PATH（指向 chrome 執行檔）
    2. 否則取 ~/.cache/ms-playwright/ 內最新的 chromium-*/chrome-linux64/chrome
    3. 都找不到就交給 Playwright 預設（需先 `npx playwright install chromium`）

遇到異常流量驗證頁（/sorry/）時只回報，不嘗試繞過。
"""

import glob
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0.0.0 Safari/537.36"
)


def find_chromium() -> str | None:
    """Return the Chromium executable path, or None to use Playwright's default."""
    env_path = os.environ.get("CHROMIUM_PATH")
    if env_path:
        return env_path
    pattern = str(Path.home() / ".cache" / "ms-playwright" / "chromium-*" / "chrome-linux64" / "chrome")
    candidates = sorted(glob.glob(pattern))
    return candidates[-1] if candidates else None


def main() -> int:
    if len(sys.argv) < 2:
        print('用法：python google_search.py "查詢詞"', file=sys.stderr)
        return 1
    query = sys.argv[1]

    with sync_playwright() as p:
        launch_args = {
            "headless": True,
            "args": ["--disable-blink-features=AutomationControlled"],
        }
        chromium = find_chromium()
        if chromium:
            launch_args["executable_path"] = chromium
        browser = p.chromium.launch(**launch_args)
        context = browser.new_context(locale="zh-TW", user_agent=USER_AGENT)
        page = context.new_page()
        page.goto(
            "https://www.google.com/search?hl=zh-TW&q=" + query,
            timeout=30000,
        )
        page.wait_for_timeout(2500)

        if "/sorry/" in page.url:
            print("BLOCKED：Google 回傳異常流量驗證頁，未嘗試繞過。請稍後再試或改請使用者提供結果。")
            browser.close()
            return 2

        print(page.url[:80])
        print(page.inner_text("body")[:3000])
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
