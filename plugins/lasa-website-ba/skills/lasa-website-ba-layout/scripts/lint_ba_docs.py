#!/usr/bin/env python3
"""Lint a LASA BA deliverable package (Markdown files produced by the skill).

Usage: python scripts/lint_ba_docs.py <folder-or-file> [...]
Exit code 0 when no ERROR is found, 1 otherwise. Standard library only.

Check codes
  L-DOC          Document control table or required field missing
  L-DUP          Same ID defined twice in one table
  L-REF          ID referenced but never defined in the package (WARN)
  L-AC           FR with priority Must has no AC
  L-STATUS       Unknown status value (ERROR) / requirement row without status (WARN)
  L-GATE         Item marked Approved before the gate that allows it
  L-SECRET       Password, OTP, private key or API key found
  L-ISO          Claim of compliance/certification with an ISO standard
  L-LISTING      Listing pages exist but no Detail page (WARN)
  L-VAGUE        Ambiguous word used in an acceptance criterion (WARN)
  L-PLACEHOLDER  Template placeholder left in the document (WARN)
"""
import re
import sys
from pathlib import Path

ID_RE = re.compile(
    r"\b(BG|STK|UG|PG|CMP|FR|NFR|INT|CNT|SEO|DH|BR|AC|ASM|CON|DEP|RSK|Q|DEC|CR|SRC|EXC)-(\d{3})\b"
)
REQ_PREFIXES = ("FR", "NFR", "INT", "CNT", "SEO", "DH", "BR", "PG")
STATUSES = [
    "Draft", "Proposed", "Needs clarification", "Confirmed", "Approved", "Deferred",
    "Out of scope", "Withdrawn", "Superseded", "Open", "Answered", "Closed", "Pending",
    "Passed", "Accepted", "Rejected", "Not started", "In progress", "Done",
    "Authoritative", "Reference", "Outdated", "TBD",
]
SECRET_PATTERNS = [
    (r"(?i)\b(password|passwd|mật khẩu|mat khau)\s*(:|=|là)\s*\S{4,}", "mật khẩu"),
    (r"(?i)\b(otp|mã otp)\s*(:|=|là)\s*\d{4,8}\b", "OTP"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"\bsk_(live|test)_[A-Za-z0-9]{8,}", "API key"),
    (r"\bsk-[A-Za-z0-9_-]{20,}", "API key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key"),
    (r"\bAIza[0-9A-Za-z_-]{35}\b", "Google API key"),
    (r"\bghp_[A-Za-z0-9]{36}\b", "GitHub token"),
    (r"(?i)\b(api[_ -]?key|secret|token)\s*(:|=)\s*[A-Za-z0-9_\-]{16,}", "secret"),
]
ISO_CLAIM = re.compile(
    r"(?i)(tuân thủ|đạt chuẩn|đáp ứng chuẩn|compliant with|complies with|conforms to|certified)\s*(theo\s*)?(tiêu\s*)?(chuẩn\s*)?ISO"
)
VAGUE = [
    "nhanh", "mượt", "đẹp", "hiện đại", "sang trọng", "chuyên nghiệp", "thân thiện", "dễ dùng",
    "trực quan", "tối ưu", "bảo mật cao", "ổn định", "linh hoạt", "đầy đủ", "hỗ trợ tốt",
    "fast", "user-friendly", "modern", "intuitive", "robust", "as needed",
]
VAGUE_RE = re.compile(r"(?i)(?<![\w])(" + "|".join(re.escape(w) for w in VAGUE) + r")(?![\w])")


class Linter:
    def __init__(self):
        self.findings = []  # (level, code, location, message)

    def add(self, level, code, loc, msg):
        self.findings.append((level, code, loc, msg))


def strip_comments(text):
    # Replace HTML comments with blank lines so line numbers stay correct.
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def split_cells(line):
    cells, buf, in_code = [], "", False
    body = line.strip().strip("|")
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


def tables(text):
    """Yield (start_line, header_cells, [(line_no, cells), ...]) outside code fences."""
    lines = text.splitlines()
    in_fence, i = False, 0
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            in_fence = not in_fence
            i += 1
            continue
        if not in_fence and lines[i].lstrip().startswith("|"):
            start = i
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append((i + 1, split_cells(lines[i])))
                i += 1
            if len(block) >= 2 and all(re.fullmatch(r":?-{3,}:?", c) for c in block[1][1] if c):
                yield start + 1, block[0][1], block[2:]
            continue
        i += 1


def col(header, *names):
    for idx, h in enumerate(header):
        if any(n.lower() in h.lower() for n in names):
            return idx
    return None


