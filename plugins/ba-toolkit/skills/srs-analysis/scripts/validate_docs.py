#!/usr/bin/env python3
"""Kiểm tra cấu trúc 3 tài liệu BRD / SRS / Diagrams theo quy ước skill srs-analysis.

Script chỉ ĐỌC các file đầu vào, không sửa. Nó kiểm tra cấu trúc và lỗi cơ học:
section bắt buộc theo đúng loại tài liệu, ID trùng hoặc sai định dạng, tham
chiếu tới ID chưa định nghĩa (kể cả tham chiếu xuyên 3 file), trường bắt buộc
của requirement, acceptance criteria, placeholder/TBD, traceability, bảng
coverage, khối sơ đồ Mermaid, nhất quán trạng thái phê duyệt.

Ba file dùng chung một không gian ID: một ID được định nghĩa ở đúng một chỗ
trong cả 3 file, có thể được tham chiếu từ file khác.

Script KHÔNG chứng minh nội dung nghiệp vụ đúng và KHÔNG thay thế việc review
của BA và stakeholder. Quy ước được kiểm tra nằm ở references/conventions.md,
references/brd-template.md, references/srs-template.md,
references/diagrams-template.md.

Cách dùng:
    python3 validate_docs.py --brd docs/brd/brd.md --srs docs/srs/srs.md --diagrams docs/diagrams/diagrams.md
    python3 validate_docs.py --srs docs/srs/srs.md --diagrams docs/diagrams/diagrams.md
    python3 validate_docs.py --partial --srs examples/sample-srs-excerpt.md
    python3 validate_docs.py --ascii --brd docs/brd/brd.md --srs docs/srs/srs.md --diagrams docs/diagrams/diagrams.md

Tùy chọn:
    --brd PATH        Đường dẫn file BRD.
    --srs PATH        Đường dẫn file SRS.
    --diagrams PATH   Đường dẫn file sơ đồ.
    --partial         Trích đoạn: bỏ kiểm tra đủ section; tham chiếu treo chỉ là WARNING.
    --ascii           In kết quả không dấu (cho console không hiển thị được UTF-8).

Phải cung cấp ít nhất một trong --brd/--srs/--diagrams. File không được cung
cấp sẽ bị bỏ qua (WARNING), và tham chiếu treo tới ID lẽ ra thuộc file đó chỉ
là WARNING, không phải ERROR (giống hành vi --partial).

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
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

TOOL_VERSION = "2.0.0"

DISCLAIMER = (
    "Lưu ý: validator chỉ kiểm tra cấu trúc và lỗi cơ học; không chứng minh nội dung "
    "nghiệp vụ đúng và không thay thế review của BA và stakeholder."
)

# ---------------------------------------------------------------------------
# Khung section theo từng loại tài liệu. "Document Control" là một bảng
# | Field | Value | ở PHẦN MỞ ĐẦU (trước section 1), không phải section đánh
# số, để section 1 đúng là "Introduction — Giới thiệu" như chuẩn SRS yêu cầu.
# ---------------------------------------------------------------------------

Sections = List[Tuple[int, str, bool]]  # (số, English title, được phép Not applicable)

BRD_SECTIONS: Sections = [
    (1, "Introduction", False),
    (2, "Business Context and Problem Statement", False),
    (3, "Goals and Success Metrics", False),
    (4, "Scope", False),
    (5, "Stakeholders and Users", False),
    (6, "Glossary", True),
    (7, "Assumptions, Constraints and Dependencies", False),
    (8, "High-Level Business Processes", True),
    (9, "Risks", False),
    (10, "Approval Record", False),
]

SRS_SECTIONS: Sections = [
    (1, "Introduction", False),
    (2, "High-Level Requirements", False),
    (3, "Functional Requirements", False),
    (4, "Non-Functional Requirements", False),
    (5, "Security Requirements", False),
    (6, "Other Requirements and Appendix", False),
]

DIAGRAMS_SECTIONS: Sections = [
    (1, "Diagrams", False),
]

FILE_KINDS: Dict[str, Sections] = {"BRD": BRD_SECTIONS, "SRS": SRS_SECTIONS, "DIAGRAMS": DIAGRAMS_SECTIONS}

# Tiền tố định nghĩa ở ô đầu một dòng bảng. Để không nhầm bảng Traceability
# Matrix (chỉ THAM CHIẾU GOAL-/SRC- ở cột đầu) thành nơi ĐỊNH NGHĨA, một bảng
# chỉ được coi là "sổ đăng ký" của một tiền tố khi header của nó chứa đủ các
# từ khóa đặc trưng dưới đây — quét toàn file, không theo số section cụ thể.
TABLE_PREFIXES: Tuple[str, ...] = ("GOAL", "ASM", "RISK", "Q", "DEC", "SRC", "UXP")
TABLE_HEADER_HINTS: Dict[str, Tuple[str, ...]] = {
    "GOAL": ("goal", "success metric"),
    "ASM": ("assumption",),
    "RISK": ("risk", "impact", "likelihood"),
    "Q": ("question", "ask whom"),
    "DEC": ("decision", "decided by"),
    "SRC": ("type", "provided by"),
    "UXP": ("type", "description", "source"),
}
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
    file_tag: str
    line: int
    message: str

    def render(self) -> str:
        where = f"{self.file_tag}:L{self.line}" if self.file_tag else f"L{self.line}"
        return f"{self.level} {self.code} {where}: {self.message}"


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
        for i, h in enumerate(self.header):
            if any(name in h for name in names):
                return i
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


@dataclass
class DefRecord:
    file_tag: str
    line: int


class FileValidator:
    """Quét và kiểm tra cấu trúc của MỘT file (BRD, SRS, hoặc Diagrams)."""

    def __init__(self, kind: str, file_tag: str, text: str, partial: bool = False) -> None:
        self.kind = kind
        self.file_tag = file_tag
        self.sections_spec = FILE_KINDS[kind]
        self.section_by_num: Dict[int, Tuple[str, bool]] = {n: (t, na) for n, t, na in self.sections_spec}
        self.text = text
        self.lines = text.splitlines()
        self.partial = partial
        self.findings: List[Finding] = []
        n = len(self.lines)
        self.code = [False] * n
        self.mermaid = [False] * n
        self.mermaid_blocks: List[Tuple[int, int]] = []
        self.sections: List[Section] = []
        self.blocks: List[Block] = []
        self.preamble_end = n
        self.local_defs: Dict[str, List[int]] = {}
        self.ac_defs: List[Tuple[str, int]] = []
        self.doc_status: Optional[str] = None
        self.doc_version: Optional[str] = None
        self.q_counts: Dict[str, int] = {}
        self.open_questions: List[str] = []  # mọi câu hỏi Status=Open, bất kể Priority (P0/P1/P2)
        self.coverage_counts: Dict[str, int] = {}

    def add(self, level: str, code: str, idx: int, message: str) -> None:
        self.findings.append(Finding(level, code, self.file_tag, idx + 1 if idx >= 0 else 0, message))

    def is_prose(self, idx: int) -> bool:
        return not self.code[idx] and not self.mermaid[idx]

    def section(self, num: int) -> Optional[Section]:
        for s in self.sections:
            if s.num == num:
                return s
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

    def all_tables(self) -> List[Table]:
        return self.tables(0, len(self.lines))

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

    def block_at(self, idx: int) -> Optional[Block]:
        for b in self.blocks:
            if b.heading_idx < idx < b.end_idx:
                return b
        return None

    def block_status(self, block: Block) -> str:
        fields = self.block_fields(block)
        return norm_value(fields["status"][0]) if "status" in fields else ""

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
        self.preamble_end = h2[0][0] if h2 else n
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

    # ---------- kiểm tra cấu trúc ----------
    def check_sections(self) -> None:
        seen: Dict[int, int] = {}
        for sec in self.sections:
            if sec.num is None or sec.num not in self.section_by_num:
                self.add("WARNING", "SEC007", sec.heading_idx,
                         f"Section H2 không thuộc danh sách chuẩn cho {self.kind}: '{self.lines[sec.heading_idx].strip()}'.")
                continue
            expected, _ = self.section_by_num[sec.num]
            if english_title(sec.raw_title) != expected.lower():
                self.add("ERROR", "SEC002", sec.heading_idx,
                         f"Section {sec.num} có tên '{sec.raw_title.strip()}'; mong đợi '## {sec.num}. {expected} — <tiếng Việt>'.")
            if sec.num in seen:
                self.add("WARNING", "SEC003", sec.heading_idx,
                         f"Section {sec.num} xuất hiện lần nữa (lần đầu ở L{seen[sec.num] + 1}).")
            else:
                seen[sec.num] = sec.heading_idx
        if not self.partial:
            for num, title, _ in self.sections_spec:
                if num not in seen:
                    self.add("ERROR", "SEC001", -1, f"Thiếu section bắt buộc: '## {num}. {title} — <tiếng Việt>'.")
        for sec in self.sections:
            if sec.num is None or sec.num not in self.section_by_num:
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
                if not self.section_by_num[sec.num][1]:
                    self.add("WARNING", "SEC006", sec.heading_idx + 1,
                             f"Section {sec.num} ({self.section_by_num[sec.num][0]}) không được ghi Not applicable.")

    def collect_definitions(self) -> None:
        for b in self.blocks:
            self.local_defs.setdefault(b.ident, []).append(b.heading_idx)
        for table in self.all_tables():
            header_text = " ".join(table.header)
            owned = [p for p in TABLE_PREFIXES if all(h in header_text for h in TABLE_HEADER_HINTS[p])]
            if not owned:
                continue
            for idx, cells in table.rows:
                if not cells:
                    continue
                first = clean_cell(cells[0])
                if ID_FULL_RE.fullmatch(first) and first.split("-")[0] in owned:
                    self.local_defs.setdefault(first, []).append(idx)
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            m = AC_DEF_RE.match(line)
            if m:
                ac = m.group(1)
                self.ac_defs.append((ac, i))
                self.local_defs.setdefault(ac, []).append(i)

    def local_duplicate_check(self) -> None:
        for ident, where in self.local_defs.items():
            if len(where) > 1:
                first = where[0] + 1
                for idx in where[1:]:
                    self.add("ERROR", "ID001", idx, f"ID {ident} được định nghĩa lại trong cùng file (lần đầu ở L{first}).")

    def malformed_tokens(self) -> None:
        malformed: Dict[str, int] = {}
        for i, line in enumerate(self.lines):
            if not (self.is_prose(i) or self.mermaid[i]):
                continue
            for m in TOKEN_RE.finditer(line):
                tok = m.group(0)
                if any(ch.isdigit() for ch in tok) and not ID_FULL_RE.fullmatch(tok) and tok not in malformed:
                    malformed[tok] = i
        for tok, idx in malformed.items():
            self.add("WARNING", "ID003", idx, f"ID sai định dạng: '{tok}' (xem references/conventions.md).")

    def collect_refs(self) -> Dict[str, List[int]]:
        refs: Dict[str, List[int]] = {}
        for i, line in enumerate(self.lines):
            if not (self.is_prose(i) or self.mermaid[i]):
                continue
            for m in ID_RE.finditer(line):
                refs.setdefault(m.group(0), []).append(i)
        return refs

    def check_ac_parents(self) -> None:
        for ac, idx in self.ac_defs:
            parent = ac[3:-3]
            owner = self.block_at(idx)
            if owner is not None and owner.ident != parent:
                self.add("WARNING", "ID004", idx, f"{ac} phải được định nghĩa trong khối {parent}, hiện nằm ở {owner.ident}.")

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

    def has_context_diagram(self) -> bool:
        for b in self.blocks:
            if b.ident.startswith("DIA-") and "context" in self.block_fields(b).get("type", ("", 0))[0].lower():
                return True
        return False

    def check_placeholders(self) -> int:
        tbd_count = 0
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            stripped = INLINE_CODE_RE.sub("", line)
            m = TBD_RE.search(stripped)
            if m:
                tbd_count += 1
                self.add("WARNING", "PH001", i, f"Còn '{m.group(1)}': cần giải quyết hoặc gắn Q- và người trả lời.")
            b = BRACKET_RE.search(stripped)
            if b:
                self.add("WARNING", "PH002", i, f"Có vẻ là placeholder chưa điền: '[{b.group(1)}]'.")
        return tbd_count

    def check_document_control(self) -> None:
        fields: Dict[str, Tuple[str, int]] = {}
        for table in self.tables(0, self.preamble_end):
            if "field" in table.header and "value" in table.header:
                fi, vi = table.header.index("field"), table.header.index("value")
                for idx, cells in table.rows:
                    if len(cells) > max(fi, vi):
                        fields[clean_cell(cells[fi]).lower()] = (clean_cell(cells[vi]), idx)
        if not fields:
            self.add("WARNING", "DOC003", -1, "Không tìm thấy bảng Document Control (| Field | Value |) ở đầu file, trước section 1.")
            return
        status_raw, status_idx = fields.get("status", ("", 0))
        status = re.sub(r"\s+[-–—]\s+", " — ", status_raw.upper())
        status = re.sub(r"\s+", " ", status).strip()
        if status not in DOC_STATUS:
            self.add("WARNING", "APR004", status_idx,
                     f"Status tài liệu '{status_raw}' không hợp lệ (DRAFT — NOT APPROVED, APPROVED, ON HOLD).")
        else:
            self.doc_status = status
        version_raw, version_idx = fields.get("document version", ("", 0))
        vm = VERSION_RE.match(version_raw)
        if not vm:
            self.add("WARNING", "APR005", version_idx, f"Document version '{version_raw}' không đúng dạng X.Y.")
        else:
            self.doc_version = f"{int(vm.group(1))}.{int(vm.group(2))}"

    def check_questions(self) -> None:
        for table in self.all_tables():
            pi, si = table.col("priority"), table.col("status")
            if pi is None or si is None:
                continue
            for idx, cells in table.rows:
                if not cells:
                    continue
                qid = clean_cell(cells[0])
                if not re.fullmatch(r"Q-\d{3}", qid):
                    continue
                prio = norm_value(cells[pi]) if pi < len(cells) else ""
                stat = norm_value(cells[si]) if si < len(cells) else ""
                problems = []
                if prio not in Q_PRIORITY:
                    problems.append(f"Priority '{prio or '(trống)'}'")
                if stat not in Q_STATUS:
                    problems.append(f"Status '{stat or '(trống)'}'")
                if problems:
                    self.add("WARNING", "Q001", idx, f"{qid}: {', '.join(problems)} không hợp lệ.")
                key = f"{prio.upper() or '?'} {stat or '?'}"
                self.q_counts[key] = self.q_counts.get(key, 0) + 1
                if stat == "open":
                    self.open_questions.append(qid)

    def proposed_active_blocks(self) -> List[str]:
        return [b.ident for b in self.blocks
                if b.ident.split("-")[0] in REQ_PREFIXES + ("US", "UC", "DIA") and self.block_status(b) == "proposed"]

    def find_approval_table(self) -> Optional[Table]:
        for table in self.all_tables():
            vi, di = table.col("version"), table.col("decision")
            if vi is not None and di is not None:
                return table
        return None

    def check_coverage(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        found = False
        for table in self.all_tables():
            si = table.col("status")
            topic_i = table.col("topic", "section")
            if si is None or topic_i is None:
                continue
            found = True
            for idx, cells in table.rows:
                if len(cells) <= si:
                    continue
                status = norm_value(cells[si])
                counts[status or "(trống)"] = counts.get(status or "(trống)", 0) + 1
                if status not in COVERAGE_STATUS:
                    self.add("WARNING", "COV001", idx, f"Elicitation coverage: trạng thái '{status or '(trống)'}' không hợp lệ.")
        if self.kind == "SRS" and not found:
            self.add("WARNING", "COV002", -1, "Không tìm thấy bảng Elicitation Coverage (cột Topic/Section, Status) trong SRS.")
        return counts

    def traced_ids(self) -> Set[str]:
        traced: Set[str] = set()
        for table in self.all_tables():
            ri = table.col("requirement")
            gi = table.col("goal / source", "goal")
            if ri is None and gi is None:
                continue
            for _, cells in table.rows:
                for i in (ri, gi):
                    if i is not None and i < len(cells):
                        traced.update(ID_RE.findall(cells[i]))
        return traced

    def check_ui(self) -> None:
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            for m in HEX_RE.finditer(line):
                if len(m.group(1)) not in (3, 4, 6, 8):
                    self.add("WARNING", "UI001", i, f"Mã màu '#{m.group(1)}' không đúng định dạng HEX (3, 4, 6 hoặc 8 ký tự).")
        for table in self.all_tables():
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

    def run_local(self) -> None:
        if not self.text.strip():
            self.add("ERROR", "DOC001", -1, "File rỗng.")
            return
        self.scan_fences()
        self.scan_headings()
        self.check_sections()
        self.collect_definitions()
        self.local_duplicate_check()
        self.malformed_tokens()
        self.check_ac_parents()
        self.check_requirements()
        self.check_diagrams()
        self.check_placeholders()
        self.check_document_control()
        self.check_questions()
        self.coverage_counts = self.check_coverage()
        self.check_ui()


def validate_project(
    sources: Dict[str, str], partial: bool = False
) -> Tuple[List[Finding], Dict[str, object]]:
    """Kiểm tra 1-3 file cùng lúc. `sources`: {"BRD": text, "SRS": text, "DIAGRAMS": text}."""
    all_findings: List[Finding] = []
    validators: Dict[str, FileValidator] = {}
    missing_level = "WARNING" if (partial or len(sources) < 3) else "ERROR"

    for kind in ("BRD", "SRS", "DIAGRAMS"):
        if kind not in sources:
            all_findings.append(Finding("WARNING", "IO002", kind, 0, f"File {kind} không được cung cấp; bỏ qua kiểm tra cấu trúc của file này."))
            continue
        fv = FileValidator(kind, kind, sources[kind], partial=partial)
        fv.run_local()
        validators[kind] = fv
        all_findings.extend(fv.findings)

    # ---- hợp nhất ID định nghĩa và kiểm tra trùng xuyên file ----
    global_defs: Dict[str, List[DefRecord]] = {}
    for kind, fv in validators.items():
        for ident, lines in fv.local_defs.items():
            for ln in lines:
                global_defs.setdefault(ident, []).append(DefRecord(kind, ln + 1))
    for ident, records in global_defs.items():
        if len(records) > 1:
            # Trùng trong cùng file đã báo ở local_duplicate_check (ID001); ở đây chỉ báo trùng GIỮA các file khác nhau.
            kinds = {r.file_tag for r in records}
            if len(kinds) > 1:
                first = records[0]
                for r in records[1:]:
                    if r.file_tag != first.file_tag:
                        all_findings.append(Finding(
                            "ERROR", "ID001", r.file_tag, r.line,
                            f"ID {ident} được định nghĩa lại (đã định nghĩa ở {first.file_tag}:L{first.line}).",
                        ))

    # ---- tham chiếu xuyên file ----
    for kind, fv in validators.items():
        refs = fv.collect_refs()
        for ident, where in refs.items():
            if ident not in global_defs:
                extra = f" (xuất hiện {len(where)} lần)" if len(where) > 1 else ""
                all_findings.append(Finding(missing_level, "ID002", kind, where[0] + 1,
                                             f"Tham chiếu tới ID chưa được định nghĩa ở file nào: {ident}{extra}."))
        for ac, idx in fv.ac_defs:
            parent = ac[3:-3]
            if parent not in global_defs:
                all_findings.append(Finding(missing_level, "ID002", kind, idx + 1,
                                             f"{ac} thuộc {parent}, nhưng {parent} chưa được định nghĩa ở file nào."))

    # ---- sơ đồ Context bắt buộc (nếu có file diagrams) ----
    if "DIAGRAMS" in validators:
        if not any(fv.has_context_diagram() for fv in validators.values()):
            all_findings.append(Finding("WARNING", "DIA005", "DIAGRAMS", 0,
                                         "Chưa có sơ đồ Type: Context (bắt buộc) trong diagrams.md."))

    # ---- nhất quán version/status giữa các file đang có ----
    present = list(validators.values())
    versions = {fv.doc_version for fv in present if fv.doc_version}
    statuses = {fv.doc_status for fv in present if fv.doc_status}
    if len(versions) > 1:
        all_findings.append(Finding("WARNING", "DOC004", "-", 0,
                                     f"Document version không khớp giữa các file: {', '.join(sorted(versions))}."))
    if len(statuses) > 1:
        all_findings.append(Finding("WARNING", "DOC005", "-", 0,
                                     f"Document status không khớp giữa các file: {', '.join(sorted(statuses))}."))

    # ---- traceability (toàn cục): mọi FR/BR/DR/IR/UIR/NFR còn hiệu lực và mọi GOAL phải được truy vết ----
    traced: Set[str] = set()
    if "SRS" in validators:
        traced |= validators["SRS"].traced_ids()
    for kind, fv in validators.items():
        for b in fv.blocks:
            if b.ident.split("-")[0] in REQ_PREFIXES and fv.block_status(b) not in ("rejected", "superseded"):
                if b.ident not in traced:
                    all_findings.append(Finding("WARNING", "TR001", kind, b.heading_idx + 1,
                                                 f"{b.ident} chưa có trong ma trận truy vết (SRS, Other Requirements and Appendix)."))
    for ident, records in global_defs.items():
        if ident.startswith("GOAL-") and ident not in traced:
            r = records[0]
            all_findings.append(Finding("WARNING", "TR002", r.file_tag, r.line,
                                         f"{ident} chưa có trong ma trận truy vết (SRS, Other Requirements and Appendix)."))

    # ---- gate phê duyệt (toàn cục) ----
    approved = "APPROVED" in statuses
    if approved:
        srs = validators.get("SRS")
        matched = False
        if srs is not None and srs.doc_version is not None:
            approval_table = srs.find_approval_table()
            if approval_table is not None:
                vi, di = approval_table.col("version"), approval_table.col("decision")
                for _, cells in approval_table.rows:
                    if len(cells) <= max(vi, di):
                        continue
                    vm = VERSION_RE.match(clean_cell(cells[vi]))
                    version = f"{int(vm.group(1))}.{int(vm.group(2))}" if vm else ""
                    decision = clean_cell(cells[di]).upper()
                    if version == srs.doc_version and decision in ("APPROVE", "DUYỆT"):
                        matched = True
        if not matched:
            ver = srs.doc_version if srs else "?"
            all_findings.append(Finding("WARNING", "APR001", "SRS", 0,
                                         f"Tài liệu APPROVED nhưng Approval Record (SRS) không có dòng APPROVE cho version {ver}."))
        proposed_all: List[str] = []
        for kind, fv in validators.items():
            proposed_all.extend(f"{kind}:{ident}" for ident in fv.proposed_active_blocks())
        if proposed_all:
            shown = ", ".join(proposed_all[:10]) + (" …" if len(proposed_all) > 10 else "")
            all_findings.append(Finding("WARNING", "APR002", "-", 0, f"Tài liệu APPROVED nhưng còn mục Status Proposed: {shown}."))
        open_questions_all: List[str] = []
        for kind, fv in validators.items():
            open_questions_all.extend(fv.open_questions)
        if open_questions_all:
            all_findings.append(Finding("WARNING", "APR003", "-", 0,
                                         f"Tài liệu APPROVED nhưng còn câu hỏi Open (bất kỳ mức P0/P1/P2): {', '.join(open_questions_all)}."))

    info: Dict[str, object] = {"validators": validators, "global_defs": global_defs, "partial": partial}
    return all_findings, info


def build_info_findings(info: Dict[str, object]) -> List[Finding]:
    validators: Dict[str, FileValidator] = info["validators"]  # type: ignore[assignment]
    global_defs: Dict[str, List[DefRecord]] = info["global_defs"]  # type: ignore[assignment]
    findings: List[Finding] = []
    if info.get("partial"):
        findings.append(Finding("INFO", "INF000", "-", 0, "Chế độ --partial: bỏ kiểm tra đủ section; tham chiếu treo chỉ là WARNING."))
    counts: Dict[str, int] = {}
    for ident in global_defs:
        prefix = ident.split("-")[0]
        counts[prefix] = counts.get(prefix, 0) + 1
    order = ["GOAL", "FR", "BR", "DR", "IR", "UIR", "NFR", "US", "UC", "AC", "DIA", "ASM", "Q", "RISK", "DEC", "SRC", "UXP", "CR"]
    summary = ", ".join(f"{p}={counts[p]}" for p in order if p in counts) or "không có"
    findings.append(Finding("INFO", "INF001", "-", 0, f"Số ID đã định nghĩa (toàn dự án): {summary}."))
    q_counts: Dict[str, int] = {}
    tbd_total = 0
    for fv in validators.values():
        for k, v in fv.q_counts.items():
            q_counts[k] = q_counts.get(k, 0) + v
        tbd_total += sum(1 for f in fv.findings if f.code == "PH001")
    if q_counts:
        q = ", ".join(f"{k}={v}" for k, v in sorted(q_counts.items()))
        findings.append(Finding("INFO", "INF002", "-", 0, f"Câu hỏi theo Priority/Status: {q}."))
    findings.append(Finding("INFO", "INF003", "-", 0, f"Số dòng còn TBD/TODO (toàn dự án): {tbd_total}."))
    coverage_all: Dict[str, int] = {}
    for fv in validators.values():
        for k, v in fv.coverage_counts.items():
            coverage_all[k] = coverage_all.get(k, 0) + v
    if coverage_all:
        c = ", ".join(f"{k}={v}" for k, v in sorted(coverage_all.items()))
        findings.append(Finding("INFO", "INF004", "-", 0, f"Elicitation coverage: {c}."))
    present = ", ".join(sorted(validators.keys())) or "không có"
    findings.append(Finding("INFO", "INF005", "-", 0, f"File đã kiểm tra: {present}."))
    return findings


def read_file(path: str) -> str:
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8-sig")


def main(argv: Optional[List[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

    parser = argparse.ArgumentParser(
        prog="validate_docs.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--brd", help="Đường dẫn file BRD Markdown")
    parser.add_argument("--srs", help="Đường dẫn file SRS Markdown")
    parser.add_argument("--diagrams", help="Đường dẫn file sơ đồ Markdown")
    parser.add_argument("--partial", action="store_true", help="Trích đoạn: bỏ kiểm tra đủ section")
    parser.add_argument("--ascii", action="store_true", help="In kết quả không dấu")
    parser.add_argument("--version", action="version", version=f"validate_docs.py {TOOL_VERSION}")
    args = parser.parse_args(argv)

    out = to_ascii if args.ascii else (lambda s: s)

    requested = {"BRD": args.brd, "SRS": args.srs, "DIAGRAMS": args.diagrams}
    if not any(requested.values()):
        print(out("ERROR IO001 -: Phải cung cấp ít nhất một trong --brd / --srs / --diagrams."))
        return 2

    sources: Dict[str, str] = {}
    for kind, path in requested.items():
        if path is None:
            continue
        try:
            sources[kind] = read_file(path)
        except FileNotFoundError:
            print(out(f"ERROR IO001 {kind}: Không tìm thấy file: {path}"))
            return 2
        except IsADirectoryError:
            print(out(f"ERROR IO001 {kind}: Đường dẫn là thư mục, không phải file: {path}"))
            return 2
        except PermissionError:
            print(out(f"ERROR IO001 {kind}: Không có quyền đọc file: {path}"))
            return 2
        except UnicodeDecodeError:
            print(out(f"ERROR IO001 {kind}: File không phải UTF-8: {path}"))
            return 2
        except OSError as exc:
            print(out(f"ERROR IO001 {kind}: Không đọc được file {path}: {exc}"))
            return 2

    findings, info = validate_project(sources, partial=args.partial)
    findings.extend(build_info_findings(info))
    for f in sorted(findings, key=lambda f: (LEVEL_ORDER[f.level], f.file_tag, f.line, f.code)):
        print(out(f.render()))
    errors = sum(1 for f in findings if f.level == "ERROR")
    warnings = sum(1 for f in findings if f.level == "WARNING")
    infos = sum(1 for f in findings if f.level == "INFO")
    print(out(f"Tổng kết: {errors} ERROR, {warnings} WARNING, {infos} INFO."))
    print(out(DISCLAIMER))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
