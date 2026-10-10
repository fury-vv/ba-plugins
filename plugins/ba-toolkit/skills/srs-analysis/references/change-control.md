# Change Control — Quản lý thay đổi sau phê duyệt

**Mục đích:** quy trình xử lý yêu cầu thay đổi đối với BRD/SRS/Diagrams đã có baseline `APPROVED`.
**Khi dùng:** Phase 6.

## Quy trình

1. **Tiếp nhận.** Tạo khối `CR-` trong SRS §6, mục Change Requests (thay `Not applicable` nếu là CR đầu tiên). Ghi người yêu cầu (vai trò), ngày, lý do, nguồn (`SRC-`).
2. **Xác định phạm vi ảnh hưởng.** Liệt kê mọi ID bị ảnh hưởng: requirement, AC, story, use case, sơ đồ, GOAL, quyền, trạng thái.
3. **Đánh giá tác động** theo từng khía cạnh dưới đây. Khía cạnh chưa đánh giá được ghi `Chưa đánh giá` kèm lý do, không bỏ trống.
4. **Đưa phương án:** chấp nhận, từ chối, hoãn; có thể có phương án chấp nhận một phần.
5. **Chờ quyết định** của người có thẩm quyền. Không sửa nội dung baseline trước khi có quyết định rõ ràng.
6. **Sau khi được duyệt:**
   - tạo version nháp mới (ví dụ 1.0 → 1.1) ở **mọi file bị ảnh hưởng** (BRD/SRS/Diagrams), Status `DRAFT — NOT APPROVED`; giữ version đồng bộ giữa 3 file;
   - cập nhật requirement bị ảnh hưởng: sửa nội dung, hoặc đánh dấu `Superseded` kèm `Superseded by` khi thay bằng requirement mới (không tái sử dụng ID);
   - cập nhật sơ đồ (`diagrams.md`), traceability (SRS §6), Revision History (mỗi file bị ảnh hưởng);
   - ghi `DEC-` cho quyết định;
   - chạy lại Phase 4 (validator trên cả 3 file) và trình G5 cho version mới.
7. **Từ chối hoặc hoãn:** cập nhật Status của CR, ghi `DEC-`, baseline giữ nguyên.

## Khối CR

```markdown
### CR-001 — <Tên ngắn>
- **Requested by:** <vai trò>
- **Date:** <ngày>
- **Reason:** <lý do>
- **Source:** SRC-010
- **Affected:** FR-003, AC-FR-003-01, DIA-002
- **Impact — Scope:** <…>
- **Impact — UX:** <…>
- **Impact — Architecture:** <… hoặc Chưa đánh giá — lý do>
- **Impact — Security/Privacy:** <…>
- **Impact — Testing:** <…>
- **Impact — Cost:** <… hoặc Chưa đánh giá — lý do>
- **Impact — Timeline:** <… hoặc Chưa đánh giá — lý do>
- **Options:** Approve / Reject / Defer (kèm hệ quả của mỗi phương án)
- **Decision:** <để trống cho đến khi có quyết định>
- **Decided by:** <vai trò, theo lời người dùng>
- **Status:** Proposed
- **Resulting version:** <ví dụ 1.1, sau khi duyệt>
```

Status CR: `Proposed`, `Approved`, `Rejected`, `Deferred`, `Implemented`.

## Quy tắc version

- Bản nháp trước lần duyệt đầu: 0.1, 0.2, …
- Lần duyệt đầu: 1.0.
- Mỗi CR được duyệt và đưa vào baseline: tăng số phụ (1.1, 1.2, …).
- Chỉ tăng số chính (2.0) khi người duyệt quyết định tái baseline.
- Mỗi lần duyệt lưu bản chụp cho mỗi file bị ảnh hưởng (ví dụ `srs-vX.Y.md`, `brd-vX.Y.md`) và không sửa bản chụp đó.

## Lưu ý

- Nhiều CR nhỏ cùng lúc có thể gộp vào một version, nhưng mỗi CR vẫn có khối và quyết định riêng.
- CR mâu thuẫn với một CR khác: nêu rõ và hỏi người có thẩm quyền.
- Skill không tự thực hiện thay đổi ngoài BRD/SRS/Diagrams (code, dữ liệu, cấu hình hệ thống).
