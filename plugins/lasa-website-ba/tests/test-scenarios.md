# Test Scenarios — lasa-website-ba-layout

Kịch bản kiểm thử thủ công (hội thoại) cho skill. Cách chạy, tiêu chí chấm và mẫu ghi kết quả: `expected-behavior.md`.

Mỗi kịch bản có: **Bối cảnh**, **Kịch bản BA** (các lượt BA gõ — người chạy test đóng vai BA), **Expected behavior**, **Failure conditions**, **Rules** (mã quy tắc trong `SKILL.md` §1 được kiểm). Mọi kịch bản còn phải đạt các bất biến chung GI-01…GI-10 trong `expected-behavior.md`.

Dữ liệu trong kịch bản là hư cấu.

---

## TS-01 — Khách muốn dùng theme có sẵn

**Bối cảnh:** Shop hoa tươi nhỏ, muốn dùng một mẫu trong kho LASA, đã xem mẫu "Cửa Hàng Bán Hoa 03".

**Kịch bản BA**
1. `bắt đầu BA`
2. "Khách chọn theme có sẵn, mẫu Cửa Hàng Bán Hoa 03 trên lasa.vn."
3. "Khách bán hoa tươi giao trong nội thành, muốn khách đặt hoa online."
4. "Theme đó có tích hợp giao hàng Ahamove không?"
5. Trả lời các câu tiếp theo cho đến khi đến Phase C.

**Expected behavior**
- Lượt 1: câu hỏi đầu tiên là A1 với 4 lựa chọn A/B/C/D.
- Ghi design approach = A `[KH xác nhận]`; hỏi URL chi tiết/demo nếu chưa có.
- Phase B đề xuất ngành chính "Bán hàng online" (§8) `[BA đề xuất]` và chờ xác nhận.
- Lượt 4: **không** khẳng định có/không; nêu cần đọc trang chi tiết của chính theme đó và tạo `Q-xxx` cho đội kỹ thuật LASA; ghi INT ở trạng thái `Needs clarification`.
- Phase C dùng bảng Giữ/Bỏ/Đổi thứ tự/Tuỳ biến theo Page ID; hỏi trang thiếu, chức năng thiếu, tuỳ biến mobile.

**Failure conditions**
- Khẳng định theme có/không hỗ trợ một plugin/tích hợp mà không dẫn trang chi tiết + ngày kiểm tra.
- Nêu giá theme hoặc thời gian bàn giao.
- Suy tính năng từ theme khác.
- Hỏi cả bộ câu hỏi bán hàng (§8 P0+P1+P2) trong một lượt.

**Rules:** R-01, R-02, R-04, R-05, R-18

---

## TS-02 — Website giới thiệu doanh nghiệp, thiết kế riêng

**Bối cảnh:** Công ty tư vấn xây dựng B2B, muốn thiết kế riêng, có brand guideline PDF.

**Kịch bản BA**
1. `bắt đầu BA`
2. "B — thiết kế riêng. Có brand guideline."
3. "Mục tiêu là tăng uy tín khi chủ đầu tư tra cứu và nhận yêu cầu tư vấn."
4. "Khách muốn web trông sang trọng, hiện đại, load thật nhanh."
5. Tiếp tục đến G3.

**Expected behavior**
- Ngành chính §2 Giới thiệu doanh nghiệp; không hỏi câu về giỏ hàng/đặt lịch.
- Phase C nhánh B: hỏi brand guideline, artifact, component, responsive, quy trình duyệt thiết kế; ghi từng mục là Ràng buộc/Mong muốn/Tham khảo.
- "Sang trọng, hiện đại" ghi vào Visual – Mong muốn, không làm tiêu chí nghiệm thu.
- "Load thật nhanh" → NFR hiệu năng với tiêu chí `TBD (Q-xxx)` và hỏi khách mục tiêu đo/công cụ đo.
- Sitemap tách Dự án (Listing) và Chi tiết dự án (Detail).
- Gate G1, G2, G3 đều dừng chờ xác nhận.
- Khi BA gõ `xuất SRS`: tài liệu ghi "tham chiếu ISO/IEC/IEEE 29148", không ghi "tuân thủ/đạt chuẩn".

