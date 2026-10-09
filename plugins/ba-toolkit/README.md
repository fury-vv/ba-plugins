# BA Toolkit — plugin hỗ trợ Business Analyst

Phiên bản: **1.0.0**. Gồm skill `srs-analysis`: dẫn BA từ brief, ghi chú họp hoặc yêu cầu thay đổi đến một SRS Markdown có thể review, kiểm thử, truy vết và phê duyệt.

- Domain-neutral: không mặc định lĩnh vực, thực thể, quy trình hay quy định nào.
- Phân biệt rõ điều đã xác nhận, đề xuất, giả định và câu hỏi mở; mọi thông tin có nguồn.
- Cổng phê duyệt của con người: G0, G1, G2 (xác nhận rõ ràng), G5 (`APPROVE SRS vX.Y`).
- Sơ đồ phân tích bằng Mermaid; validator kiểm tra cấu trúc bằng Python thuần.

Kế hoạch và quyết định thiết kế: `docs/implementation-spec.md`.

## Mục lục

1. Cấu trúc
2. Yêu cầu
3. Cài đặt
4. Cách dùng
5. Validator
6. Kiểm thử
7. Giới hạn
8. Điều kiện trước khi dùng với dữ liệu thật

## 1. Cấu trúc

```text
ba-toolkit/
├── .claude-plugin/plugin.json      # manifest plugin
├── skills/srs-analysis/
│   ├── SKILL.md                    # quy trình, gate, nguyên tắc
│   ├── references/                 # nạp theo phase
│   └── scripts/validate_srs.py     # validator
├── domain-packs/README.md          # định dạng domain pack (v1 chưa có pack)
├── examples/                       # brief và trích đoạn SRS giả lập
├── tests/                          # ca kiểm thử, unit test, công cụ quét
└── docs/implementation-spec.md
```

## 2. Yêu cầu

- Claude Code, hoặc claude.ai có bật code execution (xem mục 3).
- Python 3 để chạy validator. Unit test đã chạy thành công trên Python 3.9.25 và 3.13.16 (Linux). Các phiên bản và hệ điều hành khác chưa được kiểm chứng.

## 3. Cài đặt

