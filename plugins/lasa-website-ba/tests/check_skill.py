#!/usr/bin/env python3
"""Structural checks for the lasa-website-ba plugin and its lasa-website-ba-layout skill.

Usage: python tests/check_skill.py [plugin_dir]
Exit code 0 when no ERROR is found, 1 otherwise. Standard library only.

Paths in the docs are logical: `tests/...` and `README.md` resolve against the plugin
root; everything else (`SKILL.md`, `references/`, `templates/`, `scripts/`) against the
skill folder.
"""
import json
import re
import sys
from pathlib import Path

PLUGIN_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SKILL_NAME = "lasa-website-ba-layout"
SKILL_DIR = PLUGIN_DIR / "skills" / SKILL_NAME
PLUGIN_ONLY = ("tests/", "README.md", "CHANGELOG.md", ".claude-plugin/")
REQUIRED_FILES = [
    ".claude-plugin/plugin.json",
    "README.md",
    "CHANGELOG.md",
    "SKILL.md",
    "scripts/lint_ba_docs.py",
    "references/industry-question-bank.md",
    "references/domain-hosting-question-bank.md",
    "references/design-and-layout-guide.md",
    "references/srs-quality-checklist.md",
    "references/lasa-catalog.md",
    "templates/ba-discovery-brief.md",
    "templates/sitemap-and-page-inventory.md",
    "templates/page-specification.md",
    "templates/srs-template.md",
    "templates/requirements-traceability-matrix.md",
    "templates/decision-log.md",
    "tests/test-scenarios.md",
    "tests/expected-behavior.md",
    "tests/run_tests.py",
]
# Required scenario topics from the brief: (label, regex searched in TS titles)
REQUIRED_SCENARIOS = [
    ("existing theme", r"theme"),
    ("custom corporate", r"doanh nghiệp.*thiết kế riêng"),
    ("e-commerce + payment", r"thương mại điện tử.*thanh toán"),
    ("restaurant + reservations", r"nhà hàng.*đặt bàn"),
    ("multilingual export", r"xuất khẩu đa ngôn ngữ"),
    ("hybrid business", r"lai"),
    ("no domain/hosting", r"chưa có tên miền và hosting"),
    ("migration keeping business email", r"email"),
    ("cannot answer technical questions", r"không trả lời được"),
    ("requirement change midway", r"đổi yêu cầu"),
]
DOMAIN_WORDS = re.compile(r"hosting|tên miền|\bdomain\b|\bDNS\b", re.I)

findings = []


def err(msg):
    findings.append(("ERROR", msg))


def warn(msg):
    findings.append(("WARN", msg))


def resolve(rel):
    in_plugin = rel.startswith(PLUGIN_ONLY) or rel.rstrip("/") == "tests"
    return (PLUGIN_DIR if in_plugin else SKILL_DIR) / rel


def split_cells(line):
    """Split a Markdown table row into cells, ignoring pipes inside backticks."""
    cells, buf, in_code = [], "", False
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    for ch in body:
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append(buf.strip())
            buf = ""
        else:
            buf += ch
    cells.append(buf.strip())
    return cells


def check_markdown(rel, text):
    if text.count("```") % 2:
        err(f"{rel}: số dấu ``` lẻ (code fence chưa đóng)")
    in_fence = False
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append((i + 1, lines[i]))
                i += 1
            header = split_cells(block[0][1])
            if len(block) < 2 or not re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?", block[1][1].strip()):
                err(f"{rel}:{block[0][0]}: bảng thiếu dòng phân cách header")
                continue
            for lineno, row in block[1:]:
                n = len(split_cells(row))
                if n != len(header):
                    err(f"{rel}:{lineno}: bảng có {n} cột, header có {len(header)} cột")
            continue
        i += 1