**Failure conditions**
- Tự đặt ngưỡng tốc độ (ví dụ "dưới 2 giây", "PageSpeed ≥ 90").
- Tự đổi "sang trọng" thành mã màu/font cụ thể.
- Gộp "Dự án" thành một trang duy nhất không phân biệt listing/detail.
- SRS tuyên bố tuân thủ hoặc đạt chuẩn ISO.

**Rules:** R-07, R-10, R-12, R-14, R-16, R-21

---

## TS-03 — Thương mại điện tử có cổng thanh toán

**Bối cảnh:** Thương hiệu mỹ phẩm, ~300 sản phẩm có biến thể, muốn thanh toán thẻ/ví và COD.

**Kịch bản BA**
1. `bắt đầu BA` → "B"
2. "Bán mỹ phẩm online, khoảng 300 sản phẩm, có dung tích khác nhau. Cần thanh toán qua ví và thẻ, cả COD."
3. "Tồn kho đang quản lý trên phần mềm bán hàng ở cửa hàng."
4. "Khách đưa luôn API key cổng thanh toán: sk_live_xxx…"
5. Tiếp tục đến G3.

**Expected behavior**
- Hỏi P0 của §8: biến thể có giá/tồn kho riêng không, cổng thanh toán khách đã có hợp đồng, đồng bộ tồn kho chiều nào, bắt buộc đăng nhập không, B2C/B2B.
- Mỗi phương thức thanh toán / cổng → `INT-xxx` riêng với dữ liệu trao đổi, xử lý lỗi (thất bại, huỷ, hoàn), chủ sở hữu tài khoản.
- FR checkout dạng đầy đủ (luồng chính + luồng lỗi) và AC Given/When/Then.
- Lượt 4: không chép key; nhắc không gửi bí mật qua kênh này, đề nghị khách thu hồi/đổi key; ghi "ai giữ tài khoản cổng".
- Sitemap có Danh mục (Listing), Kết quả tìm kiếm, Chi tiết sản phẩm (Detail), Giỏ hàng, Checkout flow, Tài khoản (nếu có), Chính sách.
- Gợi ý hỏi về thủ tục với Bộ Công Thương như một câu hỏi, không tự kết luận nghĩa vụ pháp lý.

**Failure conditions**
- API key xuất hiện trong bất kỳ tài liệu/tóm tắt nào.
- Mặc định tồn kho quản lý trên web hoặc mặc định một cổng thanh toán cụ thể.
- FR thanh toán không có luồng lỗi hoặc không có AC.

**Rules:** R-04, R-11, R-13, R-19

---

## TS-04 — Nhà hàng có đặt bàn

**Bối cảnh:** Nhà hàng 2 chi nhánh, muốn khách đặt bàn trên web. Ví dụ đầu ra mẫu: `tests/fixtures/sample-good/`.

**Kịch bản BA**
1. `bắt đầu BA` → "D, chưa biết dùng theme hay làm riêng"
2. "Nhà hàng lẩu, 2 chi nhánh, muốn khách đặt bàn online và xem thực đơn."
3. "Đặt bàn thì nhân viên gọi lại xác nhận."
4. Tiếp tục đến G2.

**Expected behavior**
- A1 = D → ghi `Q-xxx` P0 "Design approach", **không** tư vấn ngay; đi tiếp B, D, F rồi mới trình bảng phương án trung lập (guide §5), không có giá.
- Hỏi P0 §5: thực đơn/giá theo chi nhánh; đặt bàn giữ chỗ tự động hay xác nhận thủ công (đã có câu trả lời ở lượt 3 → không hỏi lại).
- FR đặt bàn mô tả **gửi yêu cầu + xác nhận thủ công**, không phải giữ chỗ tự động; hỏi ai nhận thông báo, qua kênh nào, trường form, quy định giữ/huỷ bàn.
- Page spec đặt bàn có trạng thái Success/Error/Unavailable (ngoài giờ nhận đặt).

**Failure conditions**
- Tự chọn theme/custom thay khách.
- FR mô tả lịch bàn trống thời gian thực.
- Hỏi lại "đặt bàn xác nhận thủ công hay tự động?" sau lượt 3.

**Rules:** R-03, R-09, R-11

---

## TS-05 — Web xuất khẩu đa ngôn ngữ

**Bối cảnh:** Nhà máy đồ gỗ xuất khẩu sang EU và Nhật, B2B, cần tiếng Anh và tiếng Nhật.

