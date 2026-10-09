# Domain Discovery Guide — Khám phá lĩnh vực mà không giả định

**Mục đích:** cách hiểu lĩnh vực của khách hàng từ chính thông tin họ cung cấp, cách xác nhận domain, cách tách nội dung đặc thù lĩnh vực, và cách dùng domain pack an toàn.
**Khi dùng:** Phase 0–2; khi cần điền §6 (Glossary) hoặc §22 (Domain-Specific Considerations); khi người dùng cung cấp domain pack.

## Mục lục

1. Nguyên tắc
2. Rút thuật ngữ và thực thể từ đầu vào
3. Xác nhận domain
4. Tách yêu cầu chung và yêu cầu đặc thù lĩnh vực
5. Nội dung cần chuyên gia xác minh
6. Domain pack: định dạng và quy tắc sử dụng
7. Đưa tri thức từ dự án lên domain pack (cho giai đoạn sau)

## 1. Nguyên tắc

- Không chọn lĩnh vực thay người dùng. Không suy ra lĩnh vực từ vài từ khóa trong brief.
- Không đưa thực thể, vai trò, quy trình hay quy định "thường gặp" của một ngành vào SRS khi khách hàng chưa nói đến.
- Hai tổ chức cùng ngành vẫn vận hành khác nhau. Mọi thứ phải đến từ khách hàng này, có nguồn.
- Quy định theo khu vực (nơi người dùng và dữ liệu nằm) khác với quy định theo ngành; câu hỏi về khu vực nằm ở `elicitation-guide.md` mục 5.17.

## 2. Rút thuật ngữ và thực thể từ đầu vào

1. Đọc brief, ghi chú, tài liệu khách gửi. Liệt kê danh từ và cụm từ nghiệp vụ khách dùng lặp lại.
2. Với mỗi thuật ngữ: ghi đúng cách khách viết, nguồn (`SRC-`), nghĩa theo cách khách giải thích. Chưa có giải thích thì tạo `Q-` hỏi nghĩa.
3. Gom thành **sơ đồ thực thể khái niệm**: thực thể nào liên quan thực thể nào, quan hệ một-nhiều hay nhiều-nhiều. Quan hệ chưa rõ ghi `Q-`.
4. Kiểm tra từ đồng nghĩa và từ dễ hiểu nhầm: hai từ có cùng nghĩa không? Một từ có hai nghĩa ở hai bộ phận không?
5. Đưa vào §6 Glossary; thực thể và quan hệ vào §11 và sơ đồ dữ liệu khái niệm (`diagram-standard.md`).

## 3. Xác nhận domain

- Hỏi trực tiếp ở Phase 0 khi chưa rõ: "Hệ thống phục vụ hoạt động nào của tổ chức? Người dùng cuối là ai?".
- Chỉ khi người dùng xác nhận, đổi trường `Domain` trong §1 từ `Not confirmed` thành `Confirmed: <tên lĩnh vực theo cách người dùng gọi>`, ghi `DEC-` hoặc `SRC-` cho xác nhận đó.
- Trước khi domain được xác nhận, §22 phải là `Not applicable — domain chưa được xác nhận`. Validator cảnh báo nếu §22 có nội dung trong khi domain chưa xác nhận.

## 4. Tách yêu cầu chung và yêu cầu đặc thù lĩnh vực

| Loại | Ghi ở đâu |
|---|---|
| Yêu cầu không phụ thuộc lĩnh vực (đăng nhập, phân quyền, tìm kiếm, xuất dữ liệu…) | Các section chung §9–§20 |
| Yêu cầu chỉ có ý nghĩa trong lĩnh vực đã xác nhận (quy định ngành, chuẩn nghiệp vụ, thuật ngữ chuyên môn có ràng buộc) | §22, và requirement tương ứng tham chiếu tới mục đó |

Mỗi mục trong §22 ghi: nội dung, nguồn, mức chắc chắn, và ai cần xác minh.

## 5. Nội dung cần chuyên gia xác minh

- Mọi quy định pháp lý hoặc chuẩn chuyên ngành mà khách nhắc đến nhưng chưa có văn bản: ghi `Q-` với "Cần chuyên gia/pháp chế xác minh", requirement liên quan giữ `Proposed`.
- Không trích dẫn, diễn giải hay khẳng định nội dung của luật hoặc chuẩn khi chưa có nguồn khách cung cấp và chưa được xác minh.
- Không tuyên bố hệ thống tuân thủ quy định nào.

## 6. Domain pack: định dạng và quy tắc sử dụng

Domain pack là file Markdown chứa tri thức lĩnh vực **đã khái quát hóa, ẩn danh và được duyệt**, dùng chung cho nhiều dự án cùng lĩnh vực. Domain pack không phải một phần của skill này; người dùng cung cấp khi cần (đính kèm, đặt trong thư mục dự án, hoặc trong Project).

### Định dạng

```markdown
# Domain Pack — <tên lĩnh vực>

| Field | Value |
|---|---|
| Pack version | 0.1 |
| Status | Draft hoặc Reviewed |
| Reviewed by (role) | <vai trò người duyệt> |
| Last review | <ngày> |

## 1. Phạm vi của pack
## 2. Thuật ngữ thường gặp (thuật ngữ, nghĩa thường dùng, biến thể cần hỏi lại)
## 3. Quy trình điển hình (viết dưới dạng câu hỏi để xác minh với khách)
## 4. Câu hỏi hay bị bỏ sót
## 5. Rủi ro thường gặp
## 6. Quy định có thể liên quan (luôn ghi "cần chuyên gia hoặc pháp chế xác minh")
```

### Quy tắc sử dụng

1. Chỉ dùng domain pack khi domain đã được xác nhận và người dùng chỉ định pack.
2. Pack `Draft` (chưa duyệt): báo người dùng trước khi dùng.
3. Nội dung pack chỉ được dùng để **sinh câu hỏi và giả thuyết**. Mỗi gợi ý đưa vào SRS dưới dạng `Q-` hoặc `ASM-`, ghi "Theo domain pack <tên, version>, cần khách xác nhận".
4. Không chép nội dung pack thành requirement. Requirement chỉ được tạo khi khách hàng xác nhận, với nguồn là khách hàng.
5. Ghi pack đã dùng vào §26 với Type `Document`.

### Không được có trong domain pack

- Tên, logo, số liệu, tài liệu nội bộ, quy trình riêng có thể nhận diện của bất kỳ khách hàng nào.
- Dữ liệu cá nhân.
- Khẳng định pháp lý chưa được xác minh.

## 7. Đưa tri thức từ dự án lên domain pack (cho giai đoạn sau)

Skill `srs-analysis` không tự sửa domain pack. Khi kết thúc dự án, BA có thể đề xuất bổ sung theo một chiều:

1. **Khái quát hóa:** viết lại thành kiến thức chung, bỏ mọi chi tiết riêng của khách hàng.
2. **Ẩn danh:** kiểm tra không còn tên, số liệu, tài liệu có thể nhận diện.
3. **Duyệt:** người được tổ chức chỉ định duyệt trước khi đưa vào pack.

Một skill riêng (`domain-pack-curator`) sẽ hỗ trợ quy trình này trong giai đoạn sau.
