"""Unit test cho skills/srs-analysis/scripts/validate_docs.py.

Chạy từ thư mục gốc của plugin:
    python3 -m unittest discover -s tests -v

Chỉ dùng thư viện chuẩn. Mỗi quy tắc có ít nhất một ca dương (phát hiện lỗi)
và dựa trên 3 fixture hợp lệ (BRD/SRS/Diagrams) làm ca âm (không báo lỗi).
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "srs-analysis" / "scripts" / "validate_docs.py"
BRD_TEMPLATE = ROOT / "skills" / "srs-analysis" / "references" / "brd-template.md"
SRS_TEMPLATE = ROOT / "skills" / "srs-analysis" / "references" / "srs-template.md"
DIA_TEMPLATE = ROOT / "skills" / "srs-analysis" / "references" / "diagrams-template.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID_BRD = (FIXTURES / "valid-minimal-brd.md").read_text(encoding="utf-8")
VALID_SRS = (FIXTURES / "valid-minimal-srs.md").read_text(encoding="utf-8")
VALID_DIA = (FIXTURES / "valid-minimal-diagrams.md").read_text(encoding="utf-8")
SAMPLE = ROOT / "examples" / "sample-srs-excerpt.md"

_spec = importlib.util.spec_from_file_location("validate_docs", SCRIPT)
vd = importlib.util.module_from_spec(_spec)
sys.modules["validate_docs"] = vd  # dataclass cần module có trong sys.modules
assert _spec.loader is not None
_spec.loader.exec_module(vd)


def codes(brd=None, srs=None, diagrams=None, partial: bool = False, level: str | None = None) -> list:
    sources = {
        "BRD": VALID_BRD if brd is None else brd,
        "SRS": VALID_SRS if srs is None else srs,
        "DIAGRAMS": VALID_DIA if diagrams is None else diagrams,
    }
    findings, _ = vd.validate_project(sources, partial=partial)
    return [f.code for f in findings if level is None or f.level == level]


def skeleton_codes(text: str, kind: str, level: str | None = None) -> list:
    findings, _ = vd.validate_project({kind: text})
    return [f.code for f in findings if level is None or f.level == level]


def replace_once(text: str, old: str, new: str) -> str:
    assert old in text, f"Không tìm thấy đoạn cần thay: {old!r}"
    return text.replace(old, new, 1)


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


class TestValidFixtures(unittest.TestCase):
    def test_valid_project_has_no_error_or_warning(self):
        findings, _ = vd.validate_project({"BRD": VALID_BRD, "SRS": VALID_SRS, "DIAGRAMS": VALID_DIA})
        found = [f for f in findings if f.level in ("ERROR", "WARNING")]
        self.assertEqual(found, [], "\n".join(f.render() for f in found))

    def _skeleton(self, template_path: Path) -> str:
        text = template_path.read_text(encoding="utf-8")
        m = re.search(r"~~~~markdown\n(.*?)\n~~~~", text, re.S)
        self.assertIsNotNone(m, f"Không tìm thấy khung trong {template_path.name}")
        return m.group(1)

    def test_brd_template_skeleton_has_no_error(self):
        self.assertEqual(skeleton_codes(self._skeleton(BRD_TEMPLATE), "BRD", level="ERROR"), [])

    def test_srs_template_skeleton_has_no_error(self):
        self.assertEqual(skeleton_codes(self._skeleton(SRS_TEMPLATE), "SRS", level="ERROR"), [])

    def test_diagrams_template_skeleton_has_no_error(self):
        self.assertEqual(skeleton_codes(self._skeleton(DIA_TEMPLATE), "DIAGRAMS", level="ERROR"), [])

    def test_sample_excerpt_partial_has_no_error(self):
        self.assertTrue(SAMPLE.exists(), "Thiếu examples/sample-srs-excerpt.md")
        text = SAMPLE.read_text(encoding="utf-8")
        findings, _ = vd.validate_project({"SRS": text}, partial=True)
        self.assertEqual([f.code for f in findings if f.level == "ERROR"], [])


class TestSections(unittest.TestCase):
    def test_empty_file(self):
        findings, _ = vd.validate_project({"SRS": "   \n"})
        self.assertIn("DOC001", [f.code for f in findings])

    def test_missing_section(self):
        text = re.sub(r"## 5\. Security.*?(?=## 6\.)", "", VALID_SRS, flags=re.S)
        self.assertIn("SEC001", codes(srs=text, level="ERROR"))

    def test_missing_section_ignored_in_partial(self):
        text = re.sub(r"## 5\. Security.*?(?=## 6\.)", "", VALID_SRS, flags=re.S)
        self.assertNotIn("SEC001", codes(srs=text, partial=True))

    def test_title_mismatch(self):
        text = replace_once(VALID_SRS, "## 4. Non-Functional Requirements — Yêu cầu phi chức năng", "## 4. Phi chức năng")
        self.assertIn("SEC002", codes(srs=text, level="ERROR"))

    def test_vietnamese_part_can_change(self):
        text = replace_once(VALID_SRS, "## 4. Non-Functional Requirements — Yêu cầu phi chức năng",
                             "## 4. Non-Functional Requirements — Yêu cầu chất lượng")
        self.assertNotIn("SEC002", codes(srs=text))

    def test_duplicate_section(self):
        text = VALID_SRS + "\n## 4. Non-Functional Requirements — Yêu cầu phi chức năng\n\nThêm.\n"
        self.assertIn("SEC003", codes(srs=text))

    def test_empty_section(self):
        # SEC004 chỉ xét độ rỗng ở cấp section H2; xóa toàn bộ nội dung §2 (một đoạn ngắn, không section con).
        text = re.sub(
            r"(## 2\. High-Level Requirements — Yêu cầu mức độ tổng thể\n\n).*?(?=## 3\.)",
            r"\1", VALID_SRS, flags=re.S,
        )
        self.assertIn("SEC004", codes(srs=text))

    def test_na_without_reason(self):
        # BRD §6 Glossary cho phép Not applicable; test ở cấp H2 (không phải sub-heading trong §6 SRS).
        text = re.sub(
            r"(## 6\. Glossary — Thuật ngữ nghiệp vụ\n\n).*?(?=## 7\.)",
            r"\1Not applicable\n\n", VALID_BRD, flags=re.S,
        )
        self.assertIn("SEC005", codes(brd=text))

    def test_na_not_allowed(self):
        text = re.sub(r"(## 4\. Non-Functional Requirements — Yêu cầu phi chức năng\n).*?(?=## 5\.)",
                      r"\1\nNot applicable — không cần.\n\n", VALID_SRS, flags=re.S)
        self.assertIn("SEC006", codes(srs=text))

    def test_unknown_h2(self):
        text = VALID_SRS + "\n## Ghi chú thêm\n\nNội dung.\n"
        self.assertIn("SEC007", codes(srs=text))

    def test_unclosed_fence(self):
        text = VALID_SRS + "\n```text\nchưa đóng\n"
        self.assertIn("DOC002", codes(srs=text))

    def test_document_control_missing(self):
        text = VALID_SRS.split("## 1. Introduction", 1)[1]
        text = "## 1. Introduction" + text
        self.assertIn("DOC003", codes(srs=text))


class TestIds(unittest.TestCase):
    def test_duplicate_definition_same_file(self):
        text = replace_once(VALID_SRS, "### Business Rules", "### FR-001 — Trùng\n- **Statement:** x\n\n### Business Rules")
        self.assertIn("ID001", codes(srs=text, level="ERROR"))

    def test_duplicate_definition_cross_file(self):
        text = replace_once(VALID_SRS, "### FR-001 —", "### FR-001-DUP —")  # tránh trùng không mong muốn
        # ASM-001 được định nghĩa ở BRD; thêm định nghĩa trùng ở SRS qua bảng Assumptions giả.
        srs_with_dup = VALID_SRS.replace(
            "### Open Questions",
            "### Assumptions (trùng cố ý)\n\n| ID | Assumption | Source | Confirm with | Status |\n"
            "|---|---|---|---|---|\n| ASM-001 | Trùng | SRC-001 | X | Open |\n\n### Open Questions",
            1,
        )
        self.assertIn("ID001", codes(srs=srs_with_dup, level="ERROR"))

    def test_dangling_reference(self):
        text = replace_once(VALID_SRS, "- **Related:** UC-001, DR-001", "- **Related:** UC-001, DR-001, FR-099")
        self.assertIn("ID002", codes(srs=text, level="ERROR"))

    def test_dangling_reference_is_warning_in_partial(self):
        text = replace_once(VALID_SRS, "- **Related:** UC-001, DR-001", "- **Related:** UC-001, DR-001, FR-099")
        self.assertIn("ID002", codes(srs=text, partial=True, level="WARNING"))
        self.assertNotIn("ID002", codes(srs=text, partial=True, level="ERROR"))

    def test_dangling_reference_downgraded_when_file_missing(self):
        text = replace_once(VALID_SRS, "- **Related:** UC-001, DR-001", "- **Related:** UC-001, DR-001, FR-099")
        findings, _ = vd.validate_project({"SRS": text})  # thiếu BRD và DIAGRAMS
        self.assertIn("ID002", [f.code for f in findings if f.level == "WARNING"])
        self.assertNotIn("ID002", [f.code for f in findings if f.level == "ERROR"])

    def test_cross_file_reference_resolves(self):
        # SRS §8 BRD tham chiếu UC-001 (định nghĩa ở SRS) — không phải dangling.
        self.assertNotIn("ID002", codes())

    def test_dangling_reference_in_mermaid(self):
        text = replace_once(VALID_DIA, 'RoleB["Vai trò B"] -->|"FR-002"| SYS', 'RoleB["Vai trò B"] -->|"FR-077"| SYS')
        self.assertIn("ID002", codes(diagrams=text, level="ERROR"))

    def test_ids_in_plain_code_block_ignored(self):
        text = VALID_SRS + "\n```text\nVí dụ FR-555 không được tính.\n```\n"
        self.assertNotIn("ID002", codes(srs=text))

    def test_malformed_id(self):
        text = replace_once(VALID_SRS, "- **Related:** UC-001, BR-001", "- **Related:** UC-001, BR-001, FR-1")
        self.assertIn("ID003", codes(srs=text))

    def test_ac_outside_parent(self):
        text = replace_once(
            VALID_SRS,
            "  - AC-FR-002-01: Given",
            "  - AC-FR-001-03: Given đặt nhầm chỗ, when x, then y.\n  - AC-FR-002-01: Given",
        )
        self.assertIn("ID004", codes(srs=text))

    def test_traceability_row_is_reference_not_definition(self):
        # Cột đầu "Goal / Source" của Traceability Matrix KHÔNG được coi là định nghĩa GOAL mới.
        self.assertNotIn("ID001", codes())


class TestRequirements(unittest.TestCase):
    def test_missing_field(self):
        text = replace_once(VALID_SRS, "- **Statement:** Người tạo đối tượng X không được duyệt chính đối tượng đó.\n", "")
        self.assertIn("REQ001", codes(srs=text))

    def test_invalid_status(self):
        text = replace_once(VALID_SRS, "- **Priority:** Should\n- **Status:** Confirmed\n- **Classification:**",
                             "- **Priority:** Should\n- **Status:** Done\n- **Classification:**")
        self.assertIn("REQ002", codes(srs=text))

    def test_invalid_priority(self):
        text = replace_once(VALID_SRS, "- **Priority:** Should\n- **Status:** Confirmed\n- **Classification:**",
                             "- **Priority:** High\n- **Status:** Confirmed\n- **Classification:**")
        self.assertIn("REQ003", codes(srs=text))

    def test_fr_without_ac(self):
        text = replace_once(VALID_SRS, "  - AC-FR-002-01: Given đối tượng X ở trạng thái Chờ duyệt, when vai trò B duyệt, then đối tượng X chuyển sang Đã duyệt.\n", "")
        text = text.replace(", AC-FR-002-01", "").replace("| AC-FR-002-01 |", "| |")
        self.assertIn("REQ004", codes(srs=text))

    def test_br_without_ac_or_verification(self):
        text = replace_once(VALID_SRS, "- **Status:** Confirmed\n- **Verification:** Test\n\n### Dữ liệu", "- **Status:** Confirmed\n\n### Dữ liệu")
        self.assertIn("REQ005", codes(srs=text))

    def test_nfr_missing_target(self):
        text = replace_once(VALID_SRS, "- **Target:** 3 giây với 95% lượt mở trong giờ làm việc\n", "")
        self.assertIn("REQ006", codes(srs=text))

    def test_superseded_without_replacement(self):
        text = replace_once(VALID_SRS, "- **Priority:** Should\n- **Status:** Confirmed\n- **Classification:**",
                             "- **Priority:** Should\n- **Status:** Superseded\n- **Classification:**")
        self.assertIn("REQ007", codes(srs=text))

    def test_rejected_requirement_skips_ac_check(self):
        text = replace_once(VALID_SRS, "  - AC-FR-002-01: Given đối tượng X ở trạng thái Chờ duyệt, when vai trò B duyệt, then đối tượng X chuyển sang Đã duyệt.\n", "")
        text = text.replace(", AC-FR-002-01", "").replace("| AC-FR-002-01 |", "| |")
        text = replace_once(text, "- **Status:** Confirmed\n- **Related:** UC-001, BR-001", "- **Status:** Rejected\n- **Related:** UC-001, BR-001")
        self.assertNotIn("REQ004", codes(srs=text))

    def test_story_missing_parts(self):
        text = replace_once(VALID_SRS, "- **Related:** FR-001\n- **Priority:** Must\n- **Status:** Confirmed\n- **Acceptance criteria:** see AC-FR-001-01, AC-FR-001-02",
                             "- **Priority:** Must\n- **Status:** Confirmed")
        self.assertIn("REQ008", codes(srs=text))


class TestPlaceholders(unittest.TestCase):
    def test_tbd(self):
        text = replace_once(VALID_SRS, "- **Target:** 3 giây với 95% lượt mở trong giờ làm việc", "- **Target:** TBD (Q-001)")
        result = codes(srs=text)
        self.assertIn("PH001", result)
        self.assertNotIn("ERROR", [f.level for f in vd.validate_project({"BRD": VALID_BRD, "SRS": text, "DIAGRAMS": VALID_DIA})[0]])

    def test_bracket_placeholder(self):
        text = replace_once(VALID_BRD, "Vai trò A hiện xử lý", "[Tên vai trò] hiện xử lý")
        self.assertIn("PH002", codes(brd=text))

    def test_markdown_link_is_not_placeholder(self):
        text = replace_once(VALID_BRD, "Vai trò A hiện xử lý", "[Tài liệu](https://example.com) Vai trò A hiện xử lý")
        self.assertNotIn("PH002", codes(brd=text))

    def test_coverage_tbd_not_counted_as_placeholder(self):
        text = replace_once(VALID_SRS, "| Glossary | Answered | |", "| Glossary | TBD | |")
        self.assertIn("PH001", codes(srs=text))  # TBD trong coverage vẫn là placeholder thật, không bị bỏ qua nữa


class TestTraceabilityCoverageQuestions(unittest.TestCase):
    def test_requirement_not_traced(self):
        text = replace_once(VALID_SRS, "| GOAL-001 | BR-001 | | | DIA-002 | Test | | |\n", "")
        self.assertIn("TR001", codes(srs=text))

    def test_goal_not_traced(self):
        head, tail = VALID_BRD.split("## 3. Goals and Success Metrics", 1)
        text_brd = head + "## 3. Goals and Success Metrics" + tail
        head2, tail2 = VALID_SRS.split("### Traceability Matrix", 1)
        text_srs = head2 + "### Traceability Matrix" + tail2.replace("| GOAL-001 |", "| SRC-001 |")
        self.assertIn("TR002", codes(brd=text_brd, srs=text_srs))

    def test_coverage_invalid_status(self):
        text = replace_once(VALID_SRS, "| Glossary | Answered | |", "| Glossary | Maybe | |")
        self.assertIn("COV001", codes(srs=text))

    def test_coverage_table_missing_entirely(self):
        text = re.sub(r"### Elicitation Coverage.*?(?=### Traceability Matrix)", "", VALID_SRS, flags=re.S)
        self.assertIn("COV002", codes(srs=text))

    def test_question_invalid_priority(self):
        text = replace_once(VALID_SRS, "| P1 | Chủ nghiệp vụ | Answered |", "| High | Chủ nghiệp vụ | Answered |")
        self.assertIn("Q001", codes(srs=text))


class TestDiagrams(unittest.TestCase):
    def test_dia_without_mermaid(self):
        text = re.sub(r"```mermaid\nstateDiagram-v2.*?```\n", "", VALID_DIA, flags=re.S)
        self.assertIn("DIA001", codes(diagrams=text))

    def test_disallowed_mermaid_type(self):
        text = replace_once(VALID_DIA, "stateDiagram-v2", "pie")
        self.assertIn("DIA002", codes(diagrams=text))

    def test_mermaid_outside_dia(self):
        text = replace_once(
            VALID_DIA, "### DIA-001",
            "```mermaid\nflowchart LR\n  A --> B\n```\n\n### DIA-001",
        )
        self.assertIn("DIA003", codes(diagrams=text))

    def test_dia_missing_source(self):
        text = replace_once(VALID_DIA, "- **Source:** FR-002, BR-001\n- **Status:** Confirmed\n\n```mermaid", "- **Status:** Confirmed\n\n```mermaid")
        self.assertIn("DIA004", codes(diagrams=text))

    def test_no_context_diagram(self):
        text = replace_once(VALID_DIA, "- **Type:** Context", "- **Type:** Process")
        self.assertIn("DIA005", codes(diagrams=text))


class TestMultiFileConsistency(unittest.TestCase):
    def test_missing_file_warns(self):
        findings, _ = vd.validate_project({"SRS": VALID_SRS})
        self.assertIn("IO002", [f.code for f in findings])

    def test_version_mismatch_warns(self):
        text = replace_once(VALID_BRD, "| Document version | 0.3 |", "| Document version | 0.4 |")
        self.assertIn("DOC004", codes(brd=text))

    def test_status_mismatch_warns(self):
        text = replace_once(VALID_BRD, "| Status | DRAFT — NOT APPROVED |", "| Status | ON HOLD |")
        self.assertIn("DOC005", codes(brd=text))


class TestApprovalUi(unittest.TestCase):
    def _approved(self, brd=None, srs=None, diagrams=None):
        return (
            replace_once(VALID_BRD if brd is None else brd, "| Status | DRAFT — NOT APPROVED |", "| Status | APPROVED |"),
            replace_once(VALID_SRS if srs is None else srs, "| Status | DRAFT — NOT APPROVED |", "| Status | APPROVED |"),
            replace_once(VALID_DIA if diagrams is None else diagrams, "| Status | DRAFT — NOT APPROVED |", "| Status | APPROVED |"),
        )

    def test_approved_without_record(self):
        brd, srs, dia = self._approved()
        self.assertIn("APR001", codes(brd=brd, srs=srs, diagrams=dia))

    def test_approved_with_matching_record(self):
        brd, srs, dia = self._approved()
        srs = replace_once(
            srs,
            "| Version | Decision | Approver (role, as stated) | Date | Notes |\n|---|---|---|---|---|\n",
            "| Version | Decision | Approver (role, as stated) | Date | Notes |\n|---|---|---|---|---|\n"
            "| 0.3 | APPROVE | Chủ nghiệp vụ | 2026-10-06 | |\n",
        )
        self.assertNotIn("APR001", codes(brd=brd, srs=srs, diagrams=dia))

    def test_approved_with_proposed_items(self):
        brd, srs, dia = self._approved()
        srs = replace_once(srs, "- **Priority:** Must\n- **Status:** Confirmed\n- **Related:** UC-001, DR-001",
                            "- **Priority:** Must\n- **Status:** Proposed\n- **Related:** UC-001, DR-001")
        self.assertIn("APR002", codes(brd=brd, srs=srs, diagrams=dia))

    def test_approved_with_open_p0(self):
        brd, srs, dia = self._approved()
        srs = replace_once(srs, "| P1 | Chủ nghiệp vụ | Answered |", "| P0 | Chủ nghiệp vụ | Open |")
        self.assertIn("APR003", codes(brd=brd, srs=srs, diagrams=dia))

    def test_approved_with_open_p2_also_blocks(self):
        # Siết: KHÔNG chỉ P0 mới chặn phê duyệt — P1/P2 còn Open cũng phải chặn.
        brd, srs, dia = self._approved()
        srs = replace_once(srs, "| P1 | Chủ nghiệp vụ | Answered |", "| P2 | Chủ nghiệp vụ | Open |")
        self.assertIn("APR003", codes(brd=brd, srs=srs, diagrams=dia))

    def test_approved_with_deferred_question_does_not_block(self):
        brd, srs, dia = self._approved()
        srs = replace_once(srs, "| P1 | Chủ nghiệp vụ | Answered |", "| P2 | Chủ nghiệp vụ | Deferred |")
        self.assertNotIn("APR003", codes(brd=brd, srs=srs, diagrams=dia))

    def test_invalid_document_status(self):
        text = replace_once(VALID_SRS, "| Status | DRAFT — NOT APPROVED |", "| Status | Final |")
        self.assertIn("APR004", codes(srs=text))

    def test_status_dash_variants_accepted(self):
        text = replace_once(VALID_SRS, "| Status | DRAFT — NOT APPROVED |", "| Status | DRAFT - NOT APPROVED |")
        self.assertNotIn("APR004", codes(srs=text))

    def test_invalid_version(self):
        text = replace_once(VALID_SRS, "| Document version | 0.3 |", "| Document version | bản nháp |")
        self.assertIn("APR005", codes(srs=text))

    def test_invalid_hex(self):
        text = replace_once(VALID_SRS, "#1A73E8", "#1A73E")
        self.assertIn("UI001", codes(srs=text))

    def test_uxp_without_source(self):
        text = replace_once(VALID_SRS, "| UXP-001 | Preference | Giao diện thoáng, ít màu | SRC-001 |", "| UXP-001 | Preference | Giao diện thoáng, ít màu | |")
        self.assertIn("UI002", codes(srs=text))

    def test_uxp_invalid_type(self):
        text = replace_once(VALID_SRS, "| UXP-001 | Preference |", "| UXP-001 | Wish |")
        self.assertIn("UI003", codes(srs=text))


class TestCli(unittest.TestCase):
    def test_help(self):
        r = run_cli("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Exit code", r.stdout)

    def test_valid_exit_zero_and_disclaimer(self):
        r = run_cli(
            "--brd", str(FIXTURES / "valid-minimal-brd.md"),
            "--srs", str(FIXTURES / "valid-minimal-srs.md"),
            "--diagrams", str(FIXTURES / "valid-minimal-diagrams.md"),
        )
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("không thay thế review", r.stdout)

    def test_error_exit_one(self):
        r = run_cli("--srs", str(FIXTURES / "empty.md"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("DOC001", r.stdout)

    def test_missing_file_exit_two(self):
        r = run_cli("--srs", str(FIXTURES / "khong-ton-tai.md"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("IO001", r.stdout)

    def test_directory_exit_two(self):
        r = run_cli("--srs", str(FIXTURES))
        self.assertEqual(r.returncode, 2)

    def test_no_args_exit_two(self):
        self.assertEqual(run_cli().returncode, 2)

    def test_ascii_output(self):
        r = run_cli(
            "--ascii",
            "--brd", str(FIXTURES / "valid-minimal-brd.md"),
            "--srs", str(FIXTURES / "valid-minimal-srs.md"),
            "--diagrams", str(FIXTURES / "valid-minimal-diagrams.md"),
        )
        self.assertEqual(r.returncode, 0)
        self.assertTrue(all(ord(ch) < 128 for ch in r.stdout), r.stdout)

    def test_does_not_modify_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            path.write_text(VALID_SRS + "\nTBD\n", encoding="utf-8")
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            run_cli("--srs", str(path))
            after = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(before, after)

    def test_utf8_bom_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            path.write_bytes(b"\xef\xbb\xbf" + VALID_SRS.encode("utf-8"))
            r = run_cli("--srs", str(path))
            self.assertNotIn("IO001", r.stdout)

    def test_non_utf8_exit_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            path.write_bytes("Tiêu đề".encode("utf-16"))
            self.assertEqual(run_cli("--srs", str(path)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
