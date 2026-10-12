# Sitemap & Page Inventory — <Tên dự án>

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | <tên> |
| Tài liệu | 02 — Sitemap & Page Inventory |
| Phiên bản | 0.1 |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | D |
| Last gate passed | G1 |
| Ngày cập nhật | <YYYY-MM-DD> |

## 1. Sitemap

<!-- Cây phân cấp. Mỗi nút: Page ID + tên + (page type). Nhãn [BA đề xuất] cho trang khách chưa xác nhận. -->

```
PG-001 Trang chủ (Homepage)
├── PG-002 Giới thiệu (Static)
├── PG-003 Dịch vụ (Listing)
│   └── PG-004 Chi tiết dịch vụ (Detail)
├── PG-005 Đặt lịch (Booking flow)
├── PG-006 Liên hệ (Form)
└── PG-090 Chính sách bảo mật (Legal)
```

## 2. Inventory tóm tắt

Page type hợp lệ: `Homepage` · `Landing` · `Listing` · `Search results` · `Detail` · `Form` · `Auth/Account` · `Checkout/Booking flow` · `Dashboard/Portal` · `Legal/Support` · `Static`

| Page ID | Tên trang | Page type | Mục đích (1 dòng) | CTA chính | Dynamic/Static | Cần page spec? | Ưu tiên | Nhãn | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| PG-001 | | Homepage | | | | Có | Must | | Draft |

<!-- Kiểm tra R-10: mỗi Listing phải có Detail tương ứng (hoặc ghi lý do). -->

## 3. Thẻ trang

<!-- Lặp cho mỗi trang. Trang đơn giản (Static/Legal) có thể chỉ điền các trường đánh dấu *. Trường chưa biết: TBD (Q-xxx). -->

### PG-001 — <Tên trang>

| Trường | Nội dung |
|---|---|
| Page ID * | PG-001 |
| Tên trang * | |
| Page type * | |
| Mục đích * | |
| Đối tượng (UG) | |
| Entry points (đến từ đâu) | |
| CTA chính / phụ | |
| Section & thứ tự | 1. … 2. … |
| Nguồn nội dung / dữ liệu | |
| Component tái sử dụng (CMP) | |
| Dynamic / Static * | |
| Interaction | |
| Trang liên quan & điều hướng | |
| Desktop / Tablet / Mobile | |
| SEO | |
| Quyền truy cập | Public / Đăng nhập / Vai trò … |
| Acceptance criteria | AC- |
| Ưu tiên * | Must / Should / Could / Won't |
| Nhãn * | |
| Trạng thái duyệt * | Draft / Proposed / Confirmed / Approved |

## 4. Component inventory

| CMP ID | Tên | Dùng ở trang | Biến thể | Ghi chú visual | Ghi chú behavior | Trạng thái |
|---|---|---|---|---|---|---|
| CMP-001 | Header | Tất cả | Desktop / Mobile | | | Draft |
| CMP-002 | Footer | Tất cả | | | | Draft |

## 5. Điều hướng

| Menu | Mục (theo thứ tự) | Ghi chú |
|---|---|---|
| Header | | |
| Footer | | |
| Mobile | | |

## 6. Câu hỏi mở liên quan sitemap

| Q ID | Câu hỏi | Mức | Trang liên quan |
|---|---|---|---|
