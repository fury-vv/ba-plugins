# Elicitation Guide — Hướng dẫn thu thập yêu cầu

**Mục đích:** cách đặt câu hỏi và ngân hàng câu hỏi dùng chung cho mọi loại dự án.
**Khi dùng:** Phase 0 và Phase 1; khi nhập ghi chú họp; khi bảng coverage còn dòng `TBD`.

Câu hỏi theo loại sản phẩm và về UI/UX nằm ở `product-type-guide.md`. Câu hỏi về thuộc tính chất lượng nằm ở `nfr-checklist.md`.

## Mục lục

1. Cách hỏi
2. Phân loại P0/P1/P2
3. Xử lý mâu thuẫn, TBD và câu trả lời "chưa biết"
4. Tài liệu nên xin
5. Ngân hàng câu hỏi theo nhóm
6. Bảng ánh xạ nhóm câu hỏi → section SRS

## 1. Cách hỏi

- Mỗi lượt 3–7 câu, câu quan trọng nhất trước. Không dồn hết câu hỏi vào một lượt.
- Mỗi câu ghi mức ưu tiên và **vai trò nên trả lời** (chủ nghiệp vụ, người dùng cuối, IT/bảo mật, pháp chế, vận hành…). BA thường không tự trả lời được hết.
- Hỏi về **kết quả và tình huống**, không hỏi về giải pháp. Ví dụ: "Khi việc X bị trễ, ai cần biết và trong bao lâu?" thay vì "Có cần chức năng gửi thông báo không?".
- Xin **ví dụ cụ thể** và **trường hợp ngoại lệ**: "Lần gần nhất việc này đi sai là khi nào? Chuyện gì đã xảy ra?".
- Dùng **thuật ngữ của khách hàng**, ghi vào glossary; không thay bằng từ mình quen.
- Chỉ hỏi nhóm áp dụng cho dự án. Nhóm không áp dụng thì ghi `Not applicable` kèm lý do trong coverage §27.
- Mỗi câu đã hỏi được ghi vào §24 với ID `Q-`; khi có câu trả lời, ghi `Answered` và nguồn (`SRC-`).

## 2. Phân loại P0/P1/P2

| Mức | Khi nào | Ví dụ dạng câu hỏi |
|---|---|---|
| P0 | Thiếu thì không viết được đặc tả đúng, hoặc có rủi ro nghiêm trọng (pháp lý, bảo mật, mất dữ liệu, sai phạm vi) | Ai phê duyệt SRS? Phạm vi bao gồm/loại trừ gì? Ai được làm hành động nhạy cảm nhất? |
| P1 | Cần để phát hành MVP | Luồng ngoại lệ chính, dữ liệu bắt buộc, tích hợp cần có ngay |
| P2 | Có thể xử lý sau nếu ghi nhận rủi ro | Báo cáo bổ sung, tùy chọn hiển thị, tối ưu sau phát hành |

Mức trong ngân hàng câu hỏi bên dưới chỉ là gợi ý; điều chỉnh theo dự án.

## 3. Xử lý mâu thuẫn, TBD và câu trả lời "chưa biết"

- **Mâu thuẫn:** trình bày nguyên văn ý của hai bên kèm nguồn, nêu hệ quả của mỗi cách hiểu, hỏi người có thẩm quyền quyết định. Ghi `Q-` (P0 hoặc P1). Khi có quyết định, ghi `DEC-`.
- **"Chưa biết":** ghi `TBD (Q-xxx)` ở chỗ cần, kèm người sẽ trả lời. Có thể đề xuất một giả định (`ASM-`) để làm tiếp, ghi rõ cần ai xác nhận.
- **Câu trả lời mơ hồ** ("nhanh", "dễ dùng", "an toàn"): hỏi tiếp cách đo hoặc tình huống cụ thể. Không tự gán con số.
- **Người trả lời không có thẩm quyền:** ghi lại như thông tin tham khảo, requirement giữ `Proposed`, hỏi người có thẩm quyền xác nhận.

## 4. Tài liệu nên xin

Xin trước, hỏi sau; tài liệu thường trả lời được nhiều câu hỏi cùng lúc. Nhắc khách ẩn danh dữ liệu cá nhân trước khi gửi.

- Tài liệu quy trình, quy định nội bộ đang áp dụng.
- Biểu mẫu, phiếu, mẫu báo cáo đang dùng.
- Ảnh màn hình hoặc tài liệu hướng dẫn của hệ thống hiện có.
- Dữ liệu mẫu đã ẩn danh (vài dòng là đủ).
- Danh sách người dùng theo vai trò (không cần tên).
- Brand guideline, logo, file thiết kế sẵn có (xem `product-type-guide.md`).
- Hợp đồng hoặc phụ lục kỹ thuật nếu có điều khoản về chất lượng, bảo mật, dữ liệu.

