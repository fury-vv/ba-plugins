# Acceptance Criteria Standard

**Mục đích:** cách viết tiêu chí chấp nhận kiểm thử được.
**Khi dùng:** Phase 3 khi viết AC cho FR, BR, DR, IR, UIR, US; Phase 4 khi rà soát.

## Định dạng

Mỗi AC là một dòng trong khối requirement hoặc user story cha:

```markdown
- **Acceptance criteria:**
  - AC-FR-001-01: Given <bối cảnh ban đầu>, when <hành động hoặc sự kiện>, then <kết quả quan sát được>.
  - AC-FR-001-02: Given …, when …, then …
```

- ID AC phải chứa ID cha (`AC-FR-001-01` thuộc `FR-001`). Validator cảnh báo AC định nghĩa ngoài khối cha.
- Given/When/Then dùng khi có hành vi theo tình huống. Với điều kiện tĩnh (ví dụ một trường bắt buộc), có thể viết một câu khẳng định kiểm thử được.
- Có thể viết tiếng Việt: "Cho trước …, khi …, thì …".

## Tiêu chí của một AC tốt

1. **Quan sát được:** kết quả nhìn thấy hoặc đo được, không phải "hoạt động tốt", "thân thiện".
2. **Một kết quả:** mỗi AC kiểm một điều; nhiều điều thì tách AC.
3. **Không chứa giải pháp:** không nêu công nghệ, tên bảng, tên API nội bộ.
4. **Có dữ liệu cụ thể khi cần:** dùng giá trị ví dụ trung tính hoặc tham chiếu BR chứa quy tắc.
5. **Không tự đặt con số:** ngưỡng, thời hạn chưa được khách xác nhận ghi `TBD (Q-xxx)`.

## Danh mục tình huống cần cân nhắc

Không phải requirement nào cũng cần đủ, nhưng phải cân nhắc từng mục và bỏ qua có lý do:

| Tình huống | Câu hỏi gợi ý |
|---|---|
| Luồng chính | Kết quả mong đợi khi mọi thứ đúng? |
| Dữ liệu không hợp lệ | Thiếu trường, sai định dạng, vượt giới hạn thì sao? |
| Không đủ quyền | Người không có quyền thử làm thì sao? Thấy gì? |
| Trùng lặp | Gửi hai lần, tạo trùng thì sao? |
| Chuyển trạng thái không hợp lệ | Thao tác khi đối tượng ở trạng thái không cho phép thì sao? |
| Lỗi và thử lại | Lỗi giữa chừng thì dữ liệu ở trạng thái nào? Thử lại có an toàn không? |
| Hủy hoặc đảo ngược | Hủy được không, trong điều kiện nào, hệ quả gì? |
| Audit | Có cần ghi nhận ai làm, khi nào không? |
| Lỗi tích hợp | Hệ thống bên ngoài không phản hồi hoặc trả lỗi thì sao? |
| Đồng thời | Hai người thao tác cùng lúc thì sao? |

## Ví dụ dạng câu (placeholder, không gắn lĩnh vực)

- AC-FR-001-01: Given người dùng có vai trò A và đối tượng X ở trạng thái S1, when người dùng xác nhận thao tác T, then đối tượng X chuyển sang trạng thái S2 và lịch sử ghi người thực hiện, thời điểm.
- AC-FR-001-02: Given người dùng có vai trò B, when người dùng thử thao tác T trên đối tượng X, then hệ thống từ chối và hiển thị thông báo không đủ quyền; đối tượng X không thay đổi.
- AC-FR-001-03: Given đối tượng X ở trạng thái S2, when bất kỳ người dùng nào thử thao tác T, then hệ thống từ chối vì trạng thái không cho phép.
