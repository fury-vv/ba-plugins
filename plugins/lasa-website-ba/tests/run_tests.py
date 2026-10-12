#!/usr/bin/env python3
"""Run all automated checks for the lasa-website-ba plugin.

Usage: python tests/run_tests.py
Exit code 0 when every check passes. Standard library only.
"""
import io
import re
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent / "skills" / "lasa-website-ba-layout"
FIXTURES = HERE / "fixtures"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SKILL_DIR / "scripts"))
sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

import check_skill  # noqa: E402
import lint_ba_docs  # noqa: E402

results = []


def record(name, ok, detail=""):
    results.append((name, ok, detail))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # 1. Skill structure
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = check_skill.main()
    errors = [l for l in buf.getvalue().splitlines() if l.startswith("ERROR")]
    record("check_skill: không có ERROR", code == 0, "\n".join(errors))

    # 2. Good fixture: no findings at all
    good = lint_ba_docs.lint([FIXTURES / "sample-good"]).findings
    record(
        "lint sample-good: 0 ERROR, 0 WARN",
        not good,
        "\n".join(f"{lv} {c} {loc}: {m}" for lv, c, loc, m in good),
    )

    # 3. Bad fixture: every seeded defect detected at the expected level
    bad = lint_ba_docs.lint([FIXTURES / "sample-bad"]).findings
    got = {(lv, c) for lv, c, _, _ in bad}
    expected = re.findall(
        r"^\|\s*(L-[A-Z]+)\s*\|\s*(ERROR|WARN)\s*\|",
        (FIXTURES / "EXPECTED-sample-bad.md").read_text(encoding="utf-8"),
        re.M,
    )
    record("lint sample-bad: có lỗi (exit 1)", any(lv == "ERROR" for lv, _ in got))
    for code_, level in expected:
        record(f"lint sample-bad phát hiện {code_} ({level})", (level, code_) in got)
    unexpected = {c for _, c in got} - {c for c, _ in expected}
    record("lint sample-bad: không có mã ngoài kỳ vọng", not unexpected, ", ".join(sorted(unexpected)))

    # 4. Provider-style keys are built at runtime so no key-shaped string is committed
    #    (GitHub push protection would block the push).
    tmp = Path(tempfile.mkdtemp())
    try:
        for label, key in [
            ("Stripe-style", "sk_" + "live_" + "X" * 24),
            ("AWS-style", "AK" + "IA" + "Z" * 16),
            ("GitHub-style", "gh" + "p_" + "a" * 36),
        ]:
            doc = tmp / "04-srs.md"
            doc.write_text(
                "## Document control\n\n| Trường | Giá trị |\n|---|---|\n"
                "| Trạng thái | DRAFT |\n| Current phase | F |\n| Last gate passed | G1 |\n\n"
                f"Ghi chú: khách gửi {key}\n",
                encoding="utf-8",
            )
            codes = {c for _, c, _, _ in lint_ba_docs.lint([doc]).findings}
            record(f"lint phát hiện khoá {label}", "L-SECRET" in codes)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(n) for n, _, _ in results)
    for name, ok, detail in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name.ljust(width)}")
        if not ok and detail:
            for line in detail.splitlines():
                print(f"       {line}")
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