Mỗi tài liệu nhận được ghi thành một dòng `SRC-` trong §26.

## 5. Ngân hàng câu hỏi theo nhóm

### 5.1 Kết quả kinh doanh và chỉ số thành công

- [P0] Vấn đề cần giải quyết là gì? Ai đang chịu ảnh hưởng và ảnh hưởng thế nào?
- [P0] Nếu dự án thành công, điều gì sẽ khác so với hiện tại?
- [P1] Đo thành công bằng chỉ số nào? Giá trị hiện tại là bao nhiêu, đo ở đâu?
- [P1] Có mốc thời gian hoặc sự kiện bên ngoài nào khiến dự án phải xong trước một thời điểm?

### 5.2 Stakeholder và thẩm quyền

- [P0] Ai chịu trách nhiệm nghiệp vụ? Ai có quyền phê duyệt SRS và thay đổi sau này?
- [P0] Khi các bên không đồng ý, ai quyết định?
- [P1] Những bộ phận nào bị ảnh hưởng nhưng chưa tham gia trao đổi?
- [P1] Ai là đầu mối trả lời cho từng mảng (nghiệp vụ, IT, bảo mật, pháp chế, vận hành)?

### 5.3 Người dùng và đặc điểm

- [P0] Có những nhóm người dùng nào? Mỗi nhóm cần làm gì với hệ thống?
- [P1] Mỗi nhóm có khoảng bao nhiêu người, dùng thường xuyên đến đâu?
- [P1] Họ dùng thiết bị gì, trong môi trường nào, mức quen thuộc với công nghệ ra sao?
- [P2] Có nhóm người dùng có nhu cầu đặc thù (thị lực, ngôn ngữ, kết nối mạng yếu…)?

### 5.4 Phạm vi, MVP, ngân sách và thời gian

- [P0] Những gì chắc chắn nằm trong phạm vi? Những gì chắc chắn không?
- [P0] Bản phát hành đầu tiên cần tối thiểu những gì để dùng được?
- [P1] Ngân sách, mốc thời gian, nguồn lực có giới hạn gì ảnh hưởng đến phạm vi?
- [P1] Đây là sản phẩm mới, module mới, cải tiến hay thay thế hệ thống cũ?

### 5.5 Quy trình hiện tại và mong muốn

- [P0] Hiện nay công việc này được làm thế nào, theo các bước nào, ai làm bước nào?
- [P1] Điểm nào trong quy trình hiện tại gây tốn thời gian, lỗi hoặc tranh cãi nhiều nhất?
- [P1] Quy trình mong muốn khác hiện tại ở đâu? Bước nào cần bỏ, gộp, tự động hóa?

### 5.6 Chi tiết luồng và ngoại lệ

- [P0] Điều gì khởi động luồng này? Cần điều kiện gì trước khi bắt đầu?
- [P1] Luồng diễn ra bình thường thế nào từ đầu đến cuối?
- [P1] Có thể đi sai ở đâu? Khi đó cần xảy ra điều gì?
- [P1] Có thể hủy, quay lại, sửa sau khi đã hoàn tất không? Ai được làm và trong điều kiện nào?
- [P2] Nếu bị gián đoạn giữa chừng, người dùng tiếp tục thế nào?

### 5.7 Quy tắc nghiệp vụ

- [P1] Có công thức tính toán, ngưỡng, hạn mức nào không? Ai đặt và ai được thay đổi?
- [P1] Có quy tắc theo thời gian không: hạn chót, lịch chạy định kỳ, múi giờ, ngày nghỉ?
- [P1] Có quy tắc đánh số, đặt mã, định dạng bắt buộc nào không?
- [P2] Quy tắc nào thay đổi thường xuyên và cần cấu hình được thay vì cố định?

### 5.8 Trạng thái và vòng đời

- [P1] Đối tượng chính trải qua những trạng thái nào? Điều gì làm nó chuyển trạng thái?
- [P1] Ai được chuyển trạng thái nào? Có chuyển ngược được không?
- [P2] Đối tượng kết thúc vòng đời thế nào: lưu trữ, xóa, khóa?

### 5.9 Dữ liệu

- [P0] Dữ liệu nào bắt buộc phải có? Nguồn gốc chuẩn của từng loại dữ liệu là ở đâu?
- [P1] Có dữ liệu cá nhân hoặc dữ liệu cần bảo mật không? Mức độ nhạy cảm thế nào?
- [P1] Khối lượng dữ liệu và số giao dịch dự kiến, tốc độ tăng, thời điểm cao điểm?
- [P1] Kiểm tra hợp lệ thế nào? Xử lý trùng lặp thế nào?
- [P1] Dữ liệu được giữ bao lâu, ai được xóa, xóa thế nào?

