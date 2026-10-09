# NFR Checklist — Yêu cầu phi chức năng

**Mục đích:** danh mục thuộc tính chất lượng cần cân nhắc, câu hỏi tương ứng, và cách ghi khi chưa có chỉ tiêu.
**Khi dùng:** Phase 1 (hỏi), Phase 3 (viết §14), Phase 4 (rà soát).

## Mục lục

1. Quy tắc chung
2. Cách ghi một NFR
3. Danh mục hạng mục và câu hỏi
4. Khi khách hàng không biết trả lời

## 1. Quy tắc chung

- **Không tự đặt chỉ tiêu định lượng.** Mọi con số (thời gian phản hồi, độ sẵn sàng, thời gian khôi phục, số người dùng đồng thời…) phải đến từ khách hàng, hợp đồng, hoặc chính sách đã có nguồn. Chưa có thì ghi `TBD (Q-xxx)`.
- Có thể **đề xuất** một chỉ tiêu để khách cân nhắc, nhưng requirement giữ `Proposed`, ghi rõ "Đề xuất, chờ xác nhận" trong `Notes`.
- Cân nhắc mọi hạng mục; hạng mục không áp dụng ghi lý do trong coverage hoặc trong §14.
- Mỗi NFR phải có `Target` (giá trị hoặc `TBD (Q-xxx)`) và `Verification`.

## 2. Cách ghi một NFR

```markdown
### NFR-001 — <Tên ngắn>
- **Category:** <hạng mục>
- **Statement:** Hệ thống phải <thuộc tính chất lượng đo được>.
- **Metric:** <đo bằng gì, đo ở đâu, trong điều kiện nào>
- **Target:** TBD (Q-007)
- **Source:** SRC-002
- **Priority:** Should
- **Status:** Proposed
- **Verification:** Test
```

## 3. Danh mục hạng mục và câu hỏi

| Hạng mục | Câu hỏi cần hỏi |
|---|---|
| Bảo mật | Có chính sách bảo mật nội bộ nào phải theo? Dữ liệu nào cần bảo vệ đặc biệt? Đăng nhập thế nào, có xác thực nhiều lớp không? |
| Quyền riêng tư | Có dữ liệu cá nhân không? Người dùng có quyền xem, sửa, xóa dữ liệu của mình không? Cần đồng ý của người dùng ở bước nào? |
| Phân quyền | Kiểm soát truy cập theo vai trò, theo dữ liệu, theo đơn vị? Phiên đăng nhập hết hạn khi nào? |
| Hiệu năng | Thao tác nào người dùng nhạy cảm với tốc độ nhất? Chấp nhận chờ bao lâu, do ai đặt? |
| Dung lượng và mở rộng | Bao nhiêu người dùng, bao nhiêu dữ liệu hiện tại và sau 1–3 năm? Có cao điểm theo mùa, theo ngày không? |
| Độ sẵn sàng | Hệ thống cần hoạt động vào những giờ nào? Ngừng bao lâu thì ảnh hưởng nghiêm trọng? Có khung giờ bảo trì được phép không? |
| Độ tin cậy và xử lý lỗi | Khi lỗi, điều gì tuyệt đối không được xảy ra (mất dữ liệu, ghi trùng…)? |
| Sao lưu và khôi phục | Chấp nhận mất tối đa bao nhiêu dữ liệu gần nhất? Cần khôi phục trong bao lâu? Ai quyết định khôi phục? |
| Khả năng sử dụng | Người dùng mới cần làm được việc chính sau bao lâu, có cần đào tạo không? |
| Khả năng tiếp cận | Có yêu cầu bắt buộc (hợp đồng, chính sách, luật) không? Mức mục tiêu? Nhóm người dùng đặc thù? |
| Tương thích và thiết bị | Trình duyệt, hệ điều hành, thiết bị, kích thước màn hình phải hỗ trợ? Ai quyết định danh sách? |
| Bản địa hóa | Ngôn ngữ, định dạng ngày giờ, số, tiền tệ, múi giờ? |
| Khả năng quan sát | Ai cần biết khi hệ thống gặp sự cố? Cần theo dõi chỉ số vận hành nào? |
| Khả năng bảo trì | Ai sẽ vận hành và bảo trì sau bàn giao? Có ràng buộc công nghệ của tổ chức không? |
| Lưu trữ dữ liệu | Mỗi loại dữ liệu giữ bao lâu? Sau đó lưu trữ hay xóa? |
| Hỗ trợ vận hành | Hỗ trợ người dùng trong giờ nào, qua kênh nào, ai chịu trách nhiệm? |
| Audit | Hành động nào cần ghi nhật ký? Ai xem nhật ký? Giữ bao lâu? |

## 4. Khi khách hàng không biết trả lời

- Hỏi theo tình huống thay vì con số: "Nếu hệ thống ngừng 1 giờ vào giờ làm việc thì chuyện gì xảy ra?".
- Hỏi về hệ thống hiện tại: "Hiện nay mất bao lâu? Có ai phàn nàn không?".
- Nếu vẫn chưa có: ghi `TBD (Q-xxx)`, chỉ định vai trò sẽ trả lời, ghi rủi ro trong §23 nếu thiếu chỉ tiêu ảnh hưởng thiết kế.
