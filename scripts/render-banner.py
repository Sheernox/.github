"""Render banner/banner.html to profile/assets/banner.png (2560x800, transparent corners).

Usage: python3 scripts/render-banner.py
Needs the Python playwright package with its Chromium build installed. GitHub shows only
images in a profile README, so the banner ships as a PNG; commit the PNG with any banner edit.
"""
import sys
from pathlib import Path

from playwright.sync_api import Error, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "banner/banner.html"
TARGET = ROOT / "profile/assets/banner.png"


def main() -> int:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 400}, device_scale_factor=2)
            page.goto(SOURCE.as_uri())
            # Fonts and the logo load asynchronously; capturing before they finish ships fallback glyphs.
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            if not page.evaluate("document.fonts.check('800 63px Outfit')"):
                print("render-banner: Outfit did not load; check banner/fonts/", file=sys.stderr)
                return 1
            page.locator("#banner").screenshot(path=str(TARGET), omit_background=True)
            browser.close()
    except Error as exc:
        print(f"render-banner: {exc}\nInstall Chromium for playwright: python3 -m playwright install chromium", file=sys.stderr)
        return 1
    print(f"wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