### 5.10 Phân quyền

- [P0] Hành động nào nhạy cảm nhất? Ai được làm?
- [P1] Quyền theo vai trò, theo dữ liệu mình tạo, theo đơn vị, hay kết hợp?
- [P1] Có ủy quyền, làm thay, hoặc phê duyệt nhiều cấp không?
- [P2] Có cần ẩn một số trường dữ liệu với một số vai trò không?

### 5.11 Nhiều tổ chức hoặc đơn vị

- [P1] Hệ thống phục vụ một hay nhiều tổ chức, chi nhánh, đơn vị? Dữ liệu giữa chúng tách hay chung?
- [P2] Mỗi đơn vị có cấu hình, quy tắc, giao diện riêng không?

### 5.12 Thao tác đồng thời và hàng loạt

- [P1] Nhiều người có thể sửa cùng một dữ liệu cùng lúc không? Khi đó xử lý thế nào?
- [P2] Có cần nhập, sửa, duyệt hàng loạt không?

### 5.13 Tích hợp, nhập và xuất dữ liệu

- [P0] Hệ thống phải trao đổi dữ liệu với hệ thống nào? Bên nào là nguồn chuẩn?
- [P1] Chiều trao đổi, tần suất, khối lượng? Khi hệ thống bên kia lỗi thì sao?
- [P1] Có cần nhập dữ liệu từ file hoặc xuất ra file không? Định dạng nào?

### 5.14 Tìm kiếm, báo cáo và thông báo

- [P1] Người dùng cần tìm gì, theo tiêu chí nào?
- [P1] Cần báo cáo nào, ai xem, bao lâu một lần, ở định dạng nào?
- [P1] Sự kiện nào cần thông báo, cho ai, qua kênh nào? Người nhận có được tắt không?

### 5.15 Audit, bảo mật và quyền riêng tư

- [P1] Cần ghi lại ai làm gì, khi nào, với dữ liệu nào? Giữ nhật ký bao lâu, ai được xem?
- [P1] Có chính sách bảo mật nội bộ nào hệ thống phải tuân theo?
- [P1] Người dùng đăng nhập thế nào? Có dùng hệ thống đăng nhập sẵn có của tổ chức không?

### 5.16 Quản trị và cấu hình

- [P1] Dữ liệu danh mục (danh sách dùng chung) nào cần quản lý? Ai duy trì?
- [P2] Tham số nào cần cấu hình mà không phải sửa phần mềm?

### 5.17 Pháp lý theo khu vực (không phụ thuộc lĩnh vực)

- [P0] Người dùng và dữ liệu nằm ở quốc gia, khu vực nào?
- [P1] Có yêu cầu nào về lưu trữ dữ liệu trong nước, đồng ý của người dùng, quyền xóa dữ liệu không?
- [P1] Có điều khoản hợp đồng nào ràng buộc về dữ liệu, bảo mật, khả năng tiếp cận?

Skill **không khẳng định** luật nào áp dụng. Ghi câu trả lời là `ASM-` hoặc `Q-` với ghi chú "Cần pháp chế xác minh".

### 5.18 Chuyển đổi, triển khai, vận hành và nghiệm thu

- [P1] Có dữ liệu cũ cần chuyển sang không? Khối lượng, chất lượng, ai chịu trách nhiệm làm sạch?
- [P1] Triển khai một lần hay theo giai đoạn? Có chạy song song với hệ thống cũ không? Quay lui thế nào?
- [P1] Ai thực hiện nghiệm thu (UAT), trên môi trường nào, tiêu chí ký nhận là gì?
- [P2] Ai đào tạo người dùng? Ai hỗ trợ sau khi đưa vào sử dụng, trong giờ nào?

## 6. Bảng ánh xạ nhóm câu hỏi → section SRS

| Nhóm | Section |
|---|---|
| 5.1 | §2, §3 |
| 5.2 | §5, §29 |
| 5.3 | §5 |
| 5.4 | §4, §7 |
| 5.5, 5.6 | §8, §9 |
| 5.7 | §10 |
| 5.8 | §17 |
| 5.9 | §11, §19 |
| 5.10 | §16 |
| 5.11 | §11, §16 |
| 5.12 | §9, §14 |
| 5.13 | §12, §18 |
| 5.14 | §18 |
| 5.15 | §19 |
| 5.16 | §9, §11 |
| 5.17 | §7, §19 |
| 5.18 | §20 |
| `product-type-guide.md` | §13 và các section liên quan |
| `nfr-checklist.md` | §14 |
| `domain-discovery-guide.md` | §6, §22 |