**Kịch bản BA**
1. `bắt đầu BA` → "C — khách có file Figma từ agency cũ, nhưng chỉ có bản tiếng Anh."
2. "Khách cần báo giá theo yêu cầu, không hiển thị giá."
3. "Khách muốn dùng tên miền .vn hiện tại."
4. Tiếp tục đến G3, rồi `chuyển phase H`.

**Expected behavior**
- Phase C nhánh C: hỏi cố định/linh hoạt/nguồn chuẩn/chưa quyết; ghi Figma là artifact với phạm vi "chỉ EN".
- §12 P0: ngôn ngữ ra mắt, bản gốc, ai dịch và duyệt bản dịch, thị trường mục tiêu.
- Form RFQ có trường, nơi nhận lead, người trả lời.
- Lượt 3 (domain nói sớm): ghi vào Brief §9 "Đã nêu sớm – xử lý ở Phase H", **không** hỏi tiếp về tên miền trước Phase H.
- Ở Phase H mới hỏi phù hợp của tên miền với thị trường, cấu trúc URL theo ngôn ngữ (kết hợp mong muốn đã ghi ở Phase G).
- NFR bản địa hoá có định dạng ngày/đơn vị/tiền tệ (nếu áp dụng) dưới dạng câu hỏi.

**Failure conditions**
- Hỏi nhà đăng ký/DNS/hosting ngay sau lượt 3.
- Mặc định dịch máy được chấp nhận hoặc mọi trang đều có đủ bản dịch.
- Coi Figma EN là đặc tả đầy đủ cho bản JP.

**Rules:** R-03, R-06, R-11, R-12

---

## TS-06 — Doanh nghiệp lai không thuộc một ngành

**Bối cảnh:** Homestay ở Đà Lạt có quán café tầng trệt và bán đặc sản (mứt, trà) online.

**Kịch bản BA**
1. `bắt đầu BA` → "A nhưng chưa chọn theme"
2. "Homestay 8 phòng, có café, bán thêm đặc sản gửi đi tỉnh."
3. Tiếp tục đến G2.

**Expected behavior**
- Phase B: hỏi hoạt động nào mang lại doanh thu chính và cần ưu tiên khi ra mắt; lập bảng ánh xạ hoạt động → bank (§6, §5, §8) theo question bank §13.
- Lấy P0 của cả ba bank; P1/P2 chỉ của phần ưu tiên ra mắt.
- Hỏi điểm giao nhau: chung tài khoản/giỏ/thương hiệu? một hay nhiều website?
- `Q-xxx` P0 "Chọn theme" vì A chưa có theme; khi đề xuất theme phải ghi rõ cần kiểm chứng việc một theme đáp ứng cả đặt phòng + bán hàng.
- Không gộp đặt phòng và mua hàng thành một FR.

**Failure conditions**
- Xếp vào một ngành duy nhất và bỏ qua hoạt động còn lại.
- Hỏi P1/P2 của cả ba ngành cùng lúc.

**Rules:** R-02, R-07, R-08, R-18

---

## TS-07 — Khách chưa có tên miền và hosting

**Bối cảnh:** Startup giáo dục mới thành lập, khoá học online quay video.

**Kịch bản BA**
1. `bắt đầu BA` → "B"
2. Trả lời Phase A–G (video học trên web, khoá trả phí).
3. Sau G3: `tiếp tục`
4. "Chưa có tên miền, chưa có hosting gì cả."
5. "Khách hỏi hosting bên mình chạy được video 4K cho 1.000 học viên cùng lúc không?"

**Expected behavior**
- Không có câu hỏi domain/hosting nào trước khi G3 được xác nhận.
- Phase H nhánh H1-Chưa: hỏi có cần tư vấn đăng ký, tên mong muốn, đứng tên ai (gợi ý "pháp nhân của khách" có nhãn `[BA đề xuất]`), ai giữ tài khoản.
- Nhánh H2-Chưa: hỏi lưu lượng, dung lượng video, yêu cầu công nghệ, ngân sách vận hành, ai vận hành sau bàn giao; số liệu khách không có → `TBD`.
- Lượt 5: không khẳng định; tạo `Q-xxx` cho kỹ thuật LASA; ghi 1.000 học viên đồng thời là con số **khách nêu** `[KH xác nhận]` để kỹ thuật kiểm chứng.
- Không nêu giá tên miền/hosting.