def headings_with_section(text):
    return {int(m.group(1)) for m in re.finditer(r"^#{2,3}\s*§(\d+)[.\s]", text, re.M)}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # 1. Required files
    for rel in REQUIRED_FILES:
        if not resolve(rel).is_file():
            err(f"thiếu file bắt buộc: {rel}")
    if any(f[0] == "ERROR" for f in findings):
        return report()

    if (SKILL_DIR / "tests").exists():
        err("skill không được chứa thư mục tests/ (người dùng cài plugin sẽ thấy đáp án test)")
    texts = {p.relative_to(SKILL_DIR).as_posix(): p.read_text(encoding="utf-8") for p in sorted(SKILL_DIR.rglob("*.md"))}
    for p in sorted((PLUGIN_DIR / "tests").rglob("*.md")):
        if "fixtures" not in p.parts:
            texts[p.relative_to(PLUGIN_DIR).as_posix()] = p.read_text(encoding="utf-8")
    for name in ("README.md", "CHANGELOG.md"):
        texts[name] = (PLUGIN_DIR / name).read_text(encoding="utf-8")
    skill = texts["SKILL.md"]
    manifest = json.loads((PLUGIN_DIR / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != PLUGIN_DIR.name:
        err(f"plugin.json: name phải trùng tên thư mục plugin '{PLUGIN_DIR.name}'")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        err("plugin.json: thiếu version dạng X.Y.Z")
    elif f"## {manifest['version']}" not in texts["CHANGELOG.md"]:
        err(f"CHANGELOG.md: chưa có mục cho version {manifest['version']}")

    # 2. Frontmatter
    fm = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    if not fm:
        err("SKILL.md: thiếu frontmatter YAML")
    else:
        name = re.search(r"^name:\s*(.+)$", fm.group(1), re.M)
        desc = re.search(r"^description:\s*(.+)$", fm.group(1), re.M)
        if not name or name.group(1).strip() != SKILL_DIR.name:
            err(f"SKILL.md: name phải trùng tên thư mục '{SKILL_DIR.name}'")
        elif not re.fullmatch(r"[a-z0-9-]{1,64}", name.group(1).strip()):
            err("SKILL.md: name chỉ gồm chữ thường, số, gạch nối (≤64 ký tự)")
        if not desc:
            err("SKILL.md: thiếu description")
        elif len(desc.group(1)) > 1024:
            err(f"SKILL.md: description dài {len(desc.group(1))} ký tự (> 1024)")

    # 3. Internal file references and § references
    ref_re = re.compile(r"`((?:references|templates|scripts|tests)/[^`\s]*)`(\s*\(?((?:§\d+(?:\s*[–-]\s*§\d+)?)))?")
    for rel, text in texts.items():
        for m in ref_re.finditer(text):
            target = m.group(1).rstrip("/")
            if any(s in target for s in ("<", "xxx", "*")):
                continue
            path = resolve(target)
            if not path.exists():
                err(f"{rel}: tham chiếu tới file không tồn tại `{m.group(1)}`")
                continue
            if m.group(3) and path.suffix == ".md":
                nums = [int(n) for n in re.findall(r"§(\d+)", m.group(3))]
                wanted = range(nums[0], nums[-1] + 1)
                have = headings_with_section(path.read_text(encoding="utf-8"))
                missing = [n for n in wanted if n not in have]
                if missing:
                    err(f"{rel}: `{target}` không có heading §{', §'.join(map(str, missing))}")

    # 4. Phase order and gate placement in SKILL.md
    phases = [(m.group(1), m.start()) for m in re.finditer(r"^### Phase ([A-Z])\b", skill, re.M)]
    if [p for p, _ in phases] != list("ABCDEFGHI"):
        err(f"SKILL.md: thứ tự phase phải là A→I, đang là {''.join(p for p, _ in phases)}")
    else:
        pos = dict(phases)
        gates = {int(m.group(1)): m.start() for m in re.finditer(r"\*\*Gate G(\d)\b", skill)}
        expected = {1: ("A", "B"), 2: ("D", "E"), 3: ("G", "H"), 4: ("I", None)}
        for g, (after, before) in expected.items():
            if g not in gates:
                err(f"SKILL.md: thiếu Gate G{g}")
                continue
            if gates[g] < pos[after] or (before and gates[g] > pos[before]):
                err(f"SKILL.md: Gate G{g} phải nằm giữa Phase {after} và {before or 'cuối'}")
        # 4b. No domain/hosting questioning before Phase H (R-06)
        for line in skill[pos["A"]:pos["H"]].splitlines():
            if DOMAIN_WORDS.search(line) and "Phase H" not in line:
                err(f"SKILL.md: nội dung Phase A–G nhắc domain/hosting mà không hoãn sang Phase H: {line.strip()[:90]}")
        if skill.find("A1", pos["A"]) > skill.find("?", pos["A"]):
            warn("SKILL.md: câu hỏi đầu tiên trong Phase A có thể không phải A1")

    # 4c. Industry question lines mentioning domain/hosting must defer to Phase H
    for lineno, line in enumerate(texts["references/industry-question-bank.md"].splitlines(), 1):
        if "?" in line and DOMAIN_WORDS.search(line) and "Phase H" not in line:
            err(f"industry-question-bank.md:{lineno}: câu hỏi domain/hosting không hoãn sang Phase H")

    # 5. Section structure of references
    bank_sections = headings_with_section(texts["references/industry-question-bank.md"])
    missing = [n for n in range(0, 16) if n not in bank_sections]
    if missing:
        err(f"industry-question-bank.md: thiếu section §{', §'.join(map(str, missing))}")

    # 6. Templates: document control
    for rel, text in texts.items():
        if rel.startswith("templates/"):
            if "## Document control" not in text:
                err(f"{rel}: thiếu '## Document control'")
            for field in ("Trạng thái", "Current phase", "Last gate passed"):
                if not re.search(rf"^\|\s*{field}\s*\|", text, re.M):
                    err(f"{rel}: Document control thiếu trường '{field}'")

    # 7. Rules ↔ tests traceability
    rules = re.findall(r"^\|\s*(R-\d{2})\s*\|", skill, re.M)
    if len(rules) != len(set(rules)):
        err("SKILL.md: mã rule bị trùng")
    expected_seq = [f"R-{i:02d}" for i in range(1, len(rules) + 1)]
    if rules != expected_seq:
        err("SKILL.md: mã rule phải liên tục R-01..R-NN")
    referenced = set(re.findall(r"\bR-\d{2}\b", "\n".join(texts.values())))
    for r in sorted(referenced - set(rules)):
        err(f"tham chiếu tới rule không tồn tại: {r}")

    scen_text = texts["tests/test-scenarios.md"]
    blocks = re.split(r"^## (?=TS-\d{2})", scen_text, flags=re.M)[1:]
    if len(blocks) < 10:
        err(f"test-scenarios.md: cần ≥ 10 kịch bản, có {len(blocks)}")
    covered = set()
    titles = []
    for b in blocks:
        title = b.splitlines()[0]
        titles.append(title)
        tid = title.split()[0]
        for part in ("**Kịch bản BA**", "**Expected behavior**", "**Failure conditions**", "**Rules:**"):
            if part not in b:
                err(f"{tid}: thiếu mục {part}")
        rl = re.search(r"\*\*Rules:\*\*(.*)", b)
        if rl:
            covered |= set(re.findall(r"\bR-\d{2}\b", rl.group(1)))
    for r in rules:
        if r not in covered:
            err(f"rule {r} chưa được kịch bản nào kiểm (thiếu trong dòng **Rules:**)")
    for label, pattern in REQUIRED_SCENARIOS:
        if not any(re.search(pattern, t, re.I) for t in titles):
            err(f"test-scenarios.md: thiếu kịch bản bắt buộc '{label}'")

    # 8. Markdown sanity
    for rel, text in texts.items():
        check_markdown(rel, text)

    return report()


def report():
    for level, msg in findings:
        print(f"{level}: {msg}")
    n_err = sum(1 for f in findings if f[0] == "ERROR")
    n_warn = len(findings) - n_err
    print(f"check_skill: {n_err} error(s), {n_warn} warning(s) — {SKILL_DIR}")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
