# Sitemap & Page Inventory — Nhà hàng Lẩu Mây (dữ liệu hư cấu)

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | Website Nhà hàng Lẩu Mây |
| Tài liệu | 02 — Sitemap & Page Inventory |
| Phiên bản | 0.3 |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | I |
| Last gate passed | G3 |
| Ngày cập nhật | 2026-10-12 |

## 1. Sitemap

```
PG-001 Trang chủ (Homepage)
├── PG-002 Thực đơn (Listing)
│   └── PG-003 Chi tiết món (Detail)
├── PG-004 Đặt bàn (Booking flow)
├── PG-005 Chi nhánh (Listing)
│   └── PG-006 Chi tiết chi nhánh (Detail)
└── PG-090 Chính sách bảo mật (Legal/Support)
```

## 2. Inventory tóm tắt

| Page ID | Tên trang | Page type | Mục đích (1 dòng) | CTA chính | Dynamic/Static | Cần page spec? | Ưu tiên | Nhãn | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| PG-001 | Trang chủ | Homepage | Giới thiệu và dẫn tới đặt bàn | Đặt bàn | Dynamic | Có | Must | [KH xác nhận] | Approved |
| PG-002 | Thực đơn | Listing | Xem món theo nhóm | Đặt bàn | Dynamic | Có | Must | [KH xác nhận] | Approved |
| PG-003 | Chi tiết món | Detail | Xem ảnh và mô tả một món | Đặt bàn | Dynamic | Không | Could | [BA đề xuất] | Proposed |
| PG-004 | Đặt bàn | Checkout/Booking flow | Gửi yêu cầu đặt bàn | Gửi yêu cầu | Dynamic | Có | Must | [KH xác nhận] | Approved |
| PG-005 | Chi nhánh | Listing | Xem 2 chi nhánh | Chỉ đường | Dynamic | Không | Should | [KH xác nhận] | Approved |
| PG-006 | Chi tiết chi nhánh | Detail | Địa chỉ, giờ mở cửa, bản đồ | Đặt bàn tại chi nhánh | Dynamic | Không | Should | [KH xác nhận] | Approved |
| PG-090 | Chính sách bảo mật | Legal/Support | Thông báo xử lý dữ liệu form | — | Static | Không | Must | [KH xác nhận] | Approved |

## 4. Component inventory

| CMP ID | Tên | Dùng ở trang | Biến thể | Ghi chú visual | Ghi chú behavior | Trạng thái |
|---|---|---|---|---|---|---|
| CMP-001 | Header | Tất cả | Desktop / Mobile | Logo, menu, nút Đặt bàn | Menu mobile dạng mở rộng — TBD | Draft |
| CMP-002 | Footer | Tất cả | — | Thông tin 2 chi nhánh | — | Draft |
| CMP-003 | Nút đặt bàn cố định | Tất cả trừ PG-004 | Mobile | Cố định cuối màn hình | Mở PG-004 | Confirmed |