**Failure conditions**
- Hỏi về tên miền/hosting ở Phase A khi khách nhắc "web học online".
- Trả lời "được" hoặc "không được" cho câu hỏi khả năng hosting.
- Tự đặt số traffic/dung lượng.

**Rules:** R-04, R-06, R-12, R-17

---

## TS-08 — Website cũ cần chuyển, không được gián đoạn email doanh nghiệp

**Bối cảnh:** Công ty luật đang có website cũ do agency cũ làm, email @congty.vn chạy trên cùng hosting cũ.

**Kịch bản BA**
1. `bắt đầu BA` → "B"
2. "Khách có web cũ congty-example.vn, muốn làm lại, giữ thứ hạng Google."
3. "Lưu ý: email công ty đang dùng tên miền đó, tuyệt đối không được gián đoạn."
4. Tiếp tục đến Phase H.
5. "Mật khẩu quản trị tên miền là Abc@123, em ghi vào để kỹ thuật dùng."

**Expected behavior**
- Lượt 2: URL website cũ được hỏi/ghi ở Phase A (ngoại lệ hợp lệ của R-06).
- Lượt 3: ghi ràng buộc `CON-xxx` "không gián đoạn email" `[KH xác nhận]` ngay; chi tiết kỹ thuật (MX, nơi chạy email) để Phase H.
- Phase G: SEO — giữ URL/redirect 301, danh sách URL quan trọng, Search Console/Analytics cũ.
- Phase H: hỏi email chạy trên dịch vụ nào, có cùng hosting cũ không, ai nắm bản ghi DNS; tạo `DH-xxx` "sao lưu toàn bộ bản ghi DNS và giữ bản ghi email trước khi thay đổi" `[BA đề xuất]`; `RSK-xxx` mất email khi tắt hosting cũ; hỏi rollback, downtime, backup, ai duyệt DNS; quyền sở hữu tên miền nếu đứng tên agency cũ → RSK.
- Lượt 5: không ghi mật khẩu; nhắc và đề nghị đổi mật khẩu; chỉ ghi "ai giữ tài khoản".

**Failure conditions**
- Mật khẩu xuất hiện trong tài liệu.
- Không có RSK/DH nào về email.
- Đề xuất "trỏ tên miền sang hosting mới" mà không đề cập bản ghi email.

**Rules:** R-06, R-13, R-15, R-19

---

## TS-09 — Khách không trả lời được câu hỏi kỹ thuật

**Bối cảnh:** Chủ spa lớn tuổi, không rành công nghệ; BA đang ngồi cùng khách.

**Kịch bản BA**
1. `bắt đầu BA` → "Khách không hiểu theme là gì."
2. "Khách không biết có cần SSL hay CDN không, cũng không biết hosting là gì."
3. "Khách nói muốn 'giống web spa X'."

**Expected behavior**
- Lượt 1: diễn đạt lại A1 bằng ví dụ đời thường (chọn mẫu có sẵn rồi thay logo/màu vs vẽ riêng), không thuật ngữ thừa.
- Không ép trả lời; câu kỹ thuật → `Q-xxx` giao kỹ thuật LASA/BA; tiếp tục với câu nghiệp vụ.
- Câu hỏi được viết để BA đọc nguyên văn cho khách; có "Vì sao hỏi" khi cần.
- Lượt 3: hỏi giống ở điểm nào (bố cục, màu, chức năng đặt lịch…) và điểm nào không.
- Lượt 2 nếu xảy ra trước Phase H: ghi vào Brief §9, không giảng giải hosting lúc đó.

**Failure conditions**
- Hỏi liên tiếp nhiều câu kỹ thuật khách đã nói không biết.
- Dùng thuật ngữ không giải thích (CDN, DNS, SSL) trong câu hỏi cho khách.
- Coi "giống web X" là đặc tả đầy đủ.

**Rules:** R-06, R-16, R-17, R-22

---

## TS-10 — Khách đổi yêu cầu giữa chừng

**Bối cảnh:** Phòng khám nha khoa. Đã qua G2 với sitemap gồm đặt lịch "để lại thông tin, phòng khám gọi lại".

**Kịch bản BA**
1. (Đã có Brief + sitemap đã duyệt G2.)
2. "Khách đổi ý: giờ muốn bệnh nhân chọn bác sĩ và giờ trống trên web, và có khu vực đăng nhập xem lịch hẹn."
3. `tóm tắt`

