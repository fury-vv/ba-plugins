# SRS / BA Package — Nhà hàng Lẩu Mây (dữ liệu hư cấu)

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | Website Nhà hàng Lẩu Mây |
| Tài liệu | 04 — SRS / BA Package |
| Phiên bản | 0.3 |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | I |
| Last gate passed | G3 |
| Ngày cập nhật | 2026-10-12 |
| Tác giả | BA mẫu |
| Người duyệt | STK-001 |

Tài liệu tham chiếu thực hành ISO/IEC/IEEE 29148; không tuyên bố tuân thủ.

## 2. Bối cảnh kinh doanh & phạm vi

| ID | Loại trừ | Lý do | Nguồn |
|---|---|---|---|
| EXC-001 | Đặt món giao hàng trên website | Khách dùng ứng dụng giao đồ ăn bên ngoài | SRC-001 |

## 4. Giả định, ràng buộc, phụ thuộc

| ID | Loại | Nội dung | Nguồn | Trạng thái |
|---|---|---|---|---|
| CON-001 | Ràng buộc | Đặt bàn là yêu cầu, nhân viên gọi lại xác nhận; không giữ chỗ tự động | SRC-001 | Confirmed |
| DEP-001 | Phụ thuộc | Khách cung cấp ảnh món và nội dung thực đơn | SRC-001 | Confirmed |

## 8. Yêu cầu chức năng

### 8.1 Bảng tổng hợp

| ID | Tên | Mô tả ngắn | Actor | Trang | Ưu tiên | AC | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| FR-001 | Gửi yêu cầu đặt bàn | Hệ thống phải cho thực khách gửi yêu cầu đặt bàn theo chi nhánh | UG-001 | PG-004 | Must | AC-001, AC-002 | SRC-001 | Approved |
| FR-002 | Thông báo yêu cầu đặt bàn | Hệ thống phải gửi email thông báo tới chi nhánh được chọn | UG-002 | PG-004 | Must | AC-003 | SRC-001 | Approved |
| FR-003 | Quản trị thực đơn | Hệ thống phải cho UG-002 thêm, sửa, ẩn món và nhóm món | UG-002 | PG-002 | Must | AC-004 | SRC-001 | Approved |
| FR-004 | Hiển thị chi nhánh | Hệ thống phải hiển thị địa chỉ, giờ mở cửa và bản đồ từng chi nhánh | UG-001 | PG-006 | Should | — | SRC-001 | Confirmed |

### 8.3 Quy tắc nghiệp vụ

| ID | Quy tắc | Áp dụng cho | Nguồn | Trạng thái |
|---|---|---|---|---|
| BR-001 | Chỉ nhận đặt bàn trong giờ mở cửa của chi nhánh, trước ít nhất 2 giờ (khách nêu) | FR-001 | SRC-001 | Confirmed |

## 9. Yêu cầu phi chức năng

| ID | Nhóm | Yêu cầu | Tiêu chí đo | Phương pháp kiểm | Ưu tiên | Nguồn | Trạng thái |
|---|---|---|---|---|---|---|---|
| NFR-001 | Hiệu năng | Trang PG-001, PG-002 tải đủ nhanh trên di động | TBD (Q-002) | TBD | Should | SRC-001 | Needs clarification |
| NFR-002 | Quyền riêng tư | Chỉ thu thập trường cần cho đặt bàn; có thông báo tại PG-090 | Form chỉ gồm trường ở page spec PG-004 | Review form | Must | SRC-001 | Confirmed |

## 10. Yêu cầu tích hợp

| ID | Hệ thống | Mục đích | Dữ liệu trao đổi | Chiều | Tần suất / kích hoạt | Xử lý lỗi | Chủ sở hữu tài khoản | Ưu tiên | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| INT-001 | Email chi nhánh | Nhận yêu cầu đặt bàn | Nội dung form PG-004 | Web → Email | Mỗi yêu cầu | Lỗi gửi → hiển thị hotline (PG-004 Error) | Chủ nhà hàng | Must | Confirmed |

## 11. Nội dung & CMS

| ID | Yêu cầu | Chủ sở hữu nội dung | Người sản xuất | Quyền chỉnh sửa | Quy trình duyệt | Trạng thái |
|---|---|---|---|---|---|---|
| CNT-001 | Thực đơn và ảnh món | Chủ nhà hàng | Nhân viên marketing của khách | UG-002 | Không cần duyệt | Confirmed |

## 12. SEO & analytics

| ID | Yêu cầu | Chi tiết | Nguồn | Trạng thái |
|---|---|---|---|---|
| SEO-001 | Đo chuyển đổi đặt bàn | Ghi nhận sự kiện gửi form thành công ở PG-004 | SRC-001 | Confirmed |

## 13. Domain, hosting, migration & deployment

| ID | Hạng mục | Hiện trạng | Yêu cầu / ràng buộc | Người phụ trách | Trạng thái |
|---|---|---|---|---|---|
| DH-001 | Tên miền | Khách đã có, đứng tên công ty | Chủ nhà hàng duyệt thay đổi DNS | STK-001 | Confirmed |
| DH-002 | Email doanh nghiệp phụ thuộc tên miền | Không dùng email theo tên miền | Không áp dụng | — | Confirmed |
| DH-003 | Hosting | Khách có hosting cũ, chưa rõ cấu hình | Cần kiểm chứng kỹ thuật | Kỹ thuật LASA | Needs clarification |

## 14. Tiêu chí nghiệm thu

| AC ID | Given | When | Then | Yêu cầu | Trang |
|---|---|---|---|---|---|
| AC-004 | UG-002 đã đăng nhập quản trị | Ẩn một món | Món không còn hiển thị ở PG-002 | FR-003 | PG-002 |

AC-001 đến AC-003: xem `03-page-specs.md`.

## 15. Rủi ro, loại trừ, câu hỏi mở & quyết định

| ID | Rủi ro | Khả năng | Ảnh hưởng | Giảm thiểu | Người phụ trách |
|---|---|---|---|---|---|
| RSK-001 | Yêu cầu đặt bàn bị bỏ sót nếu không ai kiểm tra email | Trung bình | Cao | Xác nhận ASM-001; cân nhắc kênh thông báo thứ hai | STK-002 |
