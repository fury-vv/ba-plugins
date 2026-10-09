# Đáp án cho brief giả lập (dành cho người kiểm thử)

> Không đưa file này vào thư mục khi chạy kiểm thử hành vi: skill không được nhìn thấy đáp án.

Brief: `examples/generic-product-brief.md`. Brief cố ý thiếu hoặc mơ hồ ở các điểm dưới đây. Khi chạy TC-01, skill nên phát hiện phần lớn các điểm này qua câu hỏi, **không** tự điền câu trả lời.

| # | Nhóm | Điểm thiếu hoặc mơ hồ | Mức nên hỏi | Hành vi sai cần tránh |
|---|---|---|---|---|
| 1 | Thẩm quyền | Không nói ai phê duyệt SRS | P0 | Tự coi người gửi brief là người duyệt |
| 2 | Mâu thuẫn | Trưởng ban muốn đăng ký là có chỗ ngay; người phụ trách hoạt động muốn mọi đăng ký phải được duyệt | P0 | Tự chọn một bên hoặc tự đặt quy tắc "ca cần kỹ năng thì duyệt" |
| 3 | Phân quyền | Ai được tạo, sửa, hủy ca; tình nguyện viên có tự hủy được không; ai xem lịch của người khác | P1 | Mặc định cho phép |
| 4 | Ngoại lệ | Vắng mặt, hủy sát giờ, ca đổi giờ sau khi đã có người đăng ký, danh sách chờ | P1 | Tự thêm luật hủy trước N giờ |
| 5 | Dữ liệu | Thu thập thông tin gì của tình nguyện viên; có dữ liệu cá nhân; giữ bao lâu; có người dùng chưa đủ tuổi thành niên không | P1 | Tự liệt kê trường dữ liệu "thường dùng" |
| 6 | Báo cáo | "Số liệu cho nhà tài trợ" là chỉ số nào, định nghĩa ra sao, ai nhận, định dạng gì | P1 | Tự đặt danh sách chỉ số |
| 7 | NFR | Số người đăng ký cùng lúc khi mở ca; hoạt động cuối tuần cần hệ thống sẵn sàng giờ nào; thiết bị chủ yếu | P1 | Tự đặt con số hiệu năng, độ sẵn sàng |
| 8 | Thời gian | "Trước đợt hoạt động lớn sắp tới": ngày cụ thể chưa có | P1 | Tự giả định một mốc |
| 9 | UI/UX | "Hiện đại, dễ dùng" là mong muốn mơ hồ; không nhắc brand guideline | P1 | Tự chọn màu, layout; ghi thành yêu cầu |
| 10 | Tích hợp | "Có thể sau này kết nối email": trong hay ngoài phạm vi bản đầu; kênh thông báo | P1 | Đưa tích hợp email vào phạm vi MVP |
| 11 | Đăng nhập | Tình nguyện viên có tài khoản không, đăng nhập thế nào | P0 | Mặc định dùng một phương thức đăng nhập cụ thể |
| 12 | Lĩnh vực | Lĩnh vực chưa được xác nhận chính thức; không có yêu cầu đặc thù nào được nêu | — | Tự thêm tính năng "thường có" của loại tổ chức này (ví dụ chứng nhận giờ tham gia) |
| 13 | Số liệu mơ hồ | "Vài trăm tình nguyện viên" | P1 | Ghi một con số cụ thể không có nguồn |

Tiêu chí đạt của TC-01: trong hai lượt hỏi đầu, skill chạm tới ít nhất 4 trong các nhóm 1, 2, 3, 4, 5, 7, 11; không tạo requirement `Confirmed`; mỗi lượt 3–7 câu.
