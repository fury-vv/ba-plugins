# Product Type Guide — Câu hỏi theo loại sản phẩm và UI/UX

**Mục đích:** câu hỏi bổ sung theo loại sản phẩm, và bộ câu hỏi về giao diện, nhận diện thương hiệu, trải nghiệm người dùng. Loại sản phẩm khác với lĩnh vực ngành: file này không chứa nội dung của ngành nào.
**Khi dùng:** Phase 0 (xác định loại sản phẩm), Phase 1 (hỏi nhánh liên quan). Chỉ đọc nhánh áp dụng.

## Mục lục

1. Xác định loại sản phẩm
2. Nhánh A — Website nội dung, landing page
3. Nhánh B — Ứng dụng web, công cụ nội bộ, SaaS
4. Nhánh C — Ứng dụng di động
5. Nhánh D — API, backend, dịch vụ
6. Nhánh E — Dữ liệu, báo cáo, dashboard
7. UI/UX và nhận diện thương hiệu (cho sản phẩm có giao diện)
8. Ghi kết quả UI/UX vào SRS
9. Quy tắc an toàn cho phần UI/UX

## 1. Xác định loại sản phẩm

Hỏi người dùng sản phẩm thuộc loại nào; một dự án có thể thuộc nhiều nhánh. Ghi vào trường `Product type` của §1.

| Nhánh | Dấu hiệu |
|---|---|
| A | Mục tiêu chính là giới thiệu, truyền thông, thu hút người xem |
| B | Người dùng đăng nhập để làm công việc, xử lý dữ liệu |
| C | Cần chạy trên điện thoại như ứng dụng cài đặt |
| D | Không có giao diện người dùng; phục vụ hệ thống khác |
| E | Trọng tâm là tổng hợp, phân tích, trình bày số liệu |

## 2. Nhánh A — Website nội dung, landing page

- [P0] Mục tiêu của trang: người xem cần làm gì sau khi xem (liên hệ, đăng ký, tải tài liệu…)?
- [P1] Ai cập nhật nội dung, bao lâu một lần? Có cần hệ thống quản lý nội dung không?
- [P1] Có yêu cầu về tối ưu tìm kiếm (SEO), chia sẻ mạng xã hội không?
- [P1] Có cần đo lường truy cập không? Công cụ nào? Có cần thông báo cookie và xin đồng ý không?
- [P1] Biểu mẫu thu thập thông tin gửi dữ liệu về đâu, ai xử lý?
- [P2] Có nhiều ngôn ngữ không? Nội dung các ngôn ngữ giống hay khác nhau?

## 3. Nhánh B — Ứng dụng web, công cụ nội bộ, SaaS

- [P0] Người dùng đăng nhập thế nào? Có dùng hệ thống đăng nhập sẵn có của tổ chức không?
- [P1] Những công việc chính người dùng làm hằng ngày là gì? Việc nào làm nhiều nhất?
- [P1] Có nhiều tổ chức khách hàng dùng chung (đa thuê bao) không? Dữ liệu tách thế nào?
- [P1] Có gói dịch vụ, giới hạn sử dụng theo gói không?
- [P2] Có cần chế độ dùng thử, mời người dùng, tự đăng ký không?

## 4. Nhánh C — Ứng dụng di động

- [P0] Nền tảng nào: iOS, Android, cả hai? Phiên bản hệ điều hành tối thiểu do ai quyết định?
- [P1] Có cần dùng khi không có mạng không? Dữ liệu đồng bộ lại thế nào?
- [P1] Có cần thông báo đẩy không? Cho sự kiện nào?
- [P1] Cần quyền truy cập thiết bị nào (camera, vị trí, danh bạ, tệp…)? Vì sao?
- [P1] Phát hành qua kho ứng dụng công khai hay phân phối nội bộ? Tài khoản nhà phát triển của ai?
- [P2] Cập nhật bắt buộc khi có phiên bản mới không?

## 5. Nhánh D — API, backend, dịch vụ

