# SRS — Shop mẫu lỗi (dữ liệu hư cấu, cố ý sai để test lint)

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | Shop mẫu lỗi |
| Tài liệu | 04 — SRS / BA Package |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | F |
| Last gate passed | G1 |

Tài liệu này tuân thủ ISO/IEC/IEEE 29148.

## 8. Yêu cầu chức năng

| ID | Tên | Mô tả ngắn | Actor | Trang | Ưu tiên | AC | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| FR-001 | Giỏ hàng | Hệ thống phải cho thêm sản phẩm vào giỏ | UG-001 | PG-002 | Must | AC-001 | SRC-001 | Approved |
| FR-001 | Thanh toán | Hệ thống phải cho thanh toán qua cổng | UG-001 | PG-002 | Must | — | SRC-001 | Draft |
| FR-003 | Tìm kiếm | Hệ thống phải cho tìm sản phẩm | UG-001 | PG-002 | Should | — | SRC-001 | Xong |

## 10. Tích hợp

Ghi chú buổi họp: khách gửi api_key = FAKEKEYFAKEKEY000000 của cổng thanh toán và mật khẩu: Abc@12345 để kỹ thuật dùng.

## 14. Tiêu chí nghiệm thu

| AC ID | Given | When | Then | Yêu cầu | Trang |
|---|---|---|---|---|---|
| AC-001 | Khách ở PG-002 | Thêm sản phẩm vào giỏ | Giỏ hàng cập nhật nhanh và thân thiện | FR-001 | PG-002 |
