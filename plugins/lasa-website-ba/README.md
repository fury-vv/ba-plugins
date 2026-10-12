# LASA Website BA — plugin hỗ trợ BA làm website

Phiên bản: **1.0.0**. Gồm skill `lasa-website-ba-layout`: hỗ trợ Business Analyst phỏng vấn khách hàng muốn làm website (theme có sẵn của LASA hoặc thiết kế riêng), phân tích – xác thực – tài liệu hoá yêu cầu và bàn giao cho Layout/UI designer, developer, tester, PM.

- Hỏi từng câu, viết để BA đọc nguyên văn cho khách không rành kỹ thuật; chấp nhận "chưa biết".
- Thích ứng theo ngành; không ép doanh nghiệp lai vào một ngành.
- Phân biệt `[KH xác nhận]` / `[Nguồn LASA – ngày]` / `[BA đề xuất]` / `[Giả định]` / `[Câu hỏi mở]` / `[Đã duyệt]`.
- Không báo giá, không cam kết tính năng theme/thời hạn/khả năng hosting, không tự đặt chỉ tiêu NFR, không ghi bí mật.
- Cổng phê duyệt G1–G4 là thật: "ok" chung chung không phải là duyệt.

## 1. Cài đặt

```bash
claude plugin marketplace add fury-vv/ba-plugins     # nếu chưa thêm marketplace
claude plugin install lasa-website-ba@ba-plugins
```

Trong phiên Claude Code: `/plugin marketplace add fury-vv/ba-plugins` và `/plugin install lasa-website-ba@ba-plugins`. Kiểm tra: gõ `/` và tìm `lasa-website-ba:lasa-website-ba-layout`.

Yêu cầu: Claude Code; Python 3.8+ nếu muốn chạy lint (chỉ thư viện chuẩn).

## 2. Cách dùng

Nên mở Claude Code ở một thư mục làm việc riêng cho từng khách — tài liệu được ghi vào `docs/lasa-ba/<project-slug>/`.

```text
/lasa-website-ba:lasa-website-ba-layout bắt đầu BA
```

Hoặc nói tự nhiên: "phỏng vấn khách làm website", "lập sitemap và đặc tả layout cho khách LASA". Đã có ghi chú buổi gặp: dán vào và nói "tiếp tục BA từ đây".

Lệnh nhanh trong phiên: `bắt đầu BA`, `tiếp tục`, `tóm tắt`, `đề xuất theme`, `sitemap`, `đặc tả trang PG-xxx`, `bảng câu hỏi`, `thay đổi: …`, `kiểm tra`, `xuất SRS`, `chuyển phase H`.

Khi Claude Code hỏi quyền: cho phép ghi file trong `docs/lasa-ba/`, đọc web `lasa.vn` (để kiểm chứng theme) và chạy `lint_ba_docs.py`.

## 3. Quy trình

| Phase | Nội dung | Gate |
|---|---|---|
| A | Design approach (luôn hỏi đầu tiên) + nghiệp vụ, mục tiêu, người dùng, stakeholder | G1 |
| B | Nhận diện ngành chính/phụ, chọn question bank | |
| C | Theme có sẵn / thiết kế riêng / từ ý tưởng có sẵn / chưa quyết | |
| D | Sitemap & page inventory (listing ≠ detail) | G2 |
| E | Đặc tả trang & layout (Visual tách Behavior, trạng thái màn hình, responsive) | |
| F | FR / NFR (không tự đặt chỉ tiêu) | |
| G | Nội dung, CMS, SEO, analytics, tích hợp | G3 |
| H | Domain & hosting, email, migration (chỉ sau D–G) | |
| I | Xác thực, xếp hạng câu hỏi mở, phê duyệt phạm vi | G4 |

## 4. Đầu ra

`01-discovery-brief.md` · `02-sitemap-page-inventory.md` · `03-page-specs.md` · `04-srs.md` · `05-rtm.md` · `06-decision-log.md`. Ví dụ hoàn chỉnh (dữ liệu hư cấu, nhà hàng có đặt bàn): `tests/fixtures/sample-good/`.

## 5. Cấu trúc

```text
lasa-website-ba/
├── .claude-plugin/plugin.json
├── skills/lasa-website-ba-layout/
│   ├── SKILL.md                     quy trình, 22 quy tắc R-01..R-22, gate, lệnh
│   ├── references/                  question bank ngành, domain/hosting, design & layout, checklist SRS, catalog LASA
│   ├── templates/                   6 template bàn giao
│   └── scripts/lint_ba_docs.py      lint bộ tài liệu đầu ra
└── tests/                           không đi kèm skill khi nạp
    ├── test-scenarios.md            13 kịch bản hội thoại (TS-01..TS-13)
    ├── expected-behavior.md         bất biến chung, cách test thủ công, kết quả lần chạy gần nhất
    ├── fixtures/                    bộ tài liệu mẫu tốt và mẫu lỗi
    ├── check_skill.py               kiểm tra cấu trúc plugin/skill
    └── run_tests.py                 chạy toàn bộ kiểm thử tự động
```

## 6. Kiểm thử

```bash
python plugins/lasa-website-ba/tests/run_tests.py        # từ gốc repo marketplace
claude plugin validate ./plugins/lasa-website-ba
```

Kịch bản hội thoại chạy thủ công — xem `tests/expected-behavior.md` (có kết quả lần chạy 2026-10-12).

## 7. Giới hạn

- Dữ liệu LASA trong `references/lasa-catalog.md` được đọc ngày 2026-10-12 qua công cụ tóm tắt web; phần `[Skill cũ]` chưa đối chiếu lại. Luôn kiểm tra trang nguồn trước khi nói với khách. Skill không lưu giá.
- Lint chỉ kiểm cấu trúc; không xác minh nội dung có đúng lời khách hay không.
- Không đưa dữ liệu thật của khách vào khi chưa xác nhận chính sách công ty và hợp đồng cho phép.

## 8. Bảo trì

- **Dữ liệu LASA thay đổi:** cập nhật `references/lasa-catalog.md`, ghi ngày kiểm tra.
- **Thêm ngành:** thêm section `## §N.` vào `references/industry-question-bank.md` theo cùng khung, cập nhật bảng tra nhanh và dải section trong `tests/check_skill.py`.
- **Thêm quy tắc:** thêm dòng `R-NN` liên tục vào `SKILL.md` §1 và ít nhất một kịch bản có `R-NN` trong dòng **Rules:**.
- **Phát hành:** tăng `version` trong `.claude-plugin/plugin.json`, thêm mục vào `CHANGELOG.md` (`check_skill.py` sẽ báo nếu thiếu), chạy kiểm thử, commit, tag `lasa-website-ba-vX.Y.Z`, push.