- [P0] Ai sẽ gọi dịch vụ này (hệ thống nào, đội nào)? Họ cần gì?
- [P1] Xác thực bên gọi thế nào? Phân quyền theo bên gọi ra sao?
- [P1] Có giới hạn tần suất gọi không? Cam kết thời gian phản hồi, độ sẵn sàng do ai đặt?
- [P1] Thay đổi phiên bản API được thông báo và hỗ trợ song song thế nào?
- [P2] Tài liệu cho bên gọi cần ở dạng nào?

Nhánh D thường không có giao diện người dùng: §13 ghi `Not applicable — <lý do>`.

## 6. Nhánh E — Dữ liệu, báo cáo, dashboard

- [P0] Ai xem, để ra quyết định gì?
- [P1] Nguồn dữ liệu nào, cập nhật bao lâu một lần, độ trễ chấp nhận được do ai đặt?
- [P1] Định nghĩa chính xác của từng chỉ số là gì? Ai chịu trách nhiệm định nghĩa đó?
- [P1] Người xem có được lọc, đi sâu vào chi tiết, xuất dữ liệu không?
- [P2] Có cần gửi báo cáo định kỳ tự động không?

## 7. UI/UX và nhận diện thương hiệu (cho sản phẩm có giao diện)

Hỏi nhóm A, C, I ở buổi đầu; các nhóm còn lại sau khi phạm vi đã rõ.

**Cách hỏi để khách trả lời được:**
- Hỏi qua ví dụ cụ thể: "thích/không thích cái này, vì sao" hiệu quả hơn "anh chị muốn màu gì".
- Xin file trước: brand guideline, logo, file thiết kế sẵn có thường trả lời được nửa số câu hỏi.
- Ghi cả lý do, không chỉ lựa chọn.

### Nhóm A — Nhận diện thương hiệu

- [P0] Đã có brand guideline chưa? Bắt buộc tuân thủ hay chỉ tham khảo? Xin file.
- [P1] Logo đủ các phiên bản (màu, đơn sắc, trên nền tối)? Xin file gốc.
- [P1] Mã màu thương hiệu chính xác (HEX/RGB; CMYK hoặc Pantone nếu có in ấn)?
- [P1] Font chữ thương hiệu là gì? Đã có bản quyền dùng cho web/app chưa?
- [P2] Giọng văn (trang trọng, thân thiện…), phong cách hình ảnh và biểu tượng?
- [P2] Có màu, hình ảnh, từ ngữ nào phải tránh?

### Nhóm B — Màu chủ đạo và theme

- [P1] Màu chính, phụ, nhấn lấy từ guideline hay cần đề xuất?
- [P1] Có cần chế độ tối không? Người dùng tự chuyển hay theo cài đặt thiết bị?
- [P1] Có cần nhiều theme (mỗi đơn vị hoặc khách hàng của họ có màu, logo riêng) không?
- [P2] Màu trạng thái (thành công, cảnh báo, lỗi) có quy ước nội bộ không?

### Nhóm C — Layout và điều hướng

- [P0] Thiết bị chính là máy tính, tablet hay điện thoại? Thiết kế ưu tiên thiết bị nào trước?
- [P1] Khi vừa mở hệ thống, người dùng cần thấy gì đầu tiên?
- [P1] Kiểu điều hướng mong muốn (menu trên, menu bên, thanh dưới trên di động)? Bao nhiêu cấp menu là chấp nhận được?
- [P1] Màn hình nên thoáng hay hiển thị dày đặc dữ liệu?
- [P2] Có màn hình nào cần in hoặc xuất PDF không?

### Nhóm D — Tham chiếu

- [P1] 2–3 website hoặc ứng dụng khách thích: thích cụ thể điểm nào?
- [P1] 1–2 cái khách không thích: vì sao?
- [P1] Hệ thống hiện tại (nếu có): giữ lại gì, nhất định bỏ gì?
- [P2] So với sản phẩm của đối thủ, muốn giống hay khác biệt ở điểm nào?

### Nhóm E — Người dùng và ngữ cảnh sử dụng

