# Discovery Brief — Nhà hàng Lẩu Mây (dữ liệu hư cấu)

## Document control

| Trường | Giá trị |
|---|---|
| Dự án | Website Nhà hàng Lẩu Mây |
| Tài liệu | 01 — Discovery Brief |
| Phiên bản | 0.4 |
| Trạng thái | DRAFT — NOT APPROVED |
| Current phase | I |
| Last gate passed | G3 |
| Ngày cập nhật | 2026-10-12 |
| BA | BA mẫu |

## 1. Tóm tắt nhanh

Nhà hàng lẩu 2 chi nhánh muốn website giới thiệu thực đơn và nhận yêu cầu đặt bàn; nhân viên gọi lại xác nhận. Design approach: thiết kế riêng (DEC-002). Câu hỏi mở lớn nhất: mục tiêu tốc độ trang (Q-002).

## 2. Design approach (A1)

| Trường | Giá trị | Nhãn | Nguồn |
|---|---|---|---|
| Lựa chọn | D lúc đầu → B sau khi xem bảng phương án | [KH xác nhận] | SRC-001, DEC-002 |
| Theme (nếu A) | Không áp dụng | — | — |

## 3. Bối cảnh kinh doanh

| Mục | Nội dung | Nhãn | Nguồn |
|---|---|---|---|
| Công ty & mô hình kinh doanh | Nhà hàng lẩu, 2 chi nhánh | [KH xác nhận] | SRC-001 |
| Đối tượng mục tiêu | Nhóm bạn, gia đình, công ty đặt tiệc | [KH xác nhận] | SRC-001 |
| Thị trường & ngôn ngữ | Trong nước, tiếng Việt | [KH xác nhận] | SRC-001 |
| Ngân sách | Khách chưa chia sẻ | [Câu hỏi mở] | — |

### 3.1 Mục tiêu kinh doanh

| ID | Mục tiêu | Cách đo (nếu có) | Nhãn | Nguồn |
|---|---|---|---|---|
| BG-001 | Tăng số yêu cầu đặt bàn qua kênh trực tuyến | Số yêu cầu đặt bàn/tháng — ngưỡng TBD (Q-001) | [KH xác nhận] | SRC-001 |
| BG-002 | Giúp khách xem thực đơn và chi nhánh trước khi đến | Không đo định lượng | [KH xác nhận] | SRC-001 |

### 3.3 Stakeholder & quyền duyệt

| ID | Vai trò / tên | Quan tâm | Quyền duyệt (gate nào) | Nhãn |
|---|---|---|---|---|
| STK-001 | Chủ nhà hàng | Doanh thu, hình ảnh thương hiệu | G1–G4 | [KH xác nhận] |
| STK-002 | Quản lý chi nhánh | Xử lý đặt bàn | Góp ý G2–G3 | [KH xác nhận] |

## 6. Nhóm người dùng

| ID | Nhóm | Nhu cầu chính | Cần đăng nhập? | Nhãn |
|---|---|---|---|---|
| UG-001 | Thực khách | Xem thực đơn, gửi yêu cầu đặt bàn | Không | [KH xác nhận] |
| UG-002 | Nhân viên quản trị | Cập nhật thực đơn, nhận yêu cầu đặt bàn | Có | [KH xác nhận] |

## 9. Đã nêu sớm – xử lý ở Phase H

| # | Nội dung khách nêu | Nguồn | Ghi chú |
|---|---|---|---|
| 1 | "Đã mua tên miền rồi" | SRC-001 | Đã xử lý ở Phase H → DH-001 |

## 10. Giả định

| ID | Giả định | Lý do | Cần ai xác nhận | Trạng thái |
|---|---|---|---|---|
| ASM-001 | Nhân viên kiểm tra email đặt bàn trong giờ mở cửa | Cần để FR-002 có ý nghĩa | STK-002 | Open |

## 11. Câu hỏi mở

| ID | Câu hỏi | Mức (P0/P1/P2) | Ảnh hưởng | Người trả lời | Hạn | Trạng thái |
|---|---|---|---|---|---|---|
| Q-001 | Mục tiêu số yêu cầu đặt bàn/tháng? | P2 | Đo BG-001 | STK-001 | — | Open |
| Q-002 | Mục tiêu tốc độ tải trang và công cụ đo? | P1 | NFR-001 | STK-001 | — | Open |
| Q-003 | Hosting hiện tại có đáp ứng giải pháp không? | P1 | DH-003 | Kỹ thuật LASA | — | Open |

## 12. Nguồn

| ID | Loại (buổi họp/email/file/trang LASA) | Mô tả | Ngày | Người cung cấp |
|---|---|---|---|---|
| SRC-001 | Buổi họp | Phỏng vấn discovery | 2026-10-12 | STK-001 |
| SRC-002 | Trang LASA | https://lasa.vn/bao-gia/ — nhóm "Nhà hàng, café" | 2026-10-12 | BA |
