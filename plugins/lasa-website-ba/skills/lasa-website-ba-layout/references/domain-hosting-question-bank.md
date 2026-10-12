# Domain & Hosting Question Bank (Phase H)

**Điều kiện dùng:** chỉ sau khi phạm vi website (Phase D–G) đã được khám phá — thường sau Gate G3 (R-06). Thông tin khách tự nêu sớm đã nằm trong Brief mục "Đã nêu sớm – xử lý ở Phase H": đọc lại trước, không hỏi lại (R-03).

**An toàn (R-13):** không bao giờ hỏi hay ghi mật khẩu, OTP, private key, recovery code, secret API key, mã chuyển tên miền (EPP/auth code). Chỉ hỏi **ai giữ tài khoản** và **ai có quyền phê duyệt thay đổi**. Nếu khách gửi bí mật: nhắc không gửi qua kênh này, không chép vào tài liệu, đề nghị đổi mật khẩu/khoá.

**Không khẳng định khả năng kỹ thuật:** mọi câu "hosting X chạy được Y không" → `Q-xxx` giao đội kỹ thuật LASA kiểm chứng.

ID cho yêu cầu/ràng buộc phase này: `DH-xxx` (domain/hosting/deployment), `RSK-xxx` cho rủi ro, `Q-xxx` cho câu hỏi mở.

---

## §1. Tên miền

**H1.** Anh/chị đã có tên miền cho website chưa?

### H1-Có
Hỏi lần lượt (bỏ mục đã biết):
1. Tên miền là gì? Có nhiều tên miền (ví dụ .vn và .com) không?
2. Đăng ký ở nhà cung cấp nào (nhà đăng ký)? *[Khách không biết → Q-xxx; có thể tra cứu WHOIS công khai — BA làm, không cần khách]*
3. Tên miền đứng tên ai (công ty, cá nhân, agency cũ)? Ai đang giữ tài khoản quản lý? *[Nếu đứng tên cá nhân/agency cũ → RSK: quyền sở hữu]*
4. Ai được quyền **phê duyệt thay đổi DNS** khi website mới lên?
5. Ngày hết hạn (nếu biết)? Có bật tự gia hạn không?
6. Tên miền đang dùng cho gì: website hiện tại, **email doanh nghiệp**, hệ thống khác (CRM, landing page, app, xác minh Google/Facebook)?
7. Có subdomain nào đang dùng (ví dụ shop., mail., app.)? Dùng cho gì?
8. DNS đang quản lý ở đâu (tại nhà đăng ký, tại hosting, hay dịch vụ như Cloudflare)?

**Nếu tên miền đang dùng cho email (phụ thuộc quan trọng):**
- Email đang chạy trên dịch vụ nào (Google Workspace, Microsoft 365, email của hosting, khác)?
- Có ai nắm danh sách bản ghi DNS hiện tại (MX, SPF, DKIM, DMARC, các bản ghi xác minh) không? → ghi `DH-xxx`: *"Trước mọi thay đổi DNS phải xuất/sao lưu toàn bộ bản ghi DNS hiện tại và giữ nguyên các bản ghi email"* `[BA đề xuất]`, chờ duyệt.
- Email có nằm trên **cùng hosting** với website cũ không? *[Nếu có → RSK cao: tắt hosting cũ = mất email. Q-xxx cho kỹ thuật: kế hoạch tách email trước khi chuyển]*
- Có khung thời gian không được gián đoạn email không?

### H1-Chưa
1. Anh/chị có muốn được tư vấn đăng ký tên miền không?
2. Nếu có: tên mong muốn (vài phương án), đuôi mong muốn (.vn, .com.vn, .com, khác), thị trường mục tiêu (liên quan §12 xuất khẩu)?
3. Tên miền đứng tên ai? *[BA đề xuất: đứng tên pháp nhân của khách — `[BA đề xuất]`, khách quyết]*
4. Ai giữ tài khoản quản lý tên miền?
5. Có cần email theo tên miền không? (chỉ ghi nhu cầu; giải pháp email ngoài phạm vi trừ khi khách yêu cầu)

Không nêu giá/khuyến mãi tên miền — `Cần LASA xác nhận` (R-04).

---

## §2. Hosting / server

**H2.** Anh/chị đã có hosting hoặc máy chủ để chạy website chưa?

