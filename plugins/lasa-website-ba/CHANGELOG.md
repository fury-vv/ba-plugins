# Changelog

## 1.0.0 — 2026-10-12

Phát hành đầu tiên trên marketplace `ba-plugins`. Kế thừa skill `lasa-website-ba` (bản zip nội bộ) và mở rộng.

### Nội dung
- Skill `lasa-website-ba-layout`: quy trình phỏng vấn 9 phase A→I, bắt đầu bằng câu design approach (theme / custom / custom từ ý tưởng / chưa quyết); domain & hosting dời về Phase H; 4 gate G1–G4; 22 quy tắc có mã `R-01..R-22`.
- `references/`: question bank cho 11 nhóm website trên trang báo giá LASA (tách sàn/hệ thống và xuất khẩu đa ngôn ngữ), doanh nghiệp lai, ngành lạ, 3 nhóm bổ sung từ kho theme; bank domain/hosting/migration; hướng dẫn design & layout; checklist SRS; catalog LASA ghi rõ mức kiểm chứng (đọc ngày 2026-10-12, không lưu giá).
- `templates/`: discovery brief, sitemap & page inventory, page specification, SRS 16 mục, RTM, decision log.
- `scripts/lint_ba_docs.py`: lint bộ tài liệu đầu ra (document control, ID trùng/thiếu, FR Must thiếu AC, Approved trước gate, bí mật, tuyên bố tuân thủ ISO, listing thiếu detail, từ mơ hồ trong AC).
- `tests/` (ngoài skill, không đi kèm khi skill được nạp): 13 kịch bản hội thoại, bất biến chung, fixtures, `check_skill.py`, `run_tests.py`.

### Sửa sau lần chạy hội thoại 2026-10-12
- Chỉ dùng tiền tố ID trong bảng quy ước; không tự tạo tiền tố (`ART-`, `CG-`, `AS-` đã xuất hiện khi test).
- R-18 áp dụng cả cho nhận xét chung về trang báo giá/gói LASA.
- Lệnh lint dùng `${CLAUDE_SKILL_DIR}` để chạy được khi cài qua plugin.
