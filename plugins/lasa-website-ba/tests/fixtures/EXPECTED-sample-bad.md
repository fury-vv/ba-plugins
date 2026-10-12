# Lỗi cài sẵn trong `sample-bad/`

`scripts/run_tests.py` đọc bảng dưới và yêu cầu `lint_ba_docs.py` báo **mỗi** mã ít nhất một lần, với đúng mức độ.

| Mã | Mức | Lỗi cài sẵn | File |
|---|---|---|---|
| L-DOC | ERROR | Document control thiếu "Last gate passed" | 02-sitemap-page-inventory.md |
| L-ISO | ERROR | "tuân thủ ISO/IEC/IEEE 29148" | 04-srs.md |
| L-DUP | ERROR | FR-001 định nghĩa hai lần trong một bảng | 04-srs.md |
| L-AC | ERROR | FR Must (dòng FR-001 thứ hai) không có AC | 04-srs.md |
| L-GATE | ERROR | FR-001 Approved khi mới qua G1 | 04-srs.md |
| L-STATUS | ERROR | Trạng thái "Xong" không hợp lệ | 04-srs.md |
| L-SECRET | ERROR | API key và mật khẩu giả trong ghi chú | 04-srs.md |
| L-VAGUE | WARN | "nhanh", "thân thiện" trong AC-001 | 04-srs.md |
| L-LISTING | WARN | PG-002 Listing, không có Detail | 02-sitemap-page-inventory.md |
| L-REF | WARN | UG-001, SRC-001 được nhắc nhưng không định nghĩa | 04-srs.md |
