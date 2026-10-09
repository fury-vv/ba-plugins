"""Unit test cho skills/srs-analysis/scripts/validate_srs.py.

Chạy từ thư mục gốc của plugin:
    python3 -m unittest discover -s tests -v

Chỉ dùng thư viện chuẩn. Mỗi quy tắc có ít nhất một ca dương (phát hiện lỗi)
và dựa trên fixture hợp lệ làm ca âm (không báo lỗi).
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
SCRIPT = ROOT / "skills" / "srs-analysis" / "scripts" / "validate_srs.py"
TEMPLATE = ROOT / "skills" / "srs-analysis" / "references" / "srs-template.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID = (FIXTURES / "valid-minimal-srs.md").read_text(encoding="utf-8")
SAMPLE = ROOT / "examples" / "sample-srs-excerpt.md"

_spec = importlib.util.spec_from_file_location("validate_srs", SCRIPT)
vs = importlib.util.module_from_spec(_spec)
sys.modules["validate_srs"] = vs  # dataclass cần module có trong sys.modules
assert _spec.loader is not None
_spec.loader.exec_module(vs)


def codes(text: str, partial: bool = False, level: str | None = None) -> list:
    return [f.code for f in vs.validate_text(text, partial=partial) if level is None or f.level == level]


def replace_once(text: str, old: str, new: str) -> str:
    assert old in text, f"Không tìm thấy đoạn cần thay: {old!r}"
    return text.replace(old, new, 1)


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


class TestValidFixture(unittest.TestCase):
    def test_valid_has_no_error_or_warning(self):
        found = [f for f in vs.validate_text(VALID) if f.level in ("ERROR", "WARNING")]
        self.assertEqual(found, [], "\n".join(f.render() for f in found))

    def test_template_skeleton_has_no_error(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        m = re.search(r"~~~~markdown\n(.*?)\n~~~~", text, re.S)
        self.assertIsNotNone(m, "Không tìm thấy khung SRS trong srs-template.md")
        self.assertEqual(codes(m.group(1), level="ERROR"), [])

    def test_sample_excerpt_partial_has_no_error(self):
        self.assertTrue(SAMPLE.exists(), "Thiếu examples/sample-srs-excerpt.md")
        text = SAMPLE.read_text(encoding="utf-8")
        self.assertEqual(codes(text, partial=True, level="ERROR"), [])


class TestSections(unittest.TestCase):
    def test_empty_file(self):
        self.assertEqual(codes("   \n"), ["DOC001"])

    def test_missing_section(self):
        text = re.sub(r"## 18\. Reports.*?(?=## 19\.)", "", VALID, flags=re.S)
        self.assertIn("SEC001", codes(text, level="ERROR"))

    def test_missing_section_ignored_in_partial(self):
        text = re.sub(r"## 18\. Reports.*?(?=## 19\.)", "", VALID, flags=re.S)
        self.assertNotIn("SEC001", codes(text, partial=True))

    def test_title_mismatch(self):
        text = replace_once(VALID, "## 4. Scope — Phạm vi", "## 4. Phạm vi")
        self.assertIn("SEC002", codes(text, level="ERROR"))

    def test_vietnamese_part_can_change(self):
        text = replace_once(VALID, "## 4. Scope — Phạm vi", "## 4. Scope — Phạm vi dự án")
        self.assertNotIn("SEC002", codes(text))

    def test_duplicate_section(self):
        text = VALID + "\n## 4. Scope — Phạm vi\n\nThêm.\n"
        self.assertIn("SEC003", codes(text))

    def test_empty_section(self):
        text = replace_once(VALID, "Không có dữ liệu cũ cần chuyển. Triển khai một lần cho toàn bộ người dùng.", "")
        self.assertIn("SEC004", codes(text))

    def test_na_without_reason(self):
        text = replace_once(VALID, "Not applicable — phạm vi đã loại trừ tích hợp với hệ thống bên ngoài (§4).", "Not applicable")
        self.assertIn("SEC005", codes(text))

    def test_na_not_allowed(self):
        text = re.sub(r"(## 21\. Models and Diagrams — Mô hình và sơ đồ\n).*?(?=## 22\.)",
                      r"\1\nNot applicable — không cần sơ đồ.\n\n", VALID, flags=re.S)
        self.assertIn("SEC006", codes(text))

    def test_unknown_h2(self):
        text = VALID + "\n## Ghi chú thêm\n\nNội dung.\n"
        self.assertIn("SEC007", codes(text))

    def test_unclosed_fence(self):
        text = VALID + "\n```text\nchưa đóng\n"
        self.assertIn("DOC002", codes(text))


class TestIds(unittest.TestCase):
    def test_duplicate_definition(self):
        text = replace_once(VALID, "## 10. Business Rules", "### FR-001 — Trùng\n- **Statement:** x\n\n## 10. Business Rules")
        self.assertIn("ID001", codes(text, level="ERROR"))

    def test_duplicate_table_definition(self):
        text = replace_once(VALID, "| SRC-002 | Document |", "| SRC-001 | Document |")
        self.assertIn("ID001", codes(text, level="ERROR"))

    def test_dangling_reference(self):
        text = replace_once(VALID, "- **Related:** UC-001, DR-001", "- **Related:** UC-001, DR-001, FR-099")
        self.assertIn("ID002", codes(text, level="ERROR"))

    def test_dangling_reference_is_warning_in_partial(self):
        text = replace_once(VALID, "- **Related:** UC-001, DR-001", "- **Related:** UC-001, DR-001, FR-099")
        self.assertIn("ID002", codes(text, partial=True, level="WARNING"))
        self.assertNotIn("ID002", codes(text, partial=True, level="ERROR"))

    def test_dangling_reference_in_mermaid(self):
        text = replace_once(VALID, 'RoleB["Vai trò B"] -->|"FR-002"| SYS', 'RoleB["Vai trò B"] -->|"FR-077"| SYS')
        self.assertIn("ID002", codes(text, level="ERROR"))

    def test_ids_in_plain_code_block_ignored(self):
        text = VALID + "\n```text\nVí dụ FR-555 không được tính.\n```\n"
        self.assertNotIn("ID002", codes(text))

    def test_malformed_id(self):
        text = replace_once(VALID, "- **Related:** UC-001, BR-001", "- **Related:** UC-001, BR-001, FR-1")
        self.assertIn("ID003", codes(text))

    def test_ac_outside_parent(self):
        text = replace_once(
            VALID,
            "  - AC-FR-002-01: Given",
            "  - AC-FR-001-03: Given đặt nhầm chỗ, when x, then y.\n  - AC-FR-002-01: Given",
        )
        self.assertIn("ID004", codes(text))

    def test_table_row_outside_owner_is_reference(self):
        text = replace_once(VALID, "| GOAL-001 | FR-002 |", "| GOAL-009 | FR-002 |")
        self.assertIn("ID002", codes(text, level="ERROR"))


class TestRequirements(unittest.TestCase):
    def test_missing_field(self):
        text = replace_once(VALID, "- **Statement:** Người tạo đối tượng X không được duyệt chính đối tượng đó.\n", "")
        self.assertIn("REQ001", codes(text))

    def test_invalid_status(self):
        text = replace_once(VALID, "- **Priority:** Should\n- **Status:** Confirmed\n- **Classification:**",
                            "- **Priority:** Should\n- **Status:** Done\n- **Classification:**")
        self.assertIn("REQ002", codes(text))

    def test_invalid_priority(self):
        text = replace_once(VALID, "- **Priority:** Should\n- **Status:** Confirmed\n- **Classification:**",
                            "- **Priority:** High\n- **Status:** Confirmed\n- **Classification:**")
        self.assertIn("REQ003", codes(text))

    def test_fr_without_ac(self):
        text = replace_once(VALID, "  - AC-FR-002-01: Given đối tượng X ở trạng thái Chờ duyệt, when vai trò B duyệt, then đối tượng X chuyển sang Đã duyệt.\n", "")
        text = text.replace(", AC-FR-002-01", "").replace("| AC-FR-002-01 |", "| |")
        self.assertIn("REQ004", codes(text))

    def test_br_without_ac_or_verification(self):
        text = replace_once(VALID, "- **Status:** Confirmed\n- **Verification:** Test\n\n## 11.", "- **Status:** Confirmed\n\n## 11.")
        self.assertIn("REQ005", codes(text))

    def test_nfr_missing_target(self):
        text = replace_once(VALID, "- **Target:** 3 giây với 95% lượt mở trong giờ làm việc\n", "")
        self.assertIn("REQ006", codes(text))

    def test_superseded_without_replacement(self):
        text = replace_once(VALID, "- **Priority:** Should\n- **Status:** Confirmed\n- **Classification:**",
                            "- **Priority:** Should\n- **Status:** Superseded\n- **Classification:**")
        self.assertIn("REQ007", codes(text))

    def test_rejected_requirement_skips_ac_check(self):
        text = replace_once(VALID, "  - AC-FR-002-01: Given đối tượng X ở trạng thái Chờ duyệt, when vai trò B duyệt, then đối tượng X chuyển sang Đã duyệt.\n", "")
        text = text.replace(", AC-FR-002-01", "").replace("| AC-FR-002-01 |", "| |")
        text = replace_once(text, "- **Status:** Confirmed\n- **Related:** UC-001, BR-001", "- **Status:** Rejected\n- **Related:** UC-001, BR-001")
        self.assertNotIn("REQ004", codes(text))

    def test_story_missing_parts(self):
        text = replace_once(VALID, "- **Related:** FR-001\n- **Priority:** Must\n- **Status:** Confirmed\n- **Acceptance criteria:** see AC-FR-001-01, AC-FR-001-02",
                            "- **Priority:** Must\n- **Status:** Confirmed")
        self.assertIn("REQ008", codes(text))


class TestPlaceholders(unittest.TestCase):
    def test_tbd(self):
        text = replace_once(VALID, "- **Target:** 3 giây với 95% lượt mở trong giờ làm việc", "- **Target:** TBD (Q-001)")
        result = codes(text)
        self.assertIn("PH001", result)
        self.assertNotIn("ERROR", [f.level for f in vs.validate_text(text)])

    def test_bracket_placeholder(self):
        text = replace_once(VALID, "Vai trò A hiện xử lý", "[Tên vai trò] hiện xử lý")
        self.assertIn("PH002", codes(text))

    def test_markdown_link_is_not_placeholder(self):
        text = replace_once(VALID, "Vai trò A hiện xử lý", "[Tài liệu](https://example.com) Vai trò A hiện xử lý")
        self.assertNotIn("PH002", codes(text))

    def test_coverage_tbd_not_counted_as_placeholder(self):
        text = replace_once(VALID, "| 6. Glossary | Answered | |", "| 6. Glossary | TBD | |")
        self.assertNotIn("PH001", codes(text))


class TestTraceabilityCoverageQuestions(unittest.TestCase):
    def test_requirement_not_traced(self):
        text = replace_once(VALID, "| GOAL-001 | BR-001 | | | DIA-002 | Test | | |\n", "")
        self.assertIn("TR001", codes(text))

    def test_goal_not_traced(self):
        head, tail = VALID.split("## 28. Traceability Matrix", 1)
        text = head + "## 28. Traceability Matrix" + tail.replace("| GOAL-001 |", "| SRC-001 |")
        self.assertIn("TR002", codes(text))

    def test_coverage_invalid_status(self):
        text = replace_once(VALID, "| 6. Glossary | Answered | |", "| 6. Glossary | Maybe | |")
        self.assertIn("COV001", codes(text))

    def test_coverage_missing_row(self):
        text = replace_once(VALID, "| 6. Glossary | Answered | |\n", "")
        self.assertIn("COV002", codes(text))

    def test_question_invalid_priority(self):
        text = replace_once(VALID, "| P1 | Chủ nghiệp vụ | Answered |", "| High | Chủ nghiệp vụ | Answered |")
        self.assertIn("Q001", codes(text))


class TestDiagrams(unittest.TestCase):
    def test_dia_without_mermaid(self):
        text = re.sub(r"```mermaid\nstateDiagram-v2.*?```\n", "", VALID, flags=re.S)
        self.assertIn("DIA001", codes(text))

    def test_disallowed_mermaid_type(self):
        text = replace_once(VALID, "stateDiagram-v2", "pie")
        self.assertIn("DIA002", codes(text))

    def test_mermaid_outside_dia(self):
        text = VALID + "\n```mermaid\nflowchart LR\n  A --> B\n```\n"
        self.assertIn("DIA003", codes(text))

    def test_dia_missing_source(self):
        text = replace_once(VALID, "- **Source:** FR-002, BR-001\n- **Status:** Confirmed\n\n```mermaid", "- **Status:** Confirmed\n\n```mermaid")
        self.assertIn("DIA004", codes(text))

    def test_no_context_diagram(self):
        text = replace_once(VALID, "- **Type:** Context", "- **Type:** Process")
        self.assertIn("DIA005", codes(text))


class TestDomainApprovalUi(unittest.TestCase):
    DOMAIN_CONTENT = "Yêu cầu đặc thù: cần chuyên gia xác minh (Q-001)."

    def test_domain_section_without_confirmation(self):
        text = replace_once(VALID, "Not applicable — domain chưa được xác nhận.", self.DOMAIN_CONTENT)
        self.assertIn("DOM001", codes(text))

    def test_domain_section_with_confirmation(self):
        text = replace_once(VALID, "Not applicable — domain chưa được xác nhận.", self.DOMAIN_CONTENT)
        text = replace_once(text, "| Domain | Not confirmed |", "| Domain | Confirmed: lĩnh vực thử nghiệm |")
        self.assertNotIn("DOM001", codes(text))

    def _approved(self, text: str) -> str:
        return replace_once(text, "| Status | DRAFT — NOT APPROVED |", "| Status | APPROVED |")

    def test_approved_without_record(self):
        self.assertIn("APR001", codes(self._approved(VALID)))

    def test_approved_with_matching_record(self):
        text = self._approved(VALID)
        text = replace_once(text, "| Version | Decision | Approver (role, as stated) | Date | Notes |\n|---|---|---|---|---|",
                            "| Version | Decision | Approver (role, as stated) | Date | Notes |\n|---|---|---|---|---|\n| 0.3 | APPROVE | Chủ nghiệp vụ | 2026-10-06 | |")
        self.assertNotIn("APR001", codes(text))

    def test_approved_with_proposed_items(self):
        text = self._approved(VALID)
        text = replace_once(text, "- **Priority:** Must\n- **Status:** Confirmed\n- **Related:** UC-001, DR-001",
                            "- **Priority:** Must\n- **Status:** Proposed\n- **Related:** UC-001, DR-001")
        self.assertIn("APR002", codes(text))

    def test_approved_with_open_p0(self):
        text = self._approved(VALID)
        text = replace_once(text, "| P1 | Chủ nghiệp vụ | Answered |", "| P0 | Chủ nghiệp vụ | Open |")
        self.assertIn("APR003", codes(text))

    def test_invalid_document_status(self):
        text = replace_once(VALID, "| Status | DRAFT — NOT APPROVED |", "| Status | Final |")
        self.assertIn("APR004", codes(text))

    def test_status_dash_variants_accepted(self):
        text = replace_once(VALID, "| Status | DRAFT — NOT APPROVED |", "| Status | DRAFT - NOT APPROVED |")
        self.assertNotIn("APR004", codes(text))

    def test_invalid_version(self):
        text = replace_once(VALID, "| Document version | 0.3 |", "| Document version | bản nháp |")
        self.assertIn("APR005", codes(text))

    def test_invalid_hex(self):
        text = replace_once(VALID, "#1A73E8", "#1A73E")
        self.assertIn("UI001", codes(text))

    def test_uxp_without_source(self):
        text = replace_once(VALID, "| UXP-001 | Preference | Giao diện thoáng, ít màu | SRC-001 |", "| UXP-001 | Preference | Giao diện thoáng, ít màu | |")
        self.assertIn("UI002", codes(text))

    def test_uxp_invalid_type(self):
        text = replace_once(VALID, "| UXP-001 | Preference |", "| UXP-001 | Wish |")
        self.assertIn("UI003", codes(text))


class TestCli(unittest.TestCase):
    def test_help(self):
        r = run_cli("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Exit code", r.stdout)

    def test_valid_exit_zero_and_disclaimer(self):
        r = run_cli(str(FIXTURES / "valid-minimal-srs.md"))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("không thay thế review", r.stdout)

    def test_error_exit_one(self):
        r = run_cli(str(FIXTURES / "empty.md"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("DOC001", r.stdout)

    def test_missing_file_exit_two(self):
        r = run_cli(str(FIXTURES / "khong-ton-tai.md"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("IO001", r.stdout)

    def test_directory_exit_two(self):
        r = run_cli(str(FIXTURES))
        self.assertEqual(r.returncode, 2)

    def test_no_args_exit_two(self):
        self.assertEqual(run_cli().returncode, 2)

    def test_ascii_output(self):
        r = run_cli("--ascii", str(FIXTURES / "valid-minimal-srs.md"))
        self.assertEqual(r.returncode, 0)
        self.assertTrue(all(ord(ch) < 128 for ch in r.stdout), r.stdout)

    def test_does_not_modify_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            path.write_text(VALID + "\nTBD\n", encoding="utf-8")
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            run_cli(str(path))
            after = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(before, after)

    def test_utf8_bom_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            path.write_bytes(b"\xef\xbb\xbf" + VALID.encode("utf-8"))
            self.assertEqual(run_cli(str(path)).returncode, 0)

    def test_non_utf8_exit_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "srs.md"
            path.write_bytes("Tiêu đề".encode("utf-16"))
            self.assertEqual(run_cli(str(path)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