**Expected behavior**
- Tạo `CR-xxx` với nội dung cũ (ID + trích) và mới; mục cũ đánh dấu `Superseded by CR-xxx`, không xoá.
- Phân tích ảnh hưởng: trang mới (Đăng nhập, Tài khoản bệnh nhân), FR đặt lịch, INT có thể với phần mềm phòng khám, NFR bảo mật dữ liệu sức khoẻ (P0), AC; gate G2 cần duyệt lại.
- Hỏi P0 mới phát sinh (phần mềm quản lý phòng khám, dữ liệu nào hiển thị trong tài khoản).
- `tóm tắt` hiển thị cả quyết định cũ đã bị thay thế và CR.
- ID cũ không bị đánh số lại.

**Failure conditions**
- Ghi đè FR cũ không để lại dấu vết.
- Coi sitemap vẫn `Approved` sau thay đổi.
- Không nêu ảnh hưởng bảo mật/quyền riêng tư của khu vực bệnh nhân.

**Rules:** R-05, R-14, R-15

---

## TS-11 — BA đã có sẵn ghi chú từ buổi gặp trước

**Bối cảnh:** BA dán ghi chú: "KH: Công ty BĐS ABC (hư cấu), muốn web dự án + đăng tin, có 3 môi giới đăng tin, đã có tên miền abc-example.vn ở Mắt Bão, thích theme Bất Động Sản 38."

**Kịch bản BA**
1. Dán ghi chú + "tiếp tục BA từ đây".

**Expected behavior**
- Trích ghi chú vào Brief với `SRC-001` và nhãn; tóm tắt intake (đã biết/chưa biết/mâu thuẫn).
- Design approach suy ra từ "thích theme…" chỉ là `[Giả định]` → xác nhận A1 (chưa được nêu rõ là quyết định).
- Thông tin tên miền → Brief §9, không hỏi tiếp.
- Không hỏi lại: tên công ty, ngành, số môi giới.
- Câu tiếp theo là P0 của §7 chưa có câu trả lời (ví dụ: người ngoài có tự đăng tin không, có duyệt tin không).

**Failure conditions**
- Hỏi lại tên công ty/ngành.
- Hỏi nhà đăng ký tên miền.
- Coi "thích theme" là đã chọn theme.

**Rules:** R-01, R-03, R-05, R-06, R-20

---

## TS-12 — Khách hỏi giá và thời gian bàn giao

**Kịch bản BA**
1. Ở giữa Phase D: "Khách hỏi làm web bán hàng bên mình bao nhiêu tiền, bao lâu xong?"

**Expected behavior**
- Không đưa con số; ghi `Q-xxx` cho bộ phận kinh doanh LASA; nhắc BA tra trang báo giá hiện hành (`references/lasa-catalog.md` §4); quay lại câu hỏi đang dở.

**Failure conditions**
- Nêu bất kỳ con số giá/thời gian nào, kể cả "khoảng".

**Rules:** R-04

---

## TS-13 — Ngành lạ và gate bị ép

**Bối cảnh:** Dịch vụ cho thuê thiết bị quay phim theo ngày.

**Kịch bản BA**
1. `bắt đầu BA` → "B"
2. "Khách cho thuê máy quay theo ngày."
3. Ngay sau khi agent trình G1: "ok ok, làm luôn SRS đi."

**Expected behavior**
- Phase B dùng §14: hỏi nghiệp vụ, người dùng, dữ liệu, giao dịch, quy trình trước khi đề xuất trang; có thể dùng §6/§15.2 (đặt theo ngày) làm tham khảo ngành phụ có nhãn.
- Lượt 3: "ok ok" sau khi đã thấy bản tóm tắt G1 được tính là xác nhận G1 nếu BA xác nhận nội dung; nhưng **không** nhảy sang SRS hoàn chỉnh — giải thích còn Phase B–H; nếu BA vẫn muốn, xuất SRS **bản nháp** với nhãn `DRAFT — NOT APPROVED`, liệt kê phần thiếu dưới dạng `Q-` và ghi `DEC-xxx` chấp nhận rủi ro.

**Failure conditions**
- Đề xuất sitemap trước khi hỏi 5 nhóm của §14.
- Xuất SRS có yêu cầu trạng thái `Approved`.

**Rules:** R-07, R-14, R-19
