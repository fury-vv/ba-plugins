# SRS Quality Checklist & Conventions

Tham chiếu thực hành kỹ nghệ yêu cầu (đặc tính yêu cầu tốt trong ISO/IEC/IEEE 29148). Tài liệu do skill tạo **không** được tuyên bố là tuân thủ/chứng nhận theo chuẩn (R-21).

---

## §1. Quy ước

### 1.1 Tiền tố ID

| Tiền tố | Dùng cho | Tiền tố | Dùng cho |
|---|---|---|---|
| `BG-` | Mục tiêu kinh doanh | `CNT-` | Nội dung & CMS |
| `STK-` | Stakeholder | `SEO-` | SEO & analytics |
| `UG-` | Nhóm người dùng | `DH-` | Domain, hosting, migration, deployment |
| `PG-` | Trang (page) | `BR-` | Quy tắc nghiệp vụ |
| `CMP-` | Component tái sử dụng | `AC-` | Tiêu chí nghiệm thu |
| `FR-` | Yêu cầu chức năng | `ASM-` | Giả định |
| `NFR-` | Yêu cầu phi chức năng | `CON-` | Ràng buộc |
| `INT-` | Tích hợp | `DEP-` | Phụ thuộc |
| `RSK-` | Rủi ro | `Q-` | Câu hỏi mở |
| `DEC-` | Quyết định | `CR-` | Yêu cầu thay đổi |
| `SRC-` | Nguồn thông tin (buổi họp, email, file, trang LASA) | `EXC-` | Loại trừ phạm vi |

Định dạng 3 chữ số (`FR-001`). Không đánh số lại, không tái sử dụng ID; mục bị bỏ: trạng thái `Withdrawn`, mục bị thay: `Superseded by <ID>`.

### 1.2 Trạng thái yêu cầu

| Trạng thái | Nghĩa | Ai đặt |
|---|---|---|
| `Draft` | Mới ghi, chưa xem lại | Agent |
| `Proposed` | BA/agent đề xuất, khách chưa nói | Agent/BA |
| `Needs clarification` | Có câu hỏi mở liên quan (`Q-`) | Agent |
| `Confirmed` | Khách/BA xác nhận nội dung, có `SRC-` | Theo câu trả lời |
| `Approved` | Đã qua gate G3/G4 với xác nhận rõ ràng | Chỉ sau gate |
| `Deferred` | Để phiên bản sau | Khách/BA quyết |
| `Out of scope` | Ngoài phạm vi | Khách/BA quyết, ghi `EXC-` |
| `Withdrawn` / `Superseded by …` | Bị bỏ / bị thay | Qua `CR-`/`DEC-` |

Chuyển `Proposed → Confirmed` cần câu trả lời có nguồn. Chuyển sang `Approved` cần gate (R-05, R-14).

### 1.3 Ưu tiên MoSCoW
`Must` (thiếu thì không ra mắt) · `Should` (quan trọng, có cách tạm) · `Could` (nếu còn nguồn lực) · `Won't (this release)`. Ưu tiên do khách quyết; agent chỉ đề xuất có nhãn.

### 1.4 Nhãn thông tin
`[KH xác nhận]` · `[Nguồn LASA – <ngày>]` · `[BA đề xuất]` · `[Giả định]` · `[Câu hỏi mở]` · `[Đã duyệt]`

### 1.5 Định dạng FR kiểm thử được
Dùng cho FR có luồng (form, booking, checkout, đăng nhập, tích hợp). FR đơn giản có thể dùng dạng bảng một dòng.

```
### FR-xxx — <Tên>
| Trường | Nội dung |
|---|---|
| Mô tả | Hệ thống phải … |
| Actor | UG-xxx |
| Tiền điều kiện | … |
| Kích hoạt | … |
| Luồng chính | 1. … 2. … |
| Luồng thay thế / lỗi | A1. … E1. … |
| Quy tắc nghiệp vụ | BR-xxx |
| Trang liên quan | PG-xxx |
| Ưu tiên | Must/Should/Could/Won't |
| Tiêu chí nghiệm thu | AC-xxx (Given/When/Then) |
| Nguồn | SRC-xxx |
| Truy vết | BG-xxx |
| Trạng thái | … |
```

### 1.6 Tiêu chí nghiệm thu
Dạng Given / When / Then, mỗi AC kiểm được bằng quan sát. Ví dụ (chỉ minh hoạ):
`AC-001: Given khách đang ở PG-010 Liên hệ, When gửi form với các trường bắt buộc hợp lệ, Then hiển thị thông báo xác nhận và yêu cầu được gửi tới kênh nhận đã thống nhất (INT-002).`

---

## §2. Checklist FR theo nhóm (Phase F)

Chỉ áp dụng nhóm liên quan. Với mỗi nhóm, các câu hỏi phải có câu trả lời hoặc `Q-`.

