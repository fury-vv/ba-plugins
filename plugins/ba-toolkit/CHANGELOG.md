# Changelog

## 2.1.0 — 2026-10-10

Siết chặt gate elicitation: trước chỉ câu hỏi `P0` còn `Open` mới chặn qua G1/G5; từ giờ **mọi câu hỏi còn `Open`, ở bất kỳ mức P0, P1 hay P2, đều chặn**. Chỉ `Answered`, `Deferred`, hoặc `Risk accepted` (có `DEC-`) mới được coi là đã xử lý.

### Thay đổi
- `scripts/validate_docs.py`: `APR003` giờ kiểm tra toàn bộ câu hỏi `Open` (trước chỉ lọc `Priority = P0`).
- `SKILL.md`: cập nhật tiêu chí G1 và G5; Nguyên tắc 5 ("Gate là thật") nêu rõ áp dụng cho mọi mức P0/P1/P2.
- `references/elicitation-guide.md`: ghi rõ P0/P1/P2 chỉ quyết định thứ tự hỏi, không quyết định có bắt buộc trả lời hay không.
- `references/quality-checklist.md`: cập nhật mục `[AUTO APR003]`.
- Thêm test `test_approved_with_open_p2_also_blocks`, `test_approved_with_deferred_question_does_not_block`.

## 2.0.0 — 2026-10-10

**Breaking change:** skill `srs-analysis` không còn xuất một file SRS 30-section duy nhất. Thay vào đó xuất **3 file tách biệt**: `docs/brd/brd.md` (Business Requirement Document), `docs/srs/srs.md` (SRS theo chuẩn 6 phần: Introduction, High-Level Requirements, Functional Requirements, Non-Functional Requirements, Security Requirements, Other Requirements and Appendix), và `docs/diagrams/diagrams.md` (toàn bộ sơ đồ Mermaid). Ba file dùng chung một không gian ID.

### Thay đổi
- `references/srs-template.md`: viết lại hoàn toàn theo khung 6 phần chuẩn, chỉ còn nội dung của riêng SRS.
- Tách phần "Quy ước chung" (ngữ pháp ID, khối requirement, Priority/Status, Document Control, sổ đăng ký, phê duyệt) ra `references/conventions.md`, dùng chung cho cả 3 file.
- Thêm `references/brd-template.md` và `references/diagrams-template.md`.
- `scripts/validate_srs.py` → `scripts/validate_docs.py`: nhận `--brd`/`--srs`/`--diagrams`, đọc cả 3 file cùng lúc, kiểm tra ID trùng/tham chiếu treo xuyên file, nhất quán version/status giữa các file, gate phê duyệt tổng hợp.
- Cú pháp phê duyệt G5 đổi thành `APPROVE BRD+SRS vX.Y` / `DUYỆT BRD+SRS vX.Y` (duyệt đồng thời cả 3 file).
- Cập nhật mọi reference khác (`elicitation-guide.md`, `domain-discovery-guide.md`, `product-type-guide.md`, `nfr-checklist.md`, `user-story-standard.md`, `quality-checklist.md`, `change-control.md`, `diagram-standard.md`) để trỏ đúng file/section mới.
- Bỏ section "Domain-Specific Considerations" riêng (không còn khớp chuẩn 6 phần) — nội dung đặc thù lĩnh vực nay nằm trong BRD §2 Business Context, sau khi Domain được xác nhận.

### Không còn hỗ trợ
- Không migrate tự động SRS bản 30-section (v1.0.0) sang cấu trúc mới; cần tách thủ công hoặc bắt đầu lại.

## 1.0.0 — 2026-10-09

Phiên bản đầu tiên của plugin `ba-toolkit`.

### Thêm mới
- Skill `srs-analysis`: quy trình Phase 0–6 với gate G0, G1, G2 (xác nhận rõ ràng) và G5 (phê duyệt chính thức); chế độ nhập ghi chú họp; change control sau baseline.
- 10 reference: template và quy ước SRS (30 section song ngữ), hướng dẫn thu thập yêu cầu, câu hỏi theo loại sản phẩm và UI/UX, khám phá lĩnh vực và định dạng domain pack, chuẩn user story, chuẩn acceptance criteria, NFR checklist, chuẩn sơ đồ Mermaid, quality checklist, change control.
- `validate_srs.py`: kiểm tra cấu trúc (section, ID, tham chiếu, trường bắt buộc, AC, placeholder, traceability, coverage, sơ đồ, phê duyệt, domain, mã màu); chỉ dùng thư viện chuẩn; tùy chọn `--partial`, `--ascii`.
- Ví dụ giả lập, 26 ca kiểm thử, 68 unit test, công cụ quét thuật ngữ đặc thù lĩnh vực.

### Chưa có (theo kế hoạch)
- Kiểm tra độ tương phản màu, render Mermaid, sinh sơ đồ từ bảng (v1.1).
- Skill `meeting-prep`, `meeting-capture`, `domain-pack-curator`, `ba-status` (các giai đoạn sau).
