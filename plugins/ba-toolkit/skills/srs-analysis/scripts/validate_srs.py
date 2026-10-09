#!/usr/bin/env python3
"""Kiểm tra cấu trúc SRS Markdown theo quy ước của skill srs-analysis.

Script chỉ ĐỌC file đầu vào, không sửa. Nó kiểm tra cấu trúc và lỗi cơ học:
section bắt buộc, ID trùng hoặc sai định dạng, tham chiếu tới ID chưa định
nghĩa, trường bắt buộc của requirement, acceptance criteria, placeholder/TBD,
traceability, bảng coverage, khối sơ đồ Mermaid, nhất quán trạng thái phê duyệt.

Script KHÔNG chứng minh nội dung nghiệp vụ đúng và KHÔNG thay thế việc review
của BA và stakeholder. Quy ước được kiểm tra nằm ở references/srs-template.md.

Cách dùng:
    python3 validate_srs.py docs/srs/srs.md
    python3 validate_srs.py --partial examples/sample-srs-excerpt.md
    python3 validate_srs.py --ascii docs/srs/srs.md

Tùy chọn:
    --partial   Trích đoạn SRS: bỏ kiểm tra đủ section; tham chiếu treo chỉ là WARNING.
    --ascii     In kết quả không dấu (cho console không hiển thị được UTF-8).

Exit code:
    0  không có ERROR (có thể có WARNING/INFO)
    1  có ít nhất một ERROR
    2  lỗi sử dụng hoặc không đọc được file

Chỉ dùng thư viện chuẩn Python. Cú pháp tương thích Python 3.9 trở lên.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

TOOL_VERSION = "1.0.0"

DISCLAIMER = (
    "Lưu ý: validator chỉ kiểm tra cấu trúc và lỗi cơ học; không chứng minh nội dung "
    "nghiệp vụ đúng và không thay thế review của BA và stakeholder."
)

# (số, English title, được phép ghi Not applicable)
SECTIONS: List[Tuple[int, str, bool]] = [
    (1, "Document Control", False),
    (2, "Executive Summary", False),
    (3, "Goals and Success Metrics", False),
    (4, "Scope", False),
    (5, "Stakeholders and Users", False),
    (6, "Glossary", True),
    (7, "Assumptions, Constraints and Dependencies", False),
    (8, "Business Processes and Use Cases", True),
    (9, "Functional Requirements", False),
    (10, "Business Rules", True),
    (11, "Data Requirements", True),
    (12, "Interface and Integration Requirements", True),
    (13, "User Interface Requirements", True),
    (14, "Non-Functional Requirements", False),
    (15, "User Stories", True),
    (16, "Permissions", True),
    (17, "Lifecycle and State Transitions", True),
    (18, "Reports, Search, Exports and Notifications", True),
    (19, "Security, Privacy, Audit and Retention", True),
    (20, "Migration, Rollout and Operations", True),
    (21, "Models and Diagrams", False),
    (22, "Domain-Specific Considerations", True),
    (23, "Risks", False),
    (24, "Open Questions", False),
    (25, "Decision Log", False),
    (26, "Sources", False),
    (27, "Elicitation Coverage", False),
    (28, "Traceability Matrix", False),
    (29, "Approval Record", False),
    (30, "Change Requests", True),
]
SECTION_BY_NUM: Dict[int, Tuple[str, bool]] = {n: (t, na) for n, t, na in SECTIONS}
COVERAGE_SECTIONS = list(range(2, 23))

# Tiền tố được định nghĩa ở ô đầu của dòng bảng, trong section sở hữu.
TABLE_OWNERS: Dict[str, int] = {"GOAL": 3, "ASM": 7, "UXP": 13, "RISK": 23, "Q": 24, "DEC": 25, "SRC": 26}
REQ_PREFIXES = ("FR", "BR", "DR", "IR", "UIR", "NFR")
ALL_PREFIXES = (
    "AC", "FR", "BR", "DR", "IR", "UIR", "NFR", "GOAL", "US", "UC",
    "DIA", "ASM", "Q", "RISK", "DEC", "SRC", "UXP", "CR",
)

_MOD = r"(?:[A-Z][A-Z0-9]{1,5}-)?"
_REQ = r"(?:FR|BR|DR|IR|UIR|NFR)-" + _MOD + r"\d{3}"
_AC = r"AC-(?:" + _REQ + r"|US-\d{3})-\d{2}"
_SIMPLE = r"(?:GOAL|US|UC|DIA|ASM|Q|RISK|DEC|SRC|UXP|CR)-\d{3}"
_ID = r"(?:" + _AC + r"|" + _REQ + r"|" + _SIMPLE + r")"

ID_RE = re.compile(r"(?<![A-Za-z0-9-])" + _ID + r"(?![A-Za-z0-9])")
ID_FULL_RE = re.compile(_ID)
TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9-])(?:" + "|".join(ALL_PREFIXES) + r")-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*"
)
AC_DEF_RE = re.compile(r"^\s*[-*+]\s+(?:\*\*)?(" + _AC + r")(?:\*\*)?\s*(?::|—|–|-)")
H3_ID_RE = re.compile(r"^###\s+(" + _ID + r")(?![A-Za-z0-9])")

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
NUMBERED_RE = re.compile(r"^(\d+)\.\s+(.*)$")
FIELD_BOLD_RE = re.compile(r"^\s*[-*+]\s+\*\*([^*]+?)\s*:?\s*\*\*\s*:?\s*(.*)$")
FIELD_PLAIN_RE = re.compile(r"^\s*[-*+]\s+([A-Za-z][A-Za-z /—–-]{0,40}?)\s*:\s+(.*)$")
NA_RE = re.compile(r"^\s*(not applicable|không áp dụng|n/a)(?![A-Za-z])\s*[—–:\-]?\s*(.*)$", re.IGNORECASE)
TBD_RE = re.compile(r"(?<![A-Za-z])(TBD|TODO|FIXME|TBC)(?![A-Za-z])")
BRACKET_RE = re.compile(r"\[(?!\s?\]|[xX]\]|\^)([^\]\n]{1,80})\](?![\(\[:])")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEX_RE = re.compile(r"(?<![\w&#])#([0-9A-Fa-f]{3,})(?![0-9A-Za-z])")
SEP_CELL_RE = re.compile(r"^:?-{3,}:?$")
VERSION_RE = re.compile(r"^v?(\d+)\.(\d+)$", re.IGNORECASE)

REQ_STATUS = {"proposed", "confirmed", "approved", "deferred", "rejected", "superseded"}
CR_STATUS = {"proposed", "approved", "rejected", "deferred", "implemented"}
PRIORITY = {"must", "should", "could", "won't"}
Q_PRIORITY = {"p0", "p1", "p2"}
Q_STATUS = {"open", "answered", "deferred", "risk accepted"}
COVERAGE_STATUS = {"answered", "tbd", "not applicable", "deferred"}
UXP_TYPES = {"constraint", "preference", "reference"}
DOC_STATUS = {"DRAFT — NOT APPROVED", "APPROVED", "ON HOLD"}
MERMAID_TYPES = {
    "flowchart", "graph", "sequencediagram", "statediagram-v2",
    "statediagram", "erdiagram", "gantt",
}
LEVEL_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}


@dataclass
class Finding:
    level: str
    code: str
    line: int
    message: str

    def render(self) -> str:
        return f"{self.level} {self.code} L{self.line}: {self.message}"


@dataclass
class Section:
    num: Optional[int]
    raw_title: str
    heading_idx: int
    end_idx: int  # exclusive


@dataclass
class Block:
    ident: str
    heading_idx: int
    end_idx: int  # exclusive


@dataclass
class Table:
    header: List[str]
    rows: List[Tuple[int, List[str]]]

    def col(self, *names: str) -> Optional[int]:
        for name in names:
            if name in self.header:
                return self.header.index(name)
        return None


def clean_cell(text: str) -> str:
    return text.replace("*", "").replace("`", "").strip()


def norm_value(text: str) -> str:
    value = clean_cell(text).replace("’", "'")
    value = re.split(r"\s+\(|\s+—\s+|\s+–\s+|\s+-\s+|;|,", value)[0]
    return value.strip().rstrip(".").lower()


def split_row(line: str) -> List[str]:
    s = line.strip().replace("\\|", "\u0000")
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.replace("\u0000", "|").strip() for c in s.split("|")]


def english_title(raw: str) -> str:
    part = re.split(r"\s+[—–]\s+|\s+-\s+", raw, maxsplit=1)[0]
    return re.sub(r"\s+", " ", part).strip().lower()


def to_ascii(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D").replace("—", "-").replace("–", "-")
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).encode("ascii", "replace").decode("ascii")


class Validator:
    def __init__(self, text: str, partial: bool = False) -> None:
        self.text = text
        self.lines = text.splitlines()
        self.partial = partial
        self.findings: List[Finding] = []
        n = len(self.lines)
        self.code = [False] * n      # dòng thuộc khối code thường hoặc dòng rào fence
        self.mermaid = [False] * n   # dòng nội dung của khối mermaid
        self.mermaid_blocks: List[Tuple[int, int]] = []  # (dòng mở fence, dòng đóng hoặc n)
        self.sections: List[Section] = []
        self.blocks: List[Block] = []
        self.defs: Dict[str, List[int]] = {}
        self.ac_defs: List[Tuple[str, int]] = []
        self.doc_status: Optional[str] = None
        self.doc_version: Optional[str] = None
        self.domain_confirmed: Optional[bool] = None
        self.open_p0: List[str] = []
        self.q_counts: Dict[str, int] = {}

    # ---------- tiện ích ----------
    def add(self, level: str, code: str, idx: int, message: str) -> None:
        self.findings.append(Finding(level, code, idx + 1 if idx >= 0 else 0, message))

    def is_prose(self, idx: int) -> bool:
        return not self.code[idx] and not self.mermaid[idx]

    def section(self, num: int) -> Optional[Section]:
        for s in self.sections:
            if s.num == num:
                return s
        return None

    def section_num_at(self, idx: int) -> Optional[int]:
        for s in self.sections:
            if s.heading_idx <= idx < s.end_idx:
                return s.num
        return None

    def content_lines(self, start: int, end: int) -> List[int]:
        return [i for i in range(start, end) if self.lines[i].strip()]

    def na_info(self, sec: Section) -> Tuple[bool, str]:
        body = self.content_lines(sec.heading_idx + 1, sec.end_idx)
        if not body:
            return False, ""
        m = NA_RE.match(self.lines[body[0]]) if self.is_prose(body[0]) else None
        if m and len(body) == 1:
            return True, m.group(2).strip()
        return False, ""

    def tables(self, start: int, end: int) -> List[Table]:
        result: List[Table] = []
        i = start
        while i < end:
            if self.is_prose(i) and self.lines[i].strip().startswith("|"):
                rows: List[Tuple[int, List[str]]] = []
                while i < end and self.is_prose(i) and self.lines[i].strip().startswith("|"):
                    rows.append((i, split_row(self.lines[i])))
                    i += 1
                header: List[str] = []
                data = rows
                if len(rows) >= 2 and all(SEP_CELL_RE.match(c.replace(" ", "")) for c in rows[1][1] if c):
                    header = [clean_cell(c).lower() for c in rows[0][1]]
                    data = rows[2:]
                result.append(Table(header, data))
            else:
                i += 1
        return result

    def block_fields(self, block: Block) -> Dict[str, Tuple[str, int]]:
        fields: Dict[str, Tuple[str, int]] = {}
        for i in range(block.heading_idx + 1, block.end_idx):
            if not self.is_prose(i):
                continue
            line = self.lines[i]
            if AC_DEF_RE.match(line):
                continue
            m = FIELD_BOLD_RE.match(line) or FIELD_PLAIN_RE.match(line)
            if m:
                name = re.sub(r"\s+", " ", m.group(1)).strip().lower()
                if name not in fields:
                    fields[name] = (m.group(2).strip(), i)
        return fields

    def block_ids(self, block: Block) -> List[str]:
        ids: List[str] = []
        for i in range(block.heading_idx + 1, block.end_idx):
            if self.is_prose(i) or self.mermaid[i]:
                ids.extend(m.group(0) for m in ID_RE.finditer(self.lines[i]))
        return ids

    # ---------- phân tích cấu trúc ----------
    def scan_fences(self) -> None:
        open_char = ""
        open_len = 0
        is_mermaid = False
        start = -1
        for i, line in enumerate(self.lines):
            m = FENCE_RE.match(line)
            if not open_char:
                if m:
                    open_char = m.group(1)[0]
                    open_len = len(m.group(1))
                    is_mermaid = m.group(2).lower().startswith("mermaid")
                    start = i
                    self.code[i] = True
                continue
            closing = m and m.group(1)[0] == open_char and len(m.group(1)) >= open_len and not m.group(2)
            if closing:
                self.code[i] = True
                if is_mermaid:
                    self.mermaid_blocks.append((start, i))
                open_char = ""
                continue
            if is_mermaid:
                self.mermaid[i] = True
            else:
                self.code[i] = True
        if open_char:
            if is_mermaid:
                self.mermaid_blocks.append((start, len(self.lines)))
            self.add("WARNING", "DOC002", start, "Khối code mở nhưng chưa đóng; phần còn lại của file bị bỏ qua khi kiểm tra.")

    def scan_headings(self) -> None:
        h2: List[Tuple[int, str]] = []
        h3: List[Tuple[int, str]] = []
        heads_upto3: List[int] = []
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            m = HEADING_RE.match(line)
            if not m:
                continue
            level = len(m.group(1))
            if level <= 3:
                heads_upto3.append(i)
            if level == 2:
                h2.append((i, m.group(2)))
            elif level == 3:
                h3.append((i, line))
        n = len(self.lines)
        for k, (idx, title) in enumerate(h2):
            end = h2[k + 1][0] if k + 1 < len(h2) else n
            num_m = NUMBERED_RE.match(title)
            num = int(num_m.group(1)) if num_m else None
            raw = num_m.group(2) if num_m else title
            self.sections.append(Section(num, raw, idx, end))
        for idx, line in h3:
            m = H3_ID_RE.match(line)
            if not m:
                continue
            later = [h for h in heads_upto3 if h > idx]
            end = later[0] if later else n
            self.blocks.append(Block(m.group(1), idx, end))

    # ---------- kiểm tra ----------
    def check_sections(self) -> None:
        seen: Dict[int, int] = {}
        for sec in self.sections:
            if sec.num is None or sec.num not in SECTION_BY_NUM:
                self.add("WARNING", "SEC007", sec.heading_idx,
                         f"Section H2 không thuộc danh sách chuẩn: '{self.lines[sec.heading_idx].strip()}'.")
                continue
            expected, _ = SECTION_BY_NUM[sec.num]
            if english_title(sec.raw_title) != expected.lower():
                self.add("ERROR", "SEC002", sec.heading_idx,
                         f"Section {sec.num} có tên '{sec.raw_title.strip()}'; mong đợi '## {sec.num}. {expected} — <tiếng Việt>'.")
            if sec.num in seen:
                self.add("WARNING", "SEC003", sec.heading_idx,
                         f"Section {sec.num} xuất hiện lần nữa (lần đầu ở L{seen[sec.num] + 1}).")
            else:
                seen[sec.num] = sec.heading_idx
        if not self.partial:
            for num, title, _ in SECTIONS:
                if num not in seen:
                    self.add("ERROR", "SEC001", -1, f"Thiếu section bắt buộc: '## {num}. {title} — <tiếng Việt>'.")
        for sec in self.sections:
            if sec.num is None or sec.num not in SECTION_BY_NUM:
                continue
            body = self.content_lines(sec.heading_idx + 1, sec.end_idx)
            if not body:
                self.add("WARNING", "SEC004", sec.heading_idx,
                         f"Section {sec.num} rỗng; ghi nội dung hoặc 'Not applicable — <lý do>'.")
                continue
            is_na, reason = self.na_info(sec)
            if is_na:
                if len(reason) < 3:
                    self.add("WARNING", "SEC005", sec.heading_idx + 1,
                             f"Section {sec.num} ghi Not applicable nhưng thiếu lý do.")
                if not SECTION_BY_NUM[sec.num][1]:
                    self.add("WARNING", "SEC006", sec.heading_idx + 1,
                             f"Section {sec.num} ({SECTION_BY_NUM[sec.num][0]}) không được ghi Not applicable.")

    def collect_definitions(self) -> None:
        for b in self.blocks:
            self.defs.setdefault(b.ident, []).append(b.heading_idx)
        for sec in self.sections:
            if sec.num is None:
                continue
            owned = [p for p, num in TABLE_OWNERS.items() if num == sec.num]
            if not owned:
                continue
            for table in self.tables(sec.heading_idx + 1, sec.end_idx):
                for idx, cells in table.rows:
                    if not cells:
                        continue
                    first = clean_cell(cells[0])
                    if ID_FULL_RE.fullmatch(first) and first.split("-")[0] in owned:
                        self.defs.setdefault(first, []).append(idx)
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            m = AC_DEF_RE.match(line)
            if m:
                ac = m.group(1)
                self.ac_defs.append((ac, i))
                self.defs.setdefault(ac, []).append(i)

    def check_ids(self) -> None:
        for ident, where in self.defs.items():
            if len(where) > 1:
                first = where[0] + 1
                for idx in where[1:]:
                    self.add("ERROR", "ID001", idx, f"ID {ident} được định nghĩa lại (lần đầu ở L{first}).")
        dangling_level = "WARNING" if self.partial else "ERROR"
        refs: Dict[str, List[int]] = {}
        malformed: Dict[str, int] = {}
        for i, line in enumerate(self.lines):
            if not (self.is_prose(i) or self.mermaid[i]):
                continue
            for m in ID_RE.finditer(line):
                refs.setdefault(m.group(0), []).append(i)
            for m in TOKEN_RE.finditer(line):
                tok = m.group(0)
                if any(ch.isdigit() for ch in tok) and not ID_FULL_RE.fullmatch(tok) and tok not in malformed:
                    malformed[tok] = i
        for ident, where in refs.items():
            if ident not in self.defs:
                extra = f" (xuất hiện {len(where)} lần)" if len(where) > 1 else ""
                self.add(dangling_level, "ID002", where[0], f"Tham chiếu tới ID chưa được định nghĩa: {ident}{extra}.")
        for ac, idx in self.ac_defs:
            parent = ac[3:-3]
            if parent not in self.defs:
                self.add(dangling_level, "ID002", idx, f"{ac} thuộc {parent}, nhưng {parent} chưa được định nghĩa.")
            owner = self.block_at(idx)
            if owner is None or owner.ident != parent:
                where = owner.ident if owner else "ngoài mọi khối"
                self.add("WARNING", "ID004", idx, f"{ac} phải được định nghĩa trong khối {parent}, hiện nằm ở {where}.")
        for tok, idx in malformed.items():
            self.add("WARNING", "ID003", idx, f"ID sai định dạng: '{tok}' (xem mục A4 của srs-template.md).")

    def block_at(self, idx: int) -> Optional[Block]:
        for b in self.blocks:
            if b.heading_idx < idx < b.end_idx:
                return b
        return None

    def block_status(self, block: Block) -> str:
        fields = self.block_fields(block)
        return norm_value(fields["status"][0]) if "status" in fields else ""

    def check_requirements(self) -> None:
        for b in self.blocks:
            prefix = b.ident.split("-")[0]
            fields = self.block_fields(b)
            ids = self.block_ids(b)
            has_ac = any(x.startswith("AC-") for x in ids)
            status = norm_value(fields["status"][0]) if "status" in fields else ""
            if prefix in REQ_PREFIXES:
                missing = [f for f in ("statement", "source", "priority", "status") if not fields.get(f, ("", 0))[0]]
                if missing:
                    self.add("WARNING", "REQ001", b.heading_idx, f"{b.ident} thiếu trường: {', '.join(missing)}.")
                self._check_status(b, fields, REQ_STATUS)
                self._check_priority(b, fields)
                active = status not in ("rejected", "superseded")
                if status == "superseded" and not fields.get("superseded by", ("", 0))[0]:
                    self.add("WARNING", "REQ007", b.heading_idx, f"{b.ident} có Status Superseded nhưng thiếu 'Superseded by'.")
                if not active:
                    continue
                verification = fields.get("verification", ("", 0))[0]
                if prefix == "FR" and not has_ac:
                    self.add("WARNING", "REQ004", b.heading_idx, f"{b.ident} chưa có acceptance criteria.")
                elif prefix in ("BR", "DR", "IR", "UIR") and not has_ac and not verification:
                    self.add("WARNING", "REQ005", b.heading_idx, f"{b.ident} chưa có acceptance criteria hoặc Verification.")
                elif prefix == "NFR":
                    lacking = [f for f in ("target", "verification") if not fields.get(f, ("", 0))[0]]
                    if lacking:
                        self.add("WARNING", "REQ006", b.heading_idx, f"{b.ident} thiếu: {', '.join(lacking)}.")
            elif prefix == "US":
                lacking = []
                if not fields.get("story", ("", 0))[0]:
                    lacking.append("Story")
                related = fields.get("related", ("", 0))[0]
                if not any(x.split("-")[0] in REQ_PREFIXES for x in ID_RE.findall(related)):
                    lacking.append("Related tới requirement")
                if not has_ac:
                    lacking.append("acceptance criteria")
                if lacking:
                    self.add("WARNING", "REQ008", b.heading_idx, f"{b.ident} thiếu: {', '.join(lacking)}.")
                self._check_status(b, fields, REQ_STATUS)
                self._check_priority(b, fields)
            elif prefix in ("UC", "DIA"):
                self._check_status(b, fields, REQ_STATUS)
            elif prefix == "CR":
                self._check_status(b, fields, CR_STATUS)

    def _check_status(self, b: Block, fields: Dict[str, Tuple[str, int]], allowed: Set[str]) -> None:
        if "status" in fields and fields["status"][0]:
            value = norm_value(fields["status"][0])
            if value not in allowed:
                self.add("WARNING", "REQ002", fields["status"][1],
                         f"{b.ident}: Status '{fields['status'][0]}' không hợp lệ ({', '.join(sorted(allowed))}).")

    def _check_priority(self, b: Block, fields: Dict[str, Tuple[str, int]]) -> None:
        if "priority" in fields and fields["priority"][0]:
            value = norm_value(fields["priority"][0])
            if value not in PRIORITY:
                self.add("WARNING", "REQ003", fields["priority"][1],
                         f"{b.ident}: Priority '{fields['priority'][0]}' không hợp lệ (Must, Should, Could, Won't).")

    def check_diagrams(self) -> None:
        dia_blocks = [b for b in self.blocks if b.ident.startswith("DIA-")]
        for start, end in self.mermaid_blocks:
            owner = self.block_at(start)
            if owner is None or not owner.ident.startswith("DIA-"):
                self.add("WARNING", "DIA003", start, "Khối mermaid nằm ngoài khối DIA-; thêm heading '### DIA-xxx — <tên>'.")
            first = None
            for i in range(start + 1, min(end, len(self.lines))):
                s = self.lines[i].strip()
                if s and not s.startswith("%%"):
                    first = (i, s)
                    break
            if first:
                kind = first[1].split()[0].rstrip(":").lower()
                if kind not in MERMAID_TYPES:
                    self.add("WARNING", "DIA002", first[0],
                             f"Loại Mermaid '{first[1].split()[0]}' không nằm trong danh sách cho phép của v1.")
        for b in dia_blocks:
            if not any(b.heading_idx < s < b.end_idx for s, _ in self.mermaid_blocks):
                self.add("WARNING", "DIA001", b.heading_idx, f"{b.ident} không có khối mermaid.")
            if not self.block_fields(b).get("source", ("", 0))[0]:
                self.add("WARNING", "DIA004", b.heading_idx, f"{b.ident} thiếu trường Source.")
        sec21 = self.section(21)
        if sec21 is not None and not self.na_info(sec21)[0]:
            has_context = False
            for b in dia_blocks:
                if sec21.heading_idx < b.heading_idx < sec21.end_idx:
                    if "context" in self.block_fields(b).get("type", ("", 0))[0].lower():
                        has_context = True
            if not has_context:
                self.add("WARNING", "DIA005", sec21.heading_idx, "Section 21 chưa có sơ đồ Type: Context (bắt buộc).")

    def check_placeholders(self) -> int:
        sec27 = self.section(27)
        tbd_count = 0
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            stripped = INLINE_CODE_RE.sub("", line)
            in_coverage = sec27 is not None and sec27.heading_idx <= i < sec27.end_idx
            m = TBD_RE.search(stripped)
            if m and not in_coverage:
                tbd_count += 1
                self.add("WARNING", "PH001", i, f"Còn '{m.group(1)}': cần giải quyết hoặc gắn Q- và người trả lời.")
            b = BRACKET_RE.search(stripped)
            if b:
                self.add("WARNING", "PH002", i, f"Có vẻ là placeholder chưa điền: '[{b.group(1)}]'.")
        return tbd_count

    def check_document_control(self) -> None:
        sec1 = self.section(1)
        if sec1 is None:
            return
        fields: Dict[str, Tuple[str, int]] = {}
        for table in self.tables(sec1.heading_idx + 1, sec1.end_idx):
            if "field" in table.header and "value" in table.header:
                fi, vi = table.header.index("field"), table.header.index("value")
                for idx, cells in table.rows:
                    if len(cells) > max(fi, vi):
                        fields[clean_cell(cells[fi]).lower()] = (clean_cell(cells[vi]), idx)
        status_raw, status_idx = fields.get("status", ("", sec1.heading_idx))
        status = re.sub(r"\s+[-–—]\s+", " — ", status_raw.upper())
        status = re.sub(r"\s+", " ", status).strip()
        if status not in DOC_STATUS:
            self.add("WARNING", "APR004", status_idx,
                     f"Status tài liệu '{status_raw}' không hợp lệ (DRAFT — NOT APPROVED, APPROVED, ON HOLD).")
        else:
            self.doc_status = status
        version_raw, version_idx = fields.get("document version", ("", sec1.heading_idx))
        vm = VERSION_RE.match(version_raw)
        if not vm:
            self.add("WARNING", "APR005", version_idx, f"Document version '{version_raw}' không đúng dạng X.Y.")
        else:
            self.doc_version = f"{int(vm.group(1))}.{int(vm.group(2))}"
        domain = fields.get("domain", ("", 0))[0].lower()
        self.domain_confirmed = domain.startswith("confirmed") or domain.startswith("đã xác nhận")

    def check_domain(self) -> None:
        sec22 = self.section(22)
        if sec22 is None or self.domain_confirmed is None:
            return
        body = self.content_lines(sec22.heading_idx + 1, sec22.end_idx)
        if body and not self.na_info(sec22)[0] and not self.domain_confirmed:
            self.add("WARNING", "DOM001", sec22.heading_idx,
                     "Section 22 có nội dung nhưng Domain trong Document Control chưa được xác nhận.")

    def check_questions(self) -> None:
        sec = self.section(24)
        if sec is None:
            return
        for table in self.tables(sec.heading_idx + 1, sec.end_idx):
            pi, si = table.col("priority"), table.col("status")
            for idx, cells in table.rows:
                if not cells:
                    continue
                qid = clean_cell(cells[0])
                if not re.fullmatch(r"Q-\d{3}", qid):
                    continue
                prio = norm_value(cells[pi]) if pi is not None and pi < len(cells) else ""
                stat = norm_value(cells[si]) if si is not None and si < len(cells) else ""
                problems = []
                if prio not in Q_PRIORITY:
                    problems.append(f"Priority '{prio or '(trống)'}'")
                if stat not in Q_STATUS:
                    problems.append(f"Status '{stat or '(trống)'}'")
                if problems:
                    self.add("WARNING", "Q001", idx, f"{qid}: {', '.join(problems)} không hợp lệ.")
                key = f"{prio.upper() or '?'} {stat or '?'}"
                self.q_counts[key] = self.q_counts.get(key, 0) + 1
                if prio == "p0" and stat == "open":
                    self.open_p0.append(qid)

    def check_approval(self) -> None:
        if self.doc_status != "APPROVED":
            return
        sec29 = self.section(29)
        matched = False
        if sec29 is not None:
            for table in self.tables(sec29.heading_idx + 1, sec29.end_idx):
                vi, di = table.col("version"), table.col("decision")
                if vi is None or di is None:
                    continue
                for _, cells in table.rows:
                    if len(cells) <= max(vi, di):
                        continue
                    vm = VERSION_RE.match(clean_cell(cells[vi]))
                    version = f"{int(vm.group(1))}.{int(vm.group(2))}" if vm else ""
                    decision = clean_cell(cells[di]).upper()
                    if version == self.doc_version and decision in ("APPROVE", "DUYỆT"):
                        matched = True
        if not matched:
            self.add("WARNING", "APR001", (sec29.heading_idx if sec29 else -1),
                     f"Tài liệu APPROVED nhưng Approval Record không có dòng APPROVE cho version {self.doc_version}.")
        proposed = [b.ident for b in self.blocks
                    if b.ident.split("-")[0] in REQ_PREFIXES + ("US", "UC", "DIA") and self.block_status(b) == "proposed"]
        if proposed:
            shown = ", ".join(proposed[:10]) + (" …" if len(proposed) > 10 else "")
            self.add("WARNING", "APR002", -1, f"Tài liệu APPROVED nhưng còn mục Status Proposed: {shown}.")
        if self.open_p0:
            self.add("WARNING", "APR003", -1,
                     f"Tài liệu APPROVED nhưng còn câu hỏi P0 Open: {', '.join(self.open_p0)}.")

    def check_coverage(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        sec = self.section(27)
        if sec is None or self.na_info(sec)[0]:
            return counts
        seen: Set[int] = set()
        found_table = False
        for table in self.tables(sec.heading_idx + 1, sec.end_idx):
            ci, si = table.col("section"), table.col("status")
            if ci is None or si is None:
                continue
            found_table = True
            for idx, cells in table.rows:
                if len(cells) <= max(ci, si):
                    continue
                m = re.match(r"^(\d+)", clean_cell(cells[ci]))
                if not m:
                    continue
                seen.add(int(m.group(1)))
                status = norm_value(cells[si])
                counts[status or "(trống)"] = counts.get(status or "(trống)", 0) + 1
                if status not in COVERAGE_STATUS:
                    self.add("WARNING", "COV001", idx,
                             f"Coverage section {m.group(1)}: trạng thái '{status or '(trống)'}' không hợp lệ.")
        if not found_table:
            self.add("WARNING", "COV002", sec.heading_idx, "Section 27 không có bảng coverage (cột Section, Status).")
        else:
            missing = [str(n) for n in COVERAGE_SECTIONS if n not in seen]
            if missing:
                self.add("WARNING", "COV002", sec.heading_idx, f"Bảng coverage thiếu dòng cho section: {', '.join(missing)}.")
        return counts

    def check_traceability(self) -> None:
        sec = self.section(28)
        if sec is None or self.na_info(sec)[0]:
            return
        traced: Set[str] = set()
        for i in range(sec.heading_idx + 1, sec.end_idx):
            if self.is_prose(i):
                traced.update(ID_RE.findall(self.lines[i]))
        for b in self.blocks:
            if b.ident.split("-")[0] in REQ_PREFIXES and self.block_status(b) not in ("rejected", "superseded"):
                if b.ident not in traced:
                    self.add("WARNING", "TR001", b.heading_idx, f"{b.ident} chưa có trong ma trận truy vết (section 28).")
        for ident, where in self.defs.items():
            if ident.startswith("GOAL-") and ident not in traced:
                self.add("WARNING", "TR002", where[0], f"{ident} chưa có trong ma trận truy vết (section 28).")

    def check_ui(self) -> None:
        sec = self.section(13)
        if sec is None:
            return
        for i in range(sec.heading_idx + 1, sec.end_idx):
            if not self.is_prose(i):
                continue
            for m in HEX_RE.finditer(self.lines[i]):
                if len(m.group(1)) not in (3, 4, 6, 8):
                    self.add("WARNING", "UI001", i, f"Mã màu '#{m.group(1)}' không đúng định dạng HEX (3, 4, 6 hoặc 8 ký tự).")
        for table in self.tables(sec.heading_idx + 1, sec.end_idx):
            ti, si = table.col("type"), table.col("source")
            for idx, cells in table.rows:
                if not cells or not re.fullmatch(r"UXP-\d{3}", clean_cell(cells[0])):
                    continue
                uxp = clean_cell(cells[0])
                if si is None or si >= len(cells) or not clean_cell(cells[si]):
                    self.add("WARNING", "UI002", idx, f"{uxp} thiếu Source.")
                if ti is not None and ti < len(cells) and norm_value(cells[ti]) not in UXP_TYPES:
                    self.add("WARNING", "UI003", idx,
                             f"{uxp}: Type '{clean_cell(cells[ti])}' không hợp lệ (Constraint, Preference, Reference).")

    # ---------- chạy ----------
    def run(self) -> List[Finding]:
        if not self.text.strip():
            self.add("ERROR", "DOC001", -1, "File rỗng.")
            return self.findings
        self.scan_fences()
        self.scan_headings()
        self.check_sections()
        self.collect_definitions()
        self.check_ids()
        self.check_requirements()
        self.check_diagrams()
        tbd_count = self.check_placeholders()
        self.check_document_control()
        self.check_domain()
        self.check_questions()
        self.check_approval()
        coverage = self.check_coverage()
        self.check_traceability()
        self.check_ui()
        self.add_info(tbd_count, coverage)
        return self.findings

    def add_info(self, tbd_count: int, coverage: Dict[str, int]) -> None:
        if self.partial:
            self.add("INFO", "INF000", -1, "Chế độ --partial: bỏ kiểm tra đủ section; tham chiếu treo chỉ là WARNING.")
        counts: Dict[str, int] = {}
        for ident in self.defs:
            prefix = ident.split("-")[0]
            counts[prefix] = counts.get(prefix, 0) + 1
        order = ["GOAL", "FR", "BR", "DR", "IR", "UIR", "NFR", "US", "UC", "AC", "DIA", "ASM", "Q", "RISK", "DEC", "SRC", "UXP", "CR"]
        summary = ", ".join(f"{p}={counts[p]}" for p in order if p in counts) or "không có"
        self.add("INFO", "INF001", -1, f"Số ID đã định nghĩa: {summary}.")
        if self.q_counts:
            q = ", ".join(f"{k}={v}" for k, v in sorted(self.q_counts.items()))
            self.add("INFO", "INF002", -1, f"Câu hỏi theo Priority/Status: {q}.")
        self.add("INFO", "INF003", -1, f"Số dòng còn TBD/TODO (ngoài bảng coverage): {tbd_count}.")
        if coverage:
            c = ", ".join(f"{k}={v}" for k, v in sorted(coverage.items()))
            self.add("INFO", "INF004", -1, f"Coverage: {c}.")


def validate_text(text: str, partial: bool = False) -> List[Finding]:
    """Kiểm tra nội dung SRS; trả về danh sách Finding. Không ghi file."""
    return Validator(text, partial=partial).run()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_srs.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", help="Đường dẫn file SRS Markdown cần kiểm tra")
    parser.add_argument("--partial", action="store_true", help="Trích đoạn SRS: bỏ kiểm tra đủ section")
    parser.add_argument("--ascii", action="store_true", help="In kết quả không dấu")
    parser.add_argument("--version", action="version", version=f"validate_srs.py {TOOL_VERSION}")
    args = parser.parse_args(argv)

    out = to_ascii if args.ascii else (lambda s: s)
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

    try:
        with open(args.path, "rb") as fh:
            raw = fh.read()
        text = raw.decode("utf-8-sig")
    except FileNotFoundError:
        print(out(f"ERROR IO001 L0: Không tìm thấy file: {args.path}"))
        return 2
    except IsADirectoryError:
        print(out(f"ERROR IO001 L0: Đường dẫn là thư mục, không phải file: {args.path}"))
        return 2
    except PermissionError:
        print(out(f"ERROR IO001 L0: Không có quyền đọc file: {args.path}"))
        return 2
    except UnicodeDecodeError:
        print(out(f"ERROR IO001 L0: File không phải UTF-8: {args.path}"))
        return 2
    except OSError as exc:
        print(out(f"ERROR IO001 L0: Không đọc được file {args.path}: {exc}"))
        return 2

    findings = validate_text(text, partial=args.partial)
    for f in sorted(findings, key=lambda f: (LEVEL_ORDER[f.level], f.line, f.code)):
        print(out(f.render()))
    errors = sum(1 for f in findings if f.level == "ERROR")
    warnings = sum(1 for f in findings if f.level == "WARNING")
    infos = sum(1 for f in findings if f.level == "INFO")
    print(out(f"Tổng kết: {errors} ERROR, {warnings} WARNING, {infos} INFO — {args.path}"))
    print(out(DISCLAIMER))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
