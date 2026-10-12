# Design & Layout Guide

Hướng dẫn thu thập yêu cầu thiết kế/layout để bàn giao cho Layout/UI designer. Skill **thu thập và phân loại** yêu cầu, **không** ra quyết định thiết kế thay khách hay designer (R-09, R-12). Không tự đổi mô tả màu ("xanh dương đậm") thành mã màu; không tự chọn font, breakpoint, grid.

---

## §1. Câu hỏi A1 — design approach

Luôn là câu hỏi đầu tiên (R-01). Mẫu để BA đọc cho khách:

> **[Phase A · A1]** Anh/chị muốn làm website theo hướng nào?
> (A) Chọn một mẫu giao diện có sẵn trong kho theme của LASA rồi chỉnh theo thương hiệu
> (B) Thiết kế riêng hoàn toàn theo yêu cầu
> (C) Thiết kế riêng dựa trên ý tưởng đã có — bản vẽ phác, wireframe, file Figma hoặc website tham khảo
> (D) Chưa quyết, muốn được tư vấn
> _Vì sao hỏi:_ lựa chọn này quyết định phần lớn chi phí, thời gian và cách chúng ta làm các bước sau.

Ghi nhận:
- Nhãn `[KH xác nhận]` nếu khách trả lời rõ; nếu BA đoán từ ngữ cảnh → `[Giả định]` + xác nhận ở G1.
- (A) mà chưa chọn theme cụ thể → ghi `Q-xxx` "Chọn theme" (P0), tiếp tục Phase A.
- (C) → hỏi ngay khách có thể gửi artifact (link/file) không; ghi danh sách artifact ở Brief §4.
- (D) → không tư vấn ngay; thu thập yêu cầu trước (xem §5).

---

## §2. Nhánh A — Theme có sẵn

Thứ tự hỏi (bỏ mục đã biết):
1. Tên theme + URL trang chi tiết + URL demo. Chưa chọn → khách muốn BA gợi ý theo ngành không? (gợi ý bằng bộ lọc trong `lasa-catalog.md` §3 — không khẳng định tính năng).
2. Các trang demo nào khách thích/dùng? Ánh xạ demo page ↔ Page ID trong sitemap.
3. Với từng trang: section nào **giữ / bỏ / đổi thứ tự / tuỳ biến**? Ghi bảng:

   | Page ID | Demo URL | Section | Hành động (Giữ/Bỏ/Đổi thứ tự/Tuỳ biến) | Mô tả tuỳ biến | Trạng thái |
   |---|---|---|---|---|---|

4. Branding: logo, màu, font, hình ảnh, giọng văn — khách đã có gì?
5. Trang khách cần mà demo **không có**.
6. Chức năng khách cần mà demo **không thể hiện** (ví dụ đặt lịch thời gian thực, đa ngôn ngữ, thanh toán).
7. Tuỳ biến riêng cho mobile/tablet (ẩn/hiện, đổi thứ tự section, menu).
8. Câu hỏi khả thi kỹ thuật → `Q-xxx` cho đội kỹ thuật LASA (R-18), ví dụ: "Theme X có hỗ trợ plugin đặt lịch Y không?".

**Rủi ro thường gặp cần ghi vào RSK:** tuỳ biến nhiều đến mức gần như thiết kế lại; chức năng thiếu phải thêm plugin chưa kiểm chứng tương thích; nội dung thật dài/ngắn khác demo làm vỡ layout.

---

## §3. Nhánh B — Thiết kế riêng

Thu thập theo nhóm; mỗi mục ghi là **Ràng buộc** (bắt buộc theo), **Mong muốn** (ưu tiên nhưng linh hoạt), hoặc **Tham khảo** (cảm hứng).

