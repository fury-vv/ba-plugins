# User Story Standard

**Mục đích:** cách viết user story nhất quán và liên kết được với requirement.
**Khi dùng:** Phase 3, khi điền §15.

## Định dạng

```markdown
### US-001 — <Tên ngắn>
- **Story:** As a <vai trò>, I want <khả năng>, so that <giá trị nghiệp vụ>.
- **Related:** FR-001, BR-002
- **Dependencies:** US-003 (nếu có)
- **Scope note:** <điều nằm ngoài story này, nếu cần làm rõ>
- **Priority:** Must
- **Status:** Proposed
- **Acceptance criteria:**
  - AC-US-001-01: Given …, when …, then …
```

Câu story có thể viết tiếng Việt theo cùng cấu trúc: "Là <vai trò>, tôi muốn <khả năng>, để <giá trị>."

## Quy tắc

1. **Vai trò** phải là vai trò đã có trong §5, không dùng "người dùng" chung chung khi có nhiều vai trò.
2. **Giá trị** nói lợi ích nghiệp vụ, không lặp lại khả năng.
3. Mỗi story có ít nhất một ID trong `Related` trỏ tới FR. Story không thay thế requirement.
4. Story **không thay thế** business rule (§10) và NFR (§14). Quy tắc và thuộc tính chất lượng phải có khối riêng.
5. Acceptance criteria: định nghĩa `AC-US-…` tại story, hoặc tham chiếu AC của FR liên quan (ví dụ "see AC-FR-001-01"). Không để story không có AC.
6. Một story đủ nhỏ để hoàn thành trong một vòng phát triển; story quá lớn thì tách và ghi `Dependencies`.
7. Story chưa được khách xác nhận giữ `Proposed`.

## Kiểm tra nhanh

- [ ] Vai trò có trong §5
- [ ] Có giá trị nghiệp vụ rõ ràng
- [ ] `Related` có ít nhất một FR
- [ ] Có AC (định nghĩa hoặc tham chiếu)
- [ ] Không chứa giải pháp kỹ thuật (tên công nghệ, cấu trúc bảng…)
