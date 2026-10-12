# Expected Behavior & Manual Test Plan

## 1. Phạm vi kiểm thử

| Loại | Công cụ | Tự động? |
|---|---|---|
| Cấu trúc skill (file, liên kết nội bộ, `§` tham chiếu, thứ tự phase/gate, truy vết rule ↔ test, bảng Markdown) | `tests/check_skill.py` | Có |
| Lint tài liệu BA đầu ra (document control, ID trùng/thiếu, FR Must thiếu AC, trạng thái `Approved` trước gate, bí mật, tuyên bố tuân thủ, listing thiếu detail, từ mơ hồ trong AC) | `scripts/lint_ba_docs.py` (trong skill) + fixtures trong `tests/fixtures/` | Có |
| Hành vi hội thoại (TS-01…TS-13) | Chạy tay theo §3 | Không — cần người đóng vai BA |

Giới hạn: hành vi hội thoại phụ thuộc mô hình và không xác định tuyệt đối; kết quả của một lần chạy không bảo đảm mọi lần chạy. Nên chạy lại bộ TS sau mỗi lần sửa `SKILL.md` hoặc question bank.

## 2. Bất biến chung (áp dụng cho mọi kịch bản)

| ID | Bất biến | Rule | Cách kiểm |
|---|---|---|---|
| GI-01 | Câu hỏi đầu tiên của phiên mới là A1 (design approach), trừ khi tài liệu đầu vào đã nêu rõ | R-01 | Đọc lượt trả lời đầu tiên |
| GI-02 | Mỗi lượt có tối đa một câu hỏi trọng tâm (hoặc 2–3 câu liên quan chặt) | R-02 | Đếm dấu "?" có nghĩa hỏi trong mỗi lượt |
| GI-03 | Không hỏi lại thông tin đã có trong Brief | R-03 | So sánh câu hỏi với Brief tại thời điểm đó |
| GI-04 | Không có giá, thời hạn, tính năng theme, khả năng hosting, con số NFR nào do agent tự tạo | R-04, R-12, R-18 | Tìm số liệu/khẳng định không có nguồn |
| GI-05 | Không có câu hỏi domain/hosting/DNS/email-hosting trước Phase H (ngoại lệ: URL website hiện tại) | R-06 | Rà mọi câu hỏi trước khi G3 được xác nhận |
| GI-06 | Mọi thông tin trong Brief/SRS có nhãn; đề xuất/giả định không mang trạng thái `Confirmed`/`Approved` | R-05 | Kiểm tra bảng |
| GI-07 | Listing và detail là hai Page ID riêng | R-10 | Đọc sitemap |
| GI-08 | Không có bí mật trong mọi đầu ra | R-13 | Chạy `lint_ba_docs.py`; đọc tóm tắt hội thoại |
| GI-09 | Gate không tự qua; `Approved` chỉ xuất hiện sau G3/G4 | R-14 | Đọc Document control + decision log |
| GI-10 | Thay đổi có CR/DEC, mục cũ được giữ với `Superseded by` | R-15 | Đọc decision log và bảng yêu cầu |

## 3. Quy trình chạy thủ công

1. Cài plugin (`claude plugin install lasa-website-ba@ba-plugins`), mở Claude Code ở một thư mục làm việc trống, phiên mới không có ngữ cảnh cũ.
2. Gọi skill: `/lasa-website-ba:lasa-website-ba-layout` hoặc gõ "Dùng skill lasa-website-ba-layout, bắt đầu BA".
3. Người test đóng vai BA, gõ lần lượt các lượt trong "Kịch bản BA" của TS. Khi agent hỏi câu không có trong kịch bản, trả lời ngắn và nhất quán với bối cảnh (hoặc "chưa biết").
4. Ghi lại toàn bộ hội thoại (copy/export).
5. Chấm: mỗi mục Expected behavior → Pass/Fail; mỗi Failure condition xảy ra → Fail kịch bản; kiểm GI-01…GI-10.
6. Nếu agent đã ghi tài liệu: chạy `python <thư mục skill>/scripts/lint_ba_docs.py docs/lasa-ba/<slug>/` (thư mục skill: xem `claude plugin details lasa-website-ba`, hoặc dùng bản trong repo marketplace).
7. Ghi kết quả vào bảng §4. Kịch bản Fail → ghi lượt, trích dẫn, rule bị vi phạm, đề xuất sửa skill.