| Nhóm | Câu hỏi chính |
|---|---|
| Brand | Có bộ nhận diện/brand guideline không? Logo các phiên bản? Màu, font chính thức? |
| Layout guide | Có quy định bố cục sẵn (từ agency trước, website khác của tập đoàn) không? |
| Sitemap | Khách đã có danh sách trang/sơ đồ chưa? (đối chiếu Phase D) |
| Artifact | Wireframe, Figma, phác thảo tay, website tham khảo? Thích điểm gì ở từng tham khảo — *cụ thể* (bố cục, màu, ảnh, chuyển động, chức năng)? |
| Grid & content width | Có yêu cầu về độ rộng nội dung, số cột không? [Thường để designer đề xuất — ghi `TBD`, không tự đặt số] |
| Typography, màu, spacing, visual hierarchy | Cảm giác mong muốn (sang trọng, trẻ trung, tối giản…) → ghi nguyên văn; điều gì *không* muốn? |
| Component | Header (cố định khi cuộn?), footer, menu (mega menu?), card, button, form, breadcrumb, pagination, banner… có yêu cầu riêng? |
| Responsive | Thiết bị khách hàng chủ yếu dùng? Có yêu cầu hành vi riêng trên mobile (menu, CTA cố định, ẩn section)? |
| Interaction & animation | Mức độ chuyển động mong muốn; có hiệu ứng bắt buộc/cấm? (lưu ý ảnh hưởng hiệu năng & accessibility) |
| Duyệt thiết kế | Ai duyệt, bao nhiêu vòng (theo gói — `Cần LASA xác nhận`), duyệt trên gì (Figma, ảnh, bản demo)? |

---

## §4. Nhánh C — Đã có ý tưởng/artifact

Như §3, cộng thêm 4 câu hỏi bắt buộc (ghi vào Brief §4 "Quyết định thiết kế đã có"):
1. **Cố định:** quyết định nào không được thay đổi?
2. **Linh hoạt:** phần nào designer được đề xuất khác?
3. **Nguồn chuẩn:** khi Figma, phác thảo và lời mô tả mâu thuẫn — artifact nào thắng? (ghi thứ tự ưu tiên)
4. **Chưa quyết:** phần nào chưa có ý tưởng?

Với mỗi artifact ghi: tên, loại, link, phiên bản/ngày, phạm vi (trang nào), trạng thái (`Authoritative` / `Reference` / `Outdated`). Không tự diễn giải wireframe thành hành vi chức năng (R-11) — hỏi lại hành vi.

---

## §5. Nhánh D — Chưa quyết

1. Không tư vấn ngay. Đi tiếp Phase B, D (sitemap sơ bộ), F (chức năng chính) để có dữ kiện.
2. Khi đã có mục tiêu, sitemap sơ bộ và danh sách chức năng Must, trình bảng trung lập (không ghi giá — R-04):

| Tiêu chí | Theme có sẵn (A) | Thiết kế riêng (B) | Thiết kế riêng từ ý tưởng có sẵn (C) |
|---|---|---|---|
| Mức độ khác biệt thương hiệu | Giới hạn bởi theme | Cao | Cao, bám ý tưởng khách |
| Phụ thuộc vào việc tìm được theme khớp | Cao | Không | Không |
| Khớp với chức năng đặc thù đã nêu | Cần kiểm chứng từng theme | Thiết kế theo yêu cầu | Thiết kế theo yêu cầu |
| Công sức duyệt thiết kế của khách | Thấp hơn | Cao hơn | Trung bình |
| Chi phí & thời gian | `Cần LASA xác nhận` | `Cần LASA xác nhận` | `Cần LASA xác nhận` |

3. Nêu các yêu cầu đã thu thập ảnh hưởng thế nào đến lựa chọn (ví dụ: "đặt phòng đồng bộ OTA" → cần kiểm chứng theme). Để khách chọn; ghi `DEC-xxx` khi chọn.

---

## §6. Phân loại trang & phân biệt listing / detail

| Page type | Đặc điểm nhận diện | Trường đặc tả bắt buộc thêm |
|---|---|---|
| Homepage | Điểm vào chính, tổng hợp | Thứ tự section, nguồn dữ liệu từng khối (thủ công/tự động) |
| Landing | Một mục tiêu chuyển đổi, thường từ quảng cáo | CTA duy nhất, tracking, trang cảm ơn |
| Category / Listing | Hiển thị **nhiều** bản ghi cùng loại | Tiêu chí lọc, sắp xếp mặc định, phân trang/tải thêm, số bản ghi/trang, card hiển thị trường nào, empty state |
| Search results | Listing sinh từ từ khoá | Phạm vi tìm (đối tượng nào), không có kết quả, gợi ý |
| Detail | Hiển thị **một** bản ghi | Trường hiển thị, media, CTA, nội dung liên quan, bản ghi không tồn tại/ẩn |
| Form & conversion flow | Thu thập dữ liệu/hành động | Trường, validation, thông báo lỗi, sau khi gửi, chống spam, nơi dữ liệu đi đến |
| Auth / Account | Đăng ký, đăng nhập, hồ sơ | Phương thức đăng nhập, quên mật khẩu, dữ liệu hồ sơ, quyền |
| Checkout / Booking flow | Nhiều bước có trạng thái | Các bước, quay lại/bỏ dở, thanh toán, xác nhận, huỷ |
| Dashboard / Portal | Khu vực sau đăng nhập theo vai trò | Vai trò, widget/dữ liệu, thao tác |
| Legal / Policy / Support | Nội dung tĩnh bắt buộc | Ai cung cấp nội dung, nơi liên kết đến |