def lint(paths):
    L = Linter()
    files = []
    for p in paths:
        p = Path(p)
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    if not files:
        L.add("ERROR", "L-DOC", "-", "không tìm thấy file .md")
        return L

    docs = {}
    for f in files:
        docs[f] = strip_comments(f.read_text(encoding="utf-8"))

    # Gate level reached by the package (highest "Last gate passed").
    gate_level = 0
    doc_status = {}
    for f, text in docs.items():
        if "## Document control" not in text:
            L.add("ERROR", "L-DOC", f.name, "thiếu bảng '## Document control'")
            continue
        for field in ("Trạng thái", "Current phase", "Last gate passed"):
            m = re.search(rf"^\|\s*{field}\s*\|\s*([^|]*)\|", text, re.M)
            if not m:
                L.add("ERROR", "L-DOC", f.name, f"Document control thiếu trường '{field}'")
            elif field == "Last gate passed":
                g = re.search(r"G(\d)", m.group(1))
                gate_level = max(gate_level, int(g.group(1)) if g else 0)
            elif field == "Trạng thái":
                doc_status[f] = m.group(1).strip()

    for f, st in doc_status.items():
        if st.upper().startswith("APPROVED") and gate_level < 4:
            L.add("ERROR", "L-GATE", f.name, "tài liệu ghi APPROVED nhưng chưa qua G4")

    defined, mentioned = set(), {}
    listing = detail = 0

    for f, text in docs.items():
        lines = text.splitlines()

        # Heading definitions: "### FR-001 — ..."
        for m in re.finditer(r"^#{2,4}\s*((?:[A-Z]+)-\d{3})\b", text, re.M):
            defined.add(m.group(1))

        for start, header, rows in tables(text):
            first = header[0] if header else ""
            c_prio = col(header, "Ưu tiên", "Priority")
            c_status = col(header, "Trạng thái", "Status")
            c_type = col(header, "Page type")
            seen = {}
            for lineno, cells in rows:
                loc = f"{f.name}:{lineno}"
                key = cells[0] if cells else ""
                mid = ID_RE.fullmatch(key.replace("*", "").strip())
                if mid:
                    rid = mid.group(0)
                    defined.add(rid)
                    if first.strip() != "BG":  # RTM rows repeat BG by design
                        if rid in seen:
                            L.add("ERROR", "L-DUP", loc, f"{rid} định nghĩa lặp trong cùng bảng (dòng {seen[rid]})")
                        seen[rid] = lineno
                    prefix = mid.group(1)
                    row_text = " | ".join(cells)
                    if prefix == "FR" and c_prio is not None and c_prio < len(cells):
                        if cells[c_prio].strip().lower().startswith("must") and "AC-" not in row_text:
                            L.add("ERROR", "L-AC", loc, f"{rid} ưu tiên Must nhưng không có AC")
                    if c_status is not None and c_status < len(cells) and prefix in REQ_PREFIXES:
                        st = cells[c_status].strip()
                        if not st:
                            L.add("WARN", "L-STATUS", loc, f"{rid} thiếu trạng thái")
                        elif not any(st.lower().startswith(s.lower()) for s in STATUSES):
                            L.add("ERROR", "L-STATUS", loc, f"{rid} trạng thái không hợp lệ: '{st}'")
                        elif st.lower().startswith("approved"):
                            need = 2 if prefix == "PG" else 3
                            if gate_level < need:
                                L.add("ERROR", "L-GATE", loc, f"{rid} là Approved nhưng gói tài liệu mới qua G{gate_level} (cần G{need})")
                    if prefix == "AC":
                        for v in VAGUE_RE.findall(row_text):
                            L.add("WARN", "L-VAGUE", loc, f"{rid} dùng từ mơ hồ '{v}' trong tiêu chí nghiệm thu")
                if c_type is not None and c_type < len(cells):
                    t = cells[c_type].strip().lower()
                    listing += t.startswith("listing")
                    detail += t.startswith("detail")

        for lineno, line in enumerate(lines, 1):
            loc = f"{f.name}:{lineno}"
            for m in ID_RE.finditer(line):
                mentioned.setdefault(m.group(0), loc)
            for pat, label in SECRET_PATTERNS:
                if re.search(pat, line):
                    L.add("ERROR", "L-SECRET", loc, f"phát hiện {label} — xoá khỏi tài liệu và đề nghị khách đổi/thu hồi")
            m = ISO_CLAIM.search(line)
            if m and not re.search(r"(?i)(không|not|never)\W+(\w+\W+){0,3}$", line[: m.start()]):
                L.add("ERROR", "L-ISO", loc, "tuyên bố tuân thủ/chứng nhận ISO — chỉ được ghi 'tham chiếu'")
            if re.match(r"\s*-?\s*`?AC-\d{3}", line) and not line.lstrip().startswith("|"):
                for v in VAGUE_RE.findall(line):
                    L.add("WARN", "L-VAGUE", loc, f"từ mơ hồ '{v}' trong tiêu chí nghiệm thu")
            has_inline_code = "`" in line  # `<ID>` inside code spans is documentation, not a placeholder
            for ph in re.findall(r"<[^<>\n]{1,40}>", line):
                if not has_inline_code and not re.fullmatch(r"</?\w+\s*/?>", ph):
                    L.add("WARN", "L-PLACEHOLDER", loc, f"placeholder chưa thay: {ph}")

    for rid, loc in sorted(mentioned.items()):
        if rid not in defined:
            L.add("WARN", "L-REF", loc, f"{rid} được nhắc tới nhưng không được định nghĩa trong gói tài liệu")
    if listing and not detail:
        L.add("WARN", "L-LISTING", "sitemap", f"có {listing} trang Listing nhưng không có trang Detail nào (R-10)")
    return L


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not argv:
        print(__doc__)
        return 2
    L = lint(argv)
    for level, code, loc, msg in L.findings:
        print(f"{level} {code} {loc}: {msg}")
    n_err = sum(1 for f in L.findings if f[0] == "ERROR")
    print(f"lint_ba_docs: {n_err} error(s), {len(L.findings) - n_err} warning(s)")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
