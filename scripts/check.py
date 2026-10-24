"""Pre-commit check for the profile README.

Usage: python3 scripts/check.py
Fails when a relative image or link in profile/README.md points at a missing file, when the
banner is not a 2560x800 PNG, or when a text file contains a banned dash (en dash,
em dash or horizontal bar, U+2013 to U+2015, or their HTML entities). Stdlib only, offline:
external URLs are not fetched.
"""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "profile/README.md"
BANNER = ROOT / "profile/assets/banner.png"
BANNER_SIZE = (2560, 800)
TEXT_GLOBS = ["*.md", "profile/*.md", "banner/*.html", "scripts/*.py"]
# Built from code points so this file never contains the characters it bans.
DASH_CHARS = "".join(chr(c) for c in (0x2013, 0x2014, 0x2015))
DASHES = re.compile(f"[{DASH_CHARS}]|&(mdash|ndash|horbar);|&#(8211|8212|8213|x201[345]);", re.I)
REF = re.compile(r'(?:src|href)="([^"]+)"|\]\(([^)\s]+)\)')


def main() -> int:
    errors: list[str] = []
    for match in REF.finditer(README.read_text(encoding="utf-8")):
        target = match.group(1) or match.group(2)
        if re.match(r"[a-z]+:|#", target):
            continue
        if not (README.parent / target.split("#")[0]).is_file():
            errors.append(f"profile/README.md: missing file {target}")
    # A PNG's IHDR chunk holds width and height at bytes 16-24.
    head = BANNER.read_bytes()[:24] if BANNER.is_file() else b""
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", head[16:24]) != BANNER_SIZE:
        errors.append("profile/assets/banner.png is missing or not 2560x800: run python3 scripts/render-banner.py")
    for pattern in TEXT_GLOBS:
        for path in ROOT.glob(pattern):
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if DASHES.search(line):
                    errors.append(f"{path.relative_to(ROOT)}:{n}: banned dash")
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("check: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