**Quy tắc listing/detail (R-10):** "Trang sản phẩm" là mơ hồ — luôn tách thành `PG-xxx Danh mục sản phẩm (Listing)` và `PG-yyy Chi tiết sản phẩm (Detail)`. Ghi quan hệ: listing → detail (click card), detail → listing (breadcrumb/quay lại). Một listing có thể có nhiều biến thể (theo danh mục, theo tag) dùng chung một template — ghi là một Page ID với tham số, không nhân bản.

---

## §7. Tách Visual và Behavior (R-11)

Mỗi section trong page spec có hai cột:

| Section | Visual (designer) | Behavior (developer/tester) |
|---|---|---|
| Ví dụ: Banner carousel | 3–5 slide, ảnh + tiêu đề + CTA `[TBD Q-xxx]` | Tự chuyển? Khoảng thời gian `TBD`; dữ liệu do quản trị nhập (FR-xxx); 0 slide → ẩn section |

Câu hỏi bắt buộc khi gặp component động: dữ liệu từ đâu? ai cập nhật? có giới hạn số lượng? khi không có dữ liệu thì sao? hành động khi click?

**Component inventory** (ghi ở sitemap template §4): mỗi component tái sử dụng có `CMP-xxx`, danh sách trang dùng, biến thể, trạng thái. Header/footer/card/form/button luôn là component dùng chung — đặc tả một lần.

---

## §8. Trạng thái & tương tác

Với mỗi trang có dữ liệu động/form/flow, hỏi đủ các trạng thái áp dụng:

| Trạng thái | Câu hỏi |
|---|---|
| Loading | Có hiển thị gì khi đang tải (skeleton, spinner)? |
| Empty | Không có dữ liệu (danh mục trống, tìm không thấy) thì hiển thị gì, gợi ý gì? |
| Error | Lỗi hệ thống/kết nối hiển thị gì, người dùng làm gì tiếp? |
| Success | Sau khi gửi form/đặt hàng/đặt lịch thành công: thông báo, chuyển trang, email/tin nhắn? |
| Unavailable | Hết hàng, hết phòng, hết chỗ, ngoài giờ làm việc, tin hết hạn — hiển thị và hành vi? |
| Validation | Trường nào bắt buộc, định dạng, thông báo lỗi ở đâu, khi nào kiểm tra? |
| Permission | Người chưa đăng nhập/không đủ quyền thấy gì? |

Tương tác cần hỏi khi xuất hiện: filter, search (gợi ý tự động?), sort, pagination vs tải thêm, tab, accordion, carousel, modal/popup (khi nào hiện, có lặp lại không), sticky CTA, chat widget, chia sẻ.

---

## §9. Responsive & accessibility

**Responsive** — không tự đặt breakpoint (R-12). Hỏi:
- Thiết bị chính của khách hàng mục tiêu (nếu khách có số liệu Analytics cũ thì ghi nguồn).
- Với từng trang quan trọng: section nào ẩn/thu gọn/đổi thứ tự trên mobile? Menu mobile dạng gì? CTA cố định?
- Bảng dữ liệu/so sánh trên mobile hiển thị thế nào?
- Ghi bảng `Desktop / Tablet / Mobile` trong page spec; ô chưa biết → `TBD (Q-xxx)`.

**Accessibility** — hỏi khách có yêu cầu mức tiêu chuẩn cụ thể không (ví dụ WCAG 2.x mức A/AA — chỉ ghi khi khách xác nhận). Nếu chưa có, ghi các yêu cầu cơ bản dưới nhãn `[BA đề xuất]` để duyệt ở G3: văn bản thay thế cho ảnh, tương phản đủ đọc, điều hướng được bằng bàn phím cho form chính, nhãn rõ cho trường form, không truyền đạt thông tin chỉ bằng màu.

**Usability** — biến mong muốn mơ hồ thành tiêu chí kiểm được, ví dụ "dễ đặt lịch" → "Từ trang chi tiết dịch vụ, người dùng hoàn tất đặt lịch trong tối đa `TBD` bước" — số bước do khách/BA quyết.
