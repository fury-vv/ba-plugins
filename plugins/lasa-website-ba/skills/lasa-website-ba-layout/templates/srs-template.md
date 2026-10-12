# SRS / BA Package — <Tên dự án>

<!-- Tham chiếu thực hành ISO/IEC/IEEE 29148; KHÔNG tuyên bố tuân thủ (R-21). Bỏ mục không liên quan bằng cách ghi "Không áp dụng — lý do", không xoá im lặng. Không đưa vào yêu cầu nào chưa có nguồn. Mọi số liệu NFR chưa có → TBD (Q-xxx). -->

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | <tên> |
| Tài liệu | 04 — SRS / BA Package |
| Phiên bản | 0.1 |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | I |
| Last gate passed | G3 |
| Ngày cập nhật | <YYYY-MM-DD> |
| Tác giả | <BA> |
| Người duyệt | <STK-xxx> |

## 1. Tổng quan tài liệu & mục tiêu dự án

- Mục đích tài liệu:
- Người đọc: Layout/UI designer, developer, tester, PM, khách hàng
- Tài liệu liên quan: 01-discovery-brief, 02-sitemap-page-inventory, 03-page-specs, 05-rtm, 06-decision-log

| ID | Mục tiêu kinh doanh | Cách đo | Nguồn | Trạng thái |
|---|---|---|---|---|
| BG-001 | | TBD (Q-) | SRC- | |

## 2. Bối cảnh kinh doanh & phạm vi

### 2.1 Bối cảnh
### 2.2 Trong phạm vi
### 2.3 Ngoài phạm vi

| ID | Loại trừ | Lý do | Nguồn |
|---|---|---|---|
| EXC-001 | | | |

## 3. Stakeholder & nhóm người dùng

| ID | Stakeholder | Vai trò | Quyền duyệt |
|---|---|---|---|
| STK-001 | | | |

| ID | Nhóm người dùng | Mô tả | Mục tiêu | Quyền |
|---|---|---|---|---|
| UG-001 | | | | |

### 3.1 Ma trận vai trò & quyền (nếu có quản trị/đăng nhập)

| Chức năng / dữ liệu | UG-001 | UG-002 | Quản trị |
|---|---|---|---|
| | Xem / Tạo / Sửa / Xoá / Duyệt / TBD (Q-) | | |

## 4. Giả định, ràng buộc, phụ thuộc

| ID | Loại | Nội dung | Nguồn | Trạng thái |
|---|---|---|---|---|
| ASM-001 | Giả định | | | Open |
| CON-001 | Ràng buộc | | | |
| DEP-001 | Phụ thuộc | | | |

## 5. Loại website & design approach

| Mục | Nội dung | Nhãn |
|---|---|---|
| Ngành chính / phụ | | |
| Design approach | A / B / C / D → DEC- | |
| Theme (nếu có) | tên, URL, ngày kiểm tra, mức kiểm chứng | |
| Artifact thiết kế nguồn chuẩn | | |
| Brand & visual (ràng buộc / mong muốn / tham khảo) | | |

## 6. Sitemap & page inventory

Tóm tắt từ `02-sitemap-page-inventory.md` (sitemap + bảng inventory). Bản đầy đủ ở file 02.

## 7. Đặc tả layout theo trang

Tóm tắt trang Must và liên kết đến `03-page-specs.md`.

| Page ID | Tên | Page type | Spec | Trạng thái |
|---|---|---|---|---|

## 8. Yêu cầu chức năng

### 8.1 Bảng tổng hợp

| ID | Tên | Mô tả ngắn | Actor | Trang | Ưu tiên | AC | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| FR-001 | | Hệ thống phải … | UG- | PG- | Must | AC- | SRC- | |

### 8.2 Đặc tả chi tiết (FR có luồng)

<!-- Dùng định dạng ở references/srs-quality-checklist.md §1.5 -->

### 8.3 Quy tắc nghiệp vụ

| ID | Quy tắc | Áp dụng cho | Nguồn | Trạng thái |
|---|---|---|---|---|
| BR-001 | | FR- | | |

## 9. Yêu cầu phi chức năng

| ID | Nhóm | Yêu cầu | Tiêu chí đo | Phương pháp kiểm | Ưu tiên | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|---|
| NFR-001 | Hiệu năng | | TBD (Q-) | | | | |

## 10. Yêu cầu tích hợp

| ID | Hệ thống | Mục đích | Dữ liệu trao đổi | Chiều | Tần suất / kích hoạt | Xử lý lỗi | Chủ sở hữu tài khoản | Ưu tiên | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| INT-001 | | | | Web → X / X → Web | | | | | |

<!-- Không ghi credential (R-13). -->

## 11. Nội dung & CMS

| ID | Yêu cầu | Chủ sở hữu nội dung | Người sản xuất | Quyền chỉnh sửa | Quy trình duyệt | Trạng thái |
|---|---|---|---|---|---|---|
| CNT-001 | | | | | | |

### 11.1 Nội dung hiện có & migration nội dung

## 12. SEO & analytics

| ID | Yêu cầu | Chi tiết | Nguồn | Trạng thái |
|---|---|---|---|---|
| SEO-001 | Metadata / URL / redirect / index / tracking | | | |

## 13. Domain, hosting, migration & deployment

| ID | Hạng mục | Hiện trạng | Yêu cầu / ràng buộc | Người phụ trách | Trạng thái |
|---|---|---|---|---|---|
| DH-001 | Tên miền | | | | |
| DH-002 | Email doanh nghiệp phụ thuộc tên miền | | | | |
| DH-003 | Hosting | | | | |
| DH-004 | Migration / redirect / rollback | | | | |

## 14. Tiêu chí nghiệm thu

| AC ID | Given | When | Then | Yêu cầu | Trang |
|---|---|---|---|---|---|
| AC-001 | | | | FR- | PG- |

### 14.1 Điều kiện nghiệm thu tổng thể
<!-- Ai nghiệm thu, trên môi trường nào, thiết bị/trình duyệt nào — chỉ ghi khi đã thống nhất. -->

## 15. Rủi ro, loại trừ, câu hỏi mở & quyết định

| ID | Rủi ro | Khả năng | Ảnh hưởng | Giảm thiểu | Người phụ trách |
|---|---|---|---|---|---|
| RSK-001 | | | | | |

| ID | Câu hỏi mở | Mức | Ảnh hưởng | Người trả lời | Trạng thái |
|---|---|---|---|---|---|
| Q-001 | | P0 | | | Open |

Quyết định: xem `06-decision-log.md`.

## 16. Trạng thái phê duyệt & lịch sử thay đổi

| Gate | Trạng thái | Ngày | Người xác nhận | DEC |
|---|---|---|---|---|
| G1 | | | | |
| G2 | | | | |
| G3 | | | | |
| G4 | | | | |

| Phiên bản | Ngày | Thay đổi | Người cập nhật |
|---|---|---|---|
| 0.1 | | Khởi tạo | |