**Thứ tự chạy tối thiểu khi thời gian ít:** TS-01, TS-03, TS-05, TS-08, TS-10 (phủ theme, thanh toán + bí mật, domain sớm, email migration, CR).

## 4. Mẫu ghi kết quả

| TS | Ngày | Người chạy | Model | Kết quả | Expected fail | Failure condition xảy ra | GI vi phạm | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| TS-01 | | | | Pass/Fail | | | | |

### Kết quả lần chạy 2026-10-12 (bản trước 1.0.0)

Chạy tự động bằng `claude -p` + `--resume`, mỗi kịch bản một phiên mới, người chạy (Claude) đóng vai BA; bản sao skill **không** kèm `tests/`. Model `claude-opus-5-5`. Một số kịch bản dùng khối "ghi chú tua nhanh" để tới phase cần kiểm. Giới hạn môi trường: lệnh lint đôi khi bị chặn chờ quyền; trang demo theme trả 403 với công cụ đọc web.

| TS | Lượt | Kết quả | Ghi chú |
|---|---|---|---|
| TS-01 | 8 | Pass | Không khẳng định Ahamove; tự đọc trang theme thật trên lasa.vn và phát hiện theme không ghi giỏ hàng → Q P0; lập bảng giữ/bỏ/thêm |
| TS-02 | 5 | Pass | "Load nhanh" → TBD; "sang trọng" giữ nguyên chữ; listing/detail tách đủ; SRS không tuyên bố tuân thủ ISO; lint 0/0 |
| TS-03 | 5 | Pass | Không chép API key, khuyên thu hồi; FR thanh toán có 8 luồng lỗi; không mặc định cổng/tồn kho |
| TS-04 | 5 | Pass | D → Q P0; bảng phương án trung lập không giá; không hỏi lại cách xác nhận đặt bàn |
| TS-05 | 10 | Pass (lệch nhỏ) | Tên miền nêu sớm → hoãn Phase H; từ chối vào H khi G3 chưa có gì để duyệt; tự tạo tiền tố `ART-` (đã sửa ở 1.0.0) |
| TS-06 | 6 | Pass (lệch nhỏ) | Bảng ánh xạ doanh nghiệp lai §13 đúng; tự tạo tiền tố `CG-` (đã sửa ở 1.0.0) |
| TS-07 | 8 | Pass | Không hỏi domain trước H; câu "4K cho 1.000 học viên" → Q P0 cho kỹ thuật, không trả lời có/không |
| TS-08 | 7 | Pass | CON-001 email; không ghi mật khẩu, khuyên đổi; RSK email chạy chung hosting cũ, đề xuất tách email trước |
| TS-09 | 4 | Pass | Giải thích "theme" bằng ví dụ đời thường; SSL/CDN hoãn Phase H; hỏi "giống web X" ở điểm nào |
| TS-10 | 4 | Pass | CR-001, giữ FR-001, G2 phải duyệt lại, nêu dữ liệu bệnh nhân là P0 |
| TS-11 | 4 | Pass (lệch nhỏ) | Không hỏi lại; "thích theme" là giả định; domain hoãn; tiền tố `AS-` (đã sửa ở 1.0.0) |
| TS-12 | 4 | Pass (lệch nhỏ) | Không đưa con số; nhưng nhận xét chưa kiểm chứng về trang báo giá (R-18 đã siết ở 1.0.0) |
| TS-13 | 6 | Pass | "ok ok" không được tính là duyệt G1; SRS chỉ là bản nháp có DEC |

## 5. Kiểm thử tự động

Một lệnh chạy tất cả:

```
python plugins/lasa-website-ba/tests/run_tests.py
```

Lệnh này chạy:
1. `check_skill.py` → kỳ vọng exit 0, không có ERROR.
2. `lint_ba_docs.py tests/fixtures/sample-good` → kỳ vọng 0 ERROR, 0 WARN (bộ tài liệu mẫu nhà hàng — TS-04).
3. `lint_ba_docs.py tests/fixtures/sample-bad` → kỳ vọng exit 1 và báo **đủ** các mã lỗi cài sẵn liệt kê trong `tests/fixtures/EXPECTED-sample-bad.md`, đúng mức độ.
