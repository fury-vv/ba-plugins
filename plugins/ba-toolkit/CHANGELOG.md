# Changelog

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