| Nhóm | Phải làm rõ |
|---|---|
| Quản lý nội dung | Loại nội dung nào quản trị được; ai tạo/sửa/xoá; duyệt trước khi đăng; lịch đăng; phiên bản/khôi phục |
| Search & filter | Tìm trên đối tượng nào; trường lọc; sắp xếp mặc định; không có kết quả |
| Form & lead | Trường, bắt buộc, validation, chống spam, dữ liệu đi đâu, ai nhận thông báo, đồng ý xử lý dữ liệu |
| Auth & tài khoản | Ai cần tài khoản; đăng ký/đăng nhập bằng gì; quên mật khẩu; xoá tài khoản; dữ liệu hồ sơ |
| Booking / đặt chỗ | Tài nguyên (người/phòng/bàn/chỗ); khung giờ; xác nhận thủ công/tự động; huỷ/đổi; cọc; nhắc lịch; chống trùng |
| E-commerce & checkout | Sản phẩm/biến thể/tồn kho; giỏ; phí ship; khuyến mãi; trạng thái đơn; đổi trả |
| Thanh toán | Phương thức; cổng; xử lý thất bại/huỷ/hoàn; đối soát; ai giữ tài khoản cổng |
| Thông báo | Sự kiện nào, gửi ai, kênh nào, nội dung do ai soạn |
| Upload / download | Loại & dung lượng file (`TBD` nếu chưa có), ai được tải, quét/giới hạn |
| Tích hợp | Xem `INT-` trong SRS §10 |
| Báo cáo & analytics | Báo cáo nào, cho ai, tần suất; sự kiện chuyển đổi cần đo |
| Vai trò & quyền quản trị | Danh sách vai trò; ma trận quyền; quyền chưa rõ ghi `TBD (Q-)` — không mặc định cho phép |

---

## §3. Checklist NFR (Phase F)

Ghi NFR chỉ khi có cơ sở; mục tiêu số do khách/BA cung cấp, không có → `TBD (Q-xxx)` (R-12).

| Nhóm | Câu hỏi để có tiêu chí đo được |
|---|---|
| Hiệu năng | Trang nào quan trọng nhất về tốc độ? Có mục tiêu đo bằng công cụ nào (ví dụ PageSpeed) và ngưỡng bao nhiêu? |
| Bảo mật & quyền riêng tư | Dữ liệu cá nhân nào được thu thập, lưu bao lâu, ai truy cập? Có dữ liệu nhạy cảm (sức khoẻ, tài chính) không? Chính sách bảo mật do ai soạn? |
| Accessibility | Có yêu cầu mức chuẩn cụ thể không? |
| Responsive | Thiết bị/kích thước mục tiêu? (breakpoint do designer đề xuất) |
| Tương thích trình duyệt | Trình duyệt/phiên bản nào bắt buộc hỗ trợ? |
| Availability | Có yêu cầu thời gian hoạt động, khung bảo trì không? |
| Backup & recovery | Tần suất backup, thời gian lưu, thời gian khôi phục chấp nhận được? |
| Khả năng mở rộng | Quy mô dữ liệu/người dùng dự kiến lúc ra mắt và sau 12 tháng? |
| Bảo trì | Ai cập nhật nội dung/plugin/phiên bản sau bàn giao? |
| SEO | Yêu cầu kỹ thuật SEO (sitemap XML, meta, schema, URL thân thiện, canonical)? |
| Bản địa hoá | Ngôn ngữ, tiền tệ, định dạng ngày/số, múi giờ? |

---

## §4. Chất lượng từng yêu cầu

Mỗi yêu cầu phải:
- [ ] **Cần thiết** — truy vết được về `BG-` hoặc nguồn `SRC-`.
- [ ] **Đơn nhất** — một yêu cầu, một hành vi (không "và/hoặc" gộp nhiều chức năng).
- [ ] **Không mơ hồ** — không chứa từ ở danh sách dưới mà thiếu định nghĩa đo được.
- [ ] **Kiểm thử được** — có `AC-` quan sát được.
- [ ] **Khả thi** — hoặc đã có `Q-` kiểm chứng kỹ thuật.
- [ ] **Đúng** — khớp với lời khách (nguồn), không phải suy diễn.
- [ ] **Có ưu tiên, trạng thái, nguồn.**
- [ ] **Không mô tả cách làm** (công nghệ, plugin) trừ khi là ràng buộc của khách (`CON-`).

**Từ mơ hồ cần thay bằng tiêu chí:** nhanh, mượt, đẹp, hiện đại, sang trọng, chuyên nghiệp, thân thiện, dễ dùng, trực quan, tối ưu, bảo mật cao, ổn định, linh hoạt, đầy đủ, nhiều, ít, v.v., hỗ trợ tốt, tương tự website X, *fast, user-friendly, modern, intuitive, secure, robust, flexible, etc., as needed*. (Từ cảm nhận như "sang trọng" được phép ở **Visual – Mong muốn** cho designer, nhưng không được dùng làm tiêu chí nghiệm thu.)

