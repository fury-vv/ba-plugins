#!/usr/bin/env python3
"""Quét core skill tìm thuật ngữ đặc thù lĩnh vực (hỗ trợ kiểm tra domain-neutral).

Mặc định quét skills/srs-analysis/SKILL.md và skills/srs-analysis/references/*.md
với danh sách trong tests/domain-neutral-terms.txt.

Cách dùng (từ thư mục gốc plugin):
    python3 tests/scan_domain_terms.py
    python3 tests/scan_domain_terms.py --strict      # exit 1 nếu có kết quả
    python3 tests/scan_domain_terms.py path/a.md ...

Đây chỉ là công cụ hỗ trợ: có thể bỏ sót hoặc báo nhầm. Kết quả cần người xem lại.
Chỉ dùng thư viện chuẩn; chỉ đọc file.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
TERMS_FILE = Path(__file__).resolve().parent / "domain-neutral-terms.txt"


def load_terms(path: Path) -> Tuple[List[str], List[str]]:
    terms: List[str] = []
    allowed: List[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            allowed.append(line[1:].split("|", 1)[0].strip().lower())
        else:
            terms.append(line.lower())
    return terms, allowed


def default_paths() -> List[Path]:
    skill = ROOT / "skills" / "srs-analysis"
    return [skill / "SKILL.md"] + sorted((skill / "references").glob("*.md"))


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="File cần quét (mặc định: core skill)")
    parser.add_argument("--strict", action="store_true", help="Exit 1 nếu có kết quả")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    terms, allowed = load_terms(TERMS_FILE)
    patterns = [(t, re.compile(r"(?<!\w)" + re.escape(t) + r"(?!\w)", re.IGNORECASE)) for t in terms]
    paths = [Path(p) for p in args.paths] or default_paths()
    hits = 0
    for path in paths:
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            cleaned = line.lower()
            for phrase in allowed:
                cleaned = cleaned.replace(phrase, " ")
            for term, pattern in patterns:
                if pattern.search(cleaned):
                    hits += 1
                    rel = path.relative_to(ROOT) if path.is_absolute() and ROOT in path.parents else path
                    print(f"{rel}:{no}: '{term}' — {line.strip()[:120]}")
    print(f"Tổng: {hits} kết quả trong {len(paths)} file. Kết quả cần người xem lại.")
    return 1 if (args.strict and hits) else 0


if __name__ == "__main__":
    sys.exit(main())