### H2-Có
1. Nhà cung cấp? Loại dịch vụ (shared hosting, VPS, cloud, máy chủ riêng, nền tảng quản lý)?
2. Đang chạy gì trên đó (website cũ, email, ứng dụng khác)? *[Workload chung → RSK khi nâng cấp/chuyển]*
3. Giới hạn đã biết (dung lượng, băng thông, phiên bản phần mềm)? *[Khách không biết → Q-xxx kỹ thuật]*
4. Tài khoản đứng tên ai, ai giữ quyền quản trị?
5. Có môi trường thử nghiệm (staging) không? Có cần không?
6. Backup: có tự động không, tần suất, lưu ở đâu, đã từng khôi phục thử chưa?
7. SSL (https) đang dùng loại nào, ai gia hạn?
8. Có dùng CDN/tường lửa web không?
9. Hạn chế đặc biệt (chính sách công ty, vị trí lưu dữ liệu, IP cố định, quy định bảo mật nội bộ)?
10. Thời hạn hợp đồng hosting hiện tại?

→ `Q-xxx` cho kỹ thuật LASA: "Hosting hiện tại có đáp ứng giải pháp đề xuất không?" — **không** khẳng định có/không.

### H2-Chưa
1. Lượng truy cập dự kiến (nếu khách có số liệu/ước lượng; không có → `TBD`)?
2. Dung lượng nội dung dự kiến (số sản phẩm, ảnh, video, file tải về)?
3. Có yêu cầu công nghệ bắt buộc (nền tảng, ngôn ngữ, vị trí máy chủ trong nước/nước ngoài)?
4. Khoảng ngân sách vận hành hằng năm (nếu sẵn sàng chia sẻ)?
5. Yêu cầu bảo mật, backup, bảo trì, ai chịu trách nhiệm vận hành sau bàn giao?
6. Muốn tài khoản hosting đứng tên ai?

Không đặt con số traffic/dung lượng thay khách (R-12).

---

## §3. Migration & go-live

Chỉ hỏi khi có website/dữ liệu cũ.

| # | Câu hỏi | Ghi vào |
|---|---|---|
| M1 | Website cũ chạy nền tảng gì (nếu biết)? Ai đang quản lý? | Brief §8 |
| M2 | Có cần **giữ nguyên đường dẫn (URL)** cũ không? Nếu đổi — cần chuyển hướng (301) các trang quan trọng? Ai cung cấp danh sách URL? | SEO-xxx, DH-xxx |
| M3 | Dữ liệu nào phải chuyển (bài viết, sản phẩm, khách hàng, đơn hàng, thành viên, file)? Khoảng bao nhiêu? Định dạng xuất được? | CNT-xxx, DH-xxx |
| M4 | Có dữ liệu cá nhân (khách hàng, thành viên) cần chuyển không? Ai chịu trách nhiệm về dữ liệu đó? | NFR quyền riêng tư |
| M5 | Có khung thời gian **không được gián đoạn** (giờ cao điểm, mùa vụ, chiến dịch)? Chấp nhận downtime tối đa bao lâu (khách quyết, `TBD`)? | DH-xxx |
| M6 | Phải sao lưu toàn bộ website cũ trước khi chuyển? Giữ bản sao bao lâu? | DH-xxx |
| M7 | Nếu website mới gặp sự cố sau khi lên — có cần **phương án quay lại (rollback)** về website cũ không? Ai quyết định rollback? | DH-xxx, RSK |
| M8 | Website cũ có kết nối hệ thống khác (form gửi CRM, tracking, pixel) cần chuyển theo? | INT-xxx, SEO-xxx |
| M9 | Có tài khoản Google Search Console/Analytics cho website cũ không, ai giữ? | SEO-xxx |

**Checklist rủi ro migration** (ghi RSK khi áp dụng): mất email do đổi MX/tắt hosting cũ · mất thứ hạng SEO do không redirect · mất dữ liệu do không backup · DNS lan truyền trong giờ cao điểm · SSL chưa sẵn khi trỏ tên miền · tracking/pixel không được gắn lại · quyền tài khoản tên miền/hosting nằm ở bên thứ ba không liên lạc được.

---

## §4. Khi khách không trả lời được câu kỹ thuật

- Diễn đạt lại: "Mỗi tháng anh/chị trả tiền cho đơn vị nào để website/email chạy?" thay cho "nhà cung cấp hosting là ai?".
- Hỏi người có thể biết: kế toán (hoá đơn gia hạn), IT nội bộ, agency cũ.
- Vẫn không biết → `Q-xxx` với người phụ trách và hạn (nếu BA đặt); không ép khách đoán (R-17).