### 3.0 Claude Code — cài từ marketplace nội bộ (khuyến nghị)

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install ba-toolkit@ba-plugins
```

Hoặc trong một phiên Claude Code (v2.1.275 trở lên), một bước:

```text
/plugin install ba-toolkit --marketplace <owner>/<repo>
```

Cập nhật, gỡ cài đặt, bật cho cả dự án: xem `README.md` ở gốc repo marketplace.

### 3.1 Claude Code — thử nhanh cả plugin

```bash
claude --plugin-dir ./ba-toolkit
```

Skill được gọi là `/ba-toolkit:srs-analysis`. Kiểm tra manifest: `claude plugin validate ./ba-toolkit`.

### 3.2 Claude Code — cài riêng skill

Cho một dự án (commit để cả nhóm dùng):

```bash
# macOS / Linux
mkdir -p .claude/skills
cp -R ba-toolkit/skills/srs-analysis .claude/skills/
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force .claude\skills | Out-Null
Copy-Item -Recurse ba-toolkit\skills\srs-analysis .claude\skills\
```

Cho mọi dự án trên máy (không áp dụng cho cloud session): copy vào `~/.claude/skills/srs-analysis` (Windows: `%USERPROFILE%\.claude\skills\srs-analysis`).

Kiểm tra: gõ `/skills` hoặc `/` và tìm `srs-analysis`.

### 3.3 claude.ai

- **Cá nhân:** nén thư mục `skills/srs-analysis` thành zip (gói kèm: `srs-analysis-skill.zip`), vào **Customize > Skills**, chọn **+**, **Create skill**, **Upload a skill**. Cần bật code execution: gói Free/Pro/Max trong **Settings > Capabilities**; gói Team/Enterprise do owner bật.
- **Tổ chức (Team/Enterprise):** owner thêm plugin tại **Organization settings > Plugins & skills** (upload file zip của plugin, hoặc đồng bộ từ GitHub/GitLab), rồi đặt mức phân phối cho thành viên.
- Gợi ý: mỗi khách hàng một Project; đặt memory của Project ở chế độ tách riêng để thông tin khách này không xuất hiện ở chat khác.

## 4. Cách dùng

Gọi skill rồi đưa đầu vào:

```text
/srs-analysis Phân tích yêu cầu từ brief đính kèm.
/srs-analysis Đây là ghi chú buổi họp hôm nay, cập nhật vào SRS.
/srs-analysis Rà soát docs/srs/srs.md trước khi trình duyệt.
/srs-analysis Khách muốn thêm chức năng X vào SRS đã duyệt.
```

(Cài dạng plugin thì dùng `/ba-toolkit:srs-analysis`.) Skill cũng có thể tự kích hoạt khi yêu cầu khớp mô tả.

Luồng làm việc:

| Phase | Việc chính | Kết thúc bằng |
|---|---|---|
| 0 Intake | Phạm vi, stakeholder, người duyệt, nơi lưu SRS | G0 |
| 1 Discovery | Hỏi theo lượt 3–7 câu, P0 trước; coverage | G1 |
| 2 Domain & workflow | Glossary, quyền, use case, trạng thái, sơ đồ | G2 |
| 3 Soạn SRS | 30 section theo template | — |
| 4 Self-review | Checklist + validator | — |
| 5 Phê duyệt | `APPROVE SRS vX.Y` / `REQUEST CHANGES: …` / `HOLD` | G5 |
| 6 Change control | CR, đánh giá tác động, version mới | Quyết định từng CR |

SRS mặc định lưu ở `docs/srs/srs.md`; khi duyệt có thêm bản chụp `docs/srs/srs-vX.Y.md`.

## 5. Validator

```bash
# macOS / Linux
python3 skills/srs-analysis/scripts/validate_srs.py docs/srs/srs.md
python3 skills/srs-analysis/scripts/validate_srs.py --partial examples/sample-srs-excerpt.md
python3 skills/srs-analysis/scripts/validate_srs.py --help
```

```powershell
# Windows
py skills\srs-analysis\scripts\validate_srs.py docs\srs\srs.md
py skills\srs-analysis\scripts\validate_srs.py --ascii docs\srs\srs.md   # console không hiển thị được tiếng Việt
```

| Exit code | Ý nghĩa |
|---|---|
| 0 | Không có ERROR (có thể có WARNING) |
| 1 | Có ít nhất một ERROR |
| 2 | Lỗi sử dụng hoặc không đọc được file |

Mỗi dòng kết quả có dạng `LEVEL CODE Lnn: message` (`L0` là cấp toàn file). Ý nghĩa từng mã nằm trong `skills/srs-analysis/references/quality-checklist.md`. Validator chỉ đọc file, không sửa; nó chỉ kiểm tra cấu trúc và lỗi cơ học, **không** chứng minh nội dung nghiệp vụ đúng.

## 6. Kiểm thử

```bash
python3 -m unittest discover -s tests -v      # 68 unit test cho validator
python3 tests/scan_domain_terms.py            # quét thuật ngữ đặc thù lĩnh vực trong core skill
```

Ca kiểm thử hành vi (26 ca): `tests/srs-test-cases.md`. Chạy trong một phiên Claude Code mới, ở thư mục chỉ có skill và đầu vào; không để `tests/` (có đáp án) trong tầm đọc.

## 7. Giới hạn

- Validator không kiểm tra cú pháp Mermaid và không render sơ đồ.
- Validator không phát hiện được requirement mơ hồ, trùng nghĩa hay sai nghiệp vụ; phần đó thuộc các mục `[MANUAL]` của quality checklist và review của con người.
- Không kiểm tra được việc tái sử dụng ID qua các version khác nhau.
- Một SRS là một file; SRS rất lớn có thể vượt giới hạn ngữ cảnh.
- Skill không tuyên bố SRS tuân thủ hay được chứng nhận theo chuẩn nào, và không xác minh nội dung pháp lý.
- Ca kiểm thử hành vi chưa được chạy; kết quả phụ thuộc model và cần chạy lặp lại.
- `plugin.json` chưa có `license`; điền theo chính sách của tổ chức trước khi phân phối rộng.

## 8. Điều kiện trước khi dùng với dữ liệu thật

- Xác nhận chính sách công ty và điều khoản bảo mật trong hợp đồng với khách hàng cho phép đưa dữ liệu của khách vào công cụ AI.
- Ẩn danh dữ liệu cá nhân trước khi đưa vào.
- Không dùng thông tin của khách hàng này cho khách hàng khác; tri thức dùng chung chỉ đi qua domain pack đã khái quát, ẩn danh và được duyệt.
