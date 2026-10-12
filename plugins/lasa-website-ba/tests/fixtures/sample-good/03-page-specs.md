# Page Specifications — Nhà hàng Lẩu Mây (dữ liệu hư cấu)

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | Website Nhà hàng Lẩu Mây |
| Tài liệu | 03 — Page Specifications |
| Phiên bản | 0.2 |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | I |
| Last gate passed | G3 |
| Ngày cập nhật | 2026-10-12 |

## PG-004 — Đặt bàn (Checkout/Booking flow)

### 2. Thứ bậc thông tin & section

| # | Section | Visual (designer) | Behavior (developer) | Dữ liệu / nguồn | Ghi chú mobile |
|---|---|---|---|---|---|
| 1 | Chọn chi nhánh | 2 lựa chọn dạng thẻ | Bắt buộc chọn 1; mặc định theo trang trước nếu đến từ PG-006 | Danh sách chi nhánh (CMS) | Xếp dọc |
| 2 | Thông tin đặt bàn | Form 1 cột | Xem bảng form; luồng FR-001 | Người dùng nhập | Bàn phím số cho SĐT |
| 3 | Xác nhận | Thông báo thành công | Hiển thị sau khi gửi thành công | — | — |

### 5. Form

| Trường | Kiểu | Bắt buộc | Validation | Thông báo lỗi | Ghi chú |
|---|---|---|---|---|---|
| Họ tên | Text | Có | Không rỗng | "Vui lòng nhập họ tên" | |
| Số điện thoại | Tel | Có | Định dạng số điện thoại Việt Nam | "Số điện thoại chưa hợp lệ" | |
| Ngày giờ | Date-time | Có | Theo BR-001 | "Vui lòng chọn thời gian hợp lệ" | |
| Số khách | Number | Có | ≥ 1; tối đa TBD (Q-001) | "Số khách chưa hợp lệ" | |
| Ghi chú | Text | Không | — | — | |

### 7. Trạng thái màn hình

| Trạng thái | Hiển thị | Hành vi |
|---|---|---|
| Success | "Nhà hàng đã nhận yêu cầu và sẽ gọi lại xác nhận" | Gửi thông báo theo FR-002 |
| Error | Thông báo lỗi gửi và số hotline | Giữ dữ liệu đã nhập |
| Unavailable | Thời gian ngoài BR-001 không chọn được | — |

### 13. Acceptance criteria

| AC ID | Given | When | Then | FR liên quan |
|---|---|---|---|---|
| AC-001 | Thực khách ở PG-004 | Gửi form với đủ trường bắt buộc hợp lệ | Hiển thị thông báo thành công và yêu cầu được ghi nhận | FR-001 |
| AC-002 | Thực khách ở PG-004 | Gửi form thiếu số điện thoại | Hiển thị lỗi tại trường số điện thoại, không gửi yêu cầu | FR-001 |
| AC-003 | Một yêu cầu đặt bàn vừa được ghi nhận | Hệ thống xử lý yêu cầu | Email thông báo gửi tới địa chỉ của chi nhánh đã chọn | FR-002 |