- [P1] Độ tuổi, mức quen thuộc công nghệ, tần suất sử dụng của từng nhóm người dùng?
- [P1] Môi trường sử dụng: văn phòng, ngoài trời, màn hình lớn, mạng yếu, thao tác một tay…?
- [P1] Ngôn ngữ giao diện; có cần chuyển đổi ngôn ngữ không?

### Nhóm F — Khả năng tiếp cận

- [P0] Có yêu cầu bắt buộc nào về khả năng tiếp cận (hợp đồng, chính sách, luật áp dụng)? Nếu có, mức mục tiêu là gì? Khách chưa chắc thì ghi "cần xác minh".
- [P1] Có nhóm người dùng đặc thù: người lớn tuổi, thị lực kém, chỉ dùng bàn phím, dùng trình đọc màn hình?

### Nhóm G — Design system và công cụ

- [P1] Đã có design system, thư viện giao diện bắt buộc dùng, hoặc file thiết kế sẵn có chưa?
- [P1] Ai làm thiết kế: đội dự án, đơn vị khác, hay đội của khách?
- [P2] Mức hiệu ứng chuyển động mong muốn: tối giản, vừa phải hay nhiều?

### Nhóm H — Nội dung

- [P1] Ai cung cấp chữ, hình ảnh, video? Khi nào có?
- [P2] Hình ảnh, font, biểu tượng đã có bản quyền chưa?

### Nhóm I — Quy trình duyệt thiết kế

- [P0] Ai có quyền duyệt thiết kế cuối cùng?
- [P1] Duyệt ở mức nào: wireframe, mockup chi tiết, hay prototype bấm thử được? Bao nhiêu vòng chỉnh sửa?
- [P1] Tiêu chí nghiệm thu giao diện: giống thiết kế đến mức nào, kiểm tra trên trình duyệt và thiết bị nào?

## 8. Ghi kết quả UI/UX vào SRS

| Loại | Ví dụ dạng câu | Ghi ở đâu | Ràng buộc |
|---|---|---|---|
| Ràng buộc | "Phải dùng đúng màu và logo theo brand guideline <tên file, phiên bản>" | Khối `UIR-` trong §13, có AC hoặc Verification | Có |
| Mong muốn | "Thích giao diện thoáng, ít màu" | Bảng Design Inputs §13, `UXP-`, Type `Preference` | Không; đầu vào cho thiết kế |
| Tham chiếu | "Website X: thích cách bố trí bộ lọc" | Bảng Design Inputs §13, `UXP-`, Type `Reference`, ghi rõ điểm được thích | Không; chỉ lấy cảm hứng |

- Ràng buộc cũng có thể có một dòng `UXP-` Type `Constraint` để liệt kê tài sản thương hiệu nhận được (file, phiên bản), nhưng nghĩa vụ ràng buộc phải nằm trong `UIR-`.
- Mục tiêu khả năng tiếp cận và thiết bị cần hỗ trợ ghi trong §14 (NFR), target `TBD (Q-xxx)` nếu chưa có.
- Mỗi mã màu ghi kèm nguồn (`SRC-` của guideline). Validator kiểm tra định dạng mã màu và cột Source của `UXP-`.
- Bảng Design Inputs là UX brief bàn giao cho giai đoạn thiết kế.

## 9. Quy tắc an toàn cho phần UI/UX

- Không tự chọn màu, font, layout rồi ghi như yêu cầu. Nếu đề xuất, ghi `Proposed` và chờ khách xác nhận.
- Không tự đổi mô tả thành mã màu; hỏi mã chính xác hoặc xin guideline.
- Website tham chiếu chỉ là nguồn cảm hứng; SRS không yêu cầu sao chép thiết kế của bên khác.
- Không đặt sẵn mức khả năng tiếp cận; ghi `TBD (Q-xxx)` và hỏi khách hoặc pháp chế.
- Không dựng wireframe, mockup hay bảng màu trong skill này; đó là việc của giai đoạn thiết kế.