**Toàn bộ bộ yêu cầu:**
- [ ] Nhất quán — không có hai yêu cầu mâu thuẫn chưa giải quyết.
- [ ] Đầy đủ theo phạm vi — mọi trang Must có spec; mọi form có FR; mọi tích hợp có INT; mọi FR Must có AC.
- [ ] Mọi listing có detail tương ứng (hoặc lý do không cần) và ngược lại (R-10).
- [ ] Mọi component động có nguồn dữ liệu và FR/Q quản trị (R-11).
- [ ] Không có số liệu NFR do agent tự đặt (R-12).
- [ ] Không có tính năng theme/giá/thời hạn chưa kiểm chứng (R-04, R-18).
- [ ] Không có bí mật trong tài liệu (R-13).

---

## §5. Xếp hạng câu hỏi mở

| Mức | Ảnh hưởng | Ví dụ |
|---|---|---|
| **P0** | Kiến trúc/phạm vi/khả thi — đổi câu trả lời là đổi giải pháp | Design approach; thanh toán online; đồng bộ OTA/ERP; người ngoài đăng tin; đa ngôn ngữ; dữ liệu nhạy cảm |
| **P1** | Layout/chi phí/tiến độ đáng kể | Số trang, cấu trúc lọc, workflow duyệt, nguồn nội dung, migration |
| **P2** | Chi tiết, có thể quyết sau | Hiệu ứng, thứ tự section phụ, nội dung FAQ |

Khi trình ở gate, sắp theo: P0 → P1 → P2; trong cùng mức, theo thứ tự ảnh hưởng **kiến trúc → layout → chi phí → tiến độ → rủi ro bàn giao**. Mỗi `Q-` có: câu hỏi, mức, ảnh hưởng, người cần trả lời (khách/BA/kỹ thuật LASA/kinh doanh LASA), hạn (nếu có), trạng thái.

---

## §6. Checklist gate

### G1 — Business discovery
- [ ] Design approach đã ghi (hoặc `Q-` P0 nếu D).
- [ ] Mục tiêu kinh doanh (`BG-`) và mục tiêu chuyển đổi.
- [ ] Nhóm người dùng (`UG-`), stakeholder & người duyệt (`STK-`).
- [ ] Website hiện tại / migration (có/không).
- [ ] Không có câu hỏi domain/hosting đã được hỏi (R-06).
- [ ] Xác nhận rõ ràng của BA/khách → ghi `DEC-` "G1 passed".

### G2 — Sitemap
- [ ] Ngành chính/phụ đã xác nhận.
- [ ] Mọi trang có Page ID, page type, mục đích, ưu tiên, trạng thái.
- [ ] Listing/detail tách riêng (R-10).
- [ ] Chỉ có page type liên quan.
- [ ] Trang `[BA đề xuất]` được khách chấp nhận hoặc loại.

### G3 — Requirements baseline
- [ ] Trang Must có page spec (hoặc `Q-` liệt kê phần thiếu).
- [ ] FR/NFR/INT/CNT/SEO có ID, ưu tiên, trạng thái, nguồn.
- [ ] FR Must có AC.
- [ ] NFR không có số tự đặt.
- [ ] Tích hợp có dữ liệu trao đổi, xử lý lỗi, chủ sở hữu tài khoản.

### G4 — Scope & handoff
- [ ] Phase H đã hoàn tất hoặc bỏ qua có `DEC-` rủi ro.
- [ ] Không còn `Q-` P0 mở (hoặc có `DEC-` chấp nhận rủi ro).
- [ ] Mâu thuẫn đã giải quyết.
- [ ] Phạm vi, loại trừ (`EXC-`), giả định (`ASM-`), rủi ro (`RSK-`) đã liệt kê.
- [ ] RTM đầy đủ: mọi `BG-` có ít nhất một yêu cầu; mọi FR Must có AC và trang.
- [ ] Xác nhận rõ ràng cho (a) yêu cầu Must, (b) sitemap, (c) phạm vi → `DEC-` "G4 passed", ngày, người duyệt.
- [ ] Lint script đã chạy và báo kết quả (hoặc ghi rõ chưa chạy được).

---

## §7. Sẵn sàng bàn giao theo người nhận

| Người nhận | Cần có |
|---|---|
| Layout/UI designer | Design approach, brand/artifact, sitemap, page spec (Visual), component inventory, responsive notes, trạng thái màn hình |
| Developer | Page spec (Behavior), FR với luồng & lỗi, INT, NFR, vai trò & quyền, data/migration, DH |
| Tester | AC cho mọi FR Must, trạng thái màn hình, quyền, trình duyệt/thiết bị cần test |
| PM | Phạm vi, ưu tiên, loại trừ, rủi ro, phụ thuộc, câu hỏi mở và người phụ trách, decision log |
