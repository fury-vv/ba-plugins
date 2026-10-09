# Implementation Spec — plugin `ba-toolkit` / skill `srs-analysis` v1.0.0

| Field | Value |
|---|---|
| Spec version | 1.0 |
| Status | APPROVED |
| Approval | Người dùng phê duyệt trong hội thoại ngày 2026-10-09 ("ok đã ổn định rồi, lên plan spec và triển khai skill agent nhé"); được hiểu là duyệt Plan v0.4 với toàn bộ khuyến nghị D1–D29 |
| Kế thừa | Plan v0.1 → v0.2 (sơ đồ, độ phủ) → v0.3 (kiến trúc 3 lớp tri thức, plugin) → v0.4 (câu hỏi UI/UX) |
| Prompt gốc | `srs-analysis-generic-claude-code-prompt.md` (Project Knowledge) |

## Mục lục

1. Mục tiêu và phạm vi v1
2. Kiến trúc
3. Cấu trúc gói
4. Quy ước cốt lõi (tóm tắt)
5. Decision log
6. Giá trị mặc định cho thông tin chưa có
7. Các bước thực hiện và tiêu chí nghiệm thu
8. Ngoài phạm vi v1 và lộ trình
9. Câu hỏi còn mở

## 1. Mục tiêu và phạm vi v1

Skill `srs-analysis` hỗ trợ BA đi từ brief, ghi chú họp hoặc yêu cầu thay đổi đến một SRS Markdown có ID ổn định, phân biệt rõ điều đã xác nhận với đề xuất/giả định/câu hỏi mở, có acceptance criteria, sơ đồ phân tích (Mermaid), traceability, kiểm tra cấu trúc bằng validator và cổng phê duyệt của con người. Sau baseline, mọi thay đổi đi qua change control.

Ngoài phạm vi: thiết kế UI, kiến trúc, code, kiểm thử, triển khai; mọi tác động lên hệ thống bên ngoài.

## 2. Kiến trúc

**Ba lớp tri thức** (D24):

| Lớp | Nội dung | Phạm vi | Ai sửa |
|---|---|---|---|
| Core skills | Quy trình, template, chuẩn, validator | Mọi dự án | Người bảo trì, qua change control |
| Domain pack | Tri thức lĩnh vực đã khái quát, ẩn danh, đã duyệt | Dự án cùng lĩnh vực | BA đề xuất, người được chỉ định duyệt |
| Workspace khách hàng | Ghi chú, tài liệu, quyết định, SRS | Một khách hàng | BA phụ trách |

Quy tắc an toàn: (1) domain pack chỉ sinh câu hỏi và giả thuyết, không tự thành requirement đã xác nhận; (2) tri thức chỉ đi một chiều từ workspace lên domain pack qua khái quát hóa, ẩn danh và duyệt; (3) skill chỉ dùng thông tin của workspace hiện tại.

**Bốn lớp của skill**: metadata (frontmatter) → orchestrator (`SKILL.md`) → references (nạp theo phase) → script (`validate_srs.py`).

**Phase và gate**:

| Phase | Đầu ra | Gate |
|---|---|---|
| 0 Intake | Phạm vi đề xuất, stakeholder, người duyệt, nơi lưu SRS | G0 (xác nhận rõ ràng) |
| 1 Discovery | Câu hỏi P0–P2, sổ nguồn/giả định/câu hỏi, bảng coverage | G1 (xác nhận rõ ràng; coverage có trạng thái, không còn P0 mở trừ khi chấp nhận rủi ro) |
| 2 Domain & workflow | Glossary, actor/permission, use case, state, BR, data, interface, sơ đồ | G2 (xác nhận rõ ràng) |
| 3 Soạn SRS | SRS `DRAFT — NOT APPROVED` | — |
| 4 Self-review | Báo cáo checklist + validator | — |
| 5 Approval | Baseline `APPROVED` | G5 (cú pháp cố định) |
| 6 Change control | CR, đánh giá tác động, version mới | Quyết định cho từng CR |

## 3. Cấu trúc gói

```text
ba-toolkit/
├── .claude-plugin/plugin.json
├── README.md
├── CHANGELOG.md
├── docs/implementation-spec.md
├── domain-packs/README.md
├── skills/srs-analysis/
│   ├── SKILL.md
│   ├── references/
│   │   ├── srs-template.md
│   │   ├── elicitation-guide.md
│   │   ├── product-type-guide.md
│   │   ├── domain-discovery-guide.md
│   │   ├── user-story-standard.md
│   │   ├── acceptance-criteria-standard.md
│   │   ├── nfr-checklist.md
│   │   ├── diagram-standard.md
│   │   ├── quality-checklist.md
│   │   └── change-control.md
│   └── scripts/validate_srs.py
├── examples/
│   ├── generic-product-brief.md
│   └── sample-srs-excerpt.md
└── tests/
    ├── srs-test-cases.md
    ├── brief-answer-key.md
    ├── domain-neutral-terms.txt
    ├── scan_domain_terms.py
    ├── test_validate_srs.py
    └── fixtures/
```

## 4. Quy ước cốt lõi (tóm tắt)

Chi tiết và nguồn sự thật: `skills/srs-analysis/references/srs-template.md`.

- SRS có 30 section cố định, heading song ngữ `## <số>. <English title> — <Tiếng Việt>`; validator nhận theo số và tên tiếng Anh.
- Section không áp dụng: `Not applicable — <lý do>`.
- ID: `FR|BR|DR|IR|UIR|NFR-[MÃ-]NNN`, `GOAL|US|UC|DIA|Q|ASM|RISK|DEC|SRC|UXP|CR-NNN`, `AC-<REQ-ID>-NN`. (`GOAL-` được thêm khi triển khai để ma trận truy vết có điểm đầu là mục tiêu.)
- ID chỉ được định nghĩa ở heading H3, ở cột đầu bảng của sổ sở hữu, hoặc ở dòng AC; mọi chỗ khác là tham chiếu.
- Priority requirement: Must/Should/Could/Won't. Priority câu hỏi: P0/P1/P2.
- Status requirement: Proposed, Confirmed, Approved, Deferred, Rejected, Superseded.
- Trạng thái tài liệu: `DRAFT — NOT APPROVED`, `APPROVED`, `ON HOLD`.
- Phê duyệt: `APPROVE SRS vX.Y` / `REQUEST CHANGES: …` / `HOLD` hoặc `DUYỆT SRS vX.Y` / `YÊU CẦU SỬA: …` / `TẠM DỪNG`.
- Version: nháp 0.x; lần duyệt đầu 1.0; mỗi CR được duyệt tăng số phụ.

## 5. Decision log

| ID | Quyết định | Lựa chọn đã duyệt |
|---|---|---|
| D1 | Nơi xây dựng, bàn giao | Chat dựng trong sandbox, giao gói zip |
| D2 | Cấu trúc thư mục | Được thay bằng D23 |
| D3 | Frontmatter | Chỉ `name` + `description` (dùng được cả Claude Code và claude.ai) |
| D4 | Mức chi tiết | Một template, đủ section, `Not applicable` kèm lý do |
| D5 | Ngôn ngữ | Hướng dẫn tiếng Việt + thuật ngữ tiếng Anh; heading song ngữ; đổi ngôn ngữ SRS khi người dùng yêu cầu |
| D6 | Định dạng requirement | Khối heading H3 + danh sách trường cố định |
| D7 | Quy ước ID | Như mục 4 |
| D8 | Priority/status | MoSCoW; bộ status như mục 4 |
| D9 | Gate | G0, G1, G2 xác nhận rõ ràng; G5 phê duyệt chính thức |
| D10 | Duyệt khi còn mở | P0 mở chặn duyệt trừ khi người duyệt chấp nhận rủi ro (ghi DEC); P1/P2/TBD cho phép nếu có trong sổ câu hỏi mở; ERROR của validator phải sửa trước khi trình duyệt |
| D11 | Cú pháp phê duyệt | Như mục 4; version phải khớp |
| D12 | Version SRS | Như mục 4 |
| D13 | Nơi lưu SRS | Hỏi ở G0; mặc định `docs/srs/srs.md` + bản chụp `docs/srs/srs-vX.Y.md` khi duyệt |
| D14 | Phạm vi validator | Bắt buộc theo prompt + tham chiếu treo, traceability, N/A, nhất quán phê duyệt, `--partial`; cú pháp Python 3.9+ |
| D15 | Domain giả lập cho ví dụ | Chọn tạm: web app điều phối ca tình nguyện của một tổ chức hư cấu; ca kiểm thử domain-specific dùng bối cảnh tương phản (sổ bảo trì thiết bị của một xưởng hư cấu). Có thể đổi |
| D16 | Kiểm thử hành vi | Người dùng chạy trong Claude Code; ≥ 2 lần với ca quan trọng; có lượt baseline không dùng skill |
| D17 | Định dạng sơ đồ | Mermaid nhúng trong SRS |
| D18 | Sơ đồ bắt buộc | Context diagram luôn bắt buộc; loại khác theo điều kiện kích hoạt |
| D19 | Tự động hóa sơ đồ | Mức 1 (Claude sinh) + mức 2 (validator kiểm chéo); render và sinh từ bảng để sau |
| D20 | Độ phủ thu thập | Bảng Elicitation Coverage + điều kiện qua G1 |
| D21 | Câu hỏi theo loại sản phẩm | Reference riêng `product-type-guide.md` |
| D22 | Nền tảng của BA | claude.ai (mỗi khách hàng một Project) + Claude Code cho bảo trì |
| D23 | Đóng gói | Plugin `ba-toolkit` |
| D24 | Kiến trúc tri thức | 3 lớp + quy tắc an toàn |
| D25 | Duyệt domain pack | Chưa có thông tin; v1 chỉ định nghĩa định dạng, người duyệt ghi là "người được tổ chức chỉ định" |
| D26 | Phạm vi v1 | `srs-analysis` + thành phần dùng chung (định dạng domain pack, ghi nguồn, nhập ghi chú họp) |
| D27 | Ranh giới SRS–UI/UX | SRS thu thập và phân loại (ràng buộc/mong muốn/tham chiếu) |
| D28 | Kiểm tra tương phản màu | Để sau v1; v1 kiểm định dạng mã màu và nguồn |
| D29 | Style tile | Không có trong v1 |

## 6. Giá trị mặc định cho thông tin chưa có

| Thông tin | Mặc định đang dùng |
|---|---|
| Hệ điều hành của người dùng | README có lệnh cho macOS/Linux và Windows; chỉ kiểm chứng trên Linux sandbox |
| Phiên bản Python | Viết theo cú pháp 3.9+; chỉ cam kết các phiên bản đã thực sự chạy test |
| Model dùng trong Claude Code | Chưa biết; kiểm thử hành vi chạy trên model người dùng dùng thực tế |
| Gói claude.ai, owner | Chưa biết; README mô tả cả cách cá nhân upload và cách owner phân phối |
| Chính sách dữ liệu khách hàng | Chưa xác nhận; README nêu là điều kiện tiên quyết |
| Người duyệt domain pack | "Người được tổ chức chỉ định" |

## 7. Các bước thực hiện và tiêu chí nghiệm thu

| Bước | Nội dung | Tiêu chí nghiệm thu chính |
|---|---|---|
| 1 | Quy ước + khung SRS | Một danh sách section duy nhất; regex cho mọi tiền tố; phân biệt định nghĩa/tham chiếu; không có nội dung ngành |
| 2 | `SKILL.md` | Frontmatter hợp lệ (name ≤ 64 ký tự, description ≤ 1.024 ký tự, ngôi thứ ba, không thẻ XML); < 300 dòng; đủ phase, gate, guardrails, bảng phase→reference, fallback |
| 3 | References | Có mục đích/lúc dùng; file > 100 dòng có mục lục; ví dụ dùng placeholder; không có target định lượng mặc định |
| 4 | Validator + unit test | Chỉ stdlib; `--help`; exit 0/1/2; không ghi file đầu vào; mỗi quy tắc có test dương và âm; test pass |
| 5 | Ví dụ + test case | Brief giả lập cố ý thiếu ≥ 4 nhóm thông tin, đáp án tách riêng; sample chạy `--partial` không có ERROR; ≥ 22 ca kiểm thử |
| 6 | README, manifest | Cài đặt cho Claude Code và claude.ai; lệnh validator; giới hạn; changelog |
| 7 | Tự kiểm, đóng gói | Báo cáo kèm output thật; mục chưa kiểm được ghi rõ lý do |
| 8 | Kiểm chứng trong Claude Code (người dùng) | Skill hiện trong `/skills`; validator chạy trên máy người dùng; kết quả ca hành vi được ghi |
| 9 | Sửa lỗi, duyệt Skill v1.0 | Người dùng duyệt rõ ràng |

## 8. Ngoài phạm vi v1 và lộ trình

- v1.1: script kiểm tra tương phản màu (D28); render Mermaid bằng mermaid-cli (tùy chọn); sinh sơ đồ từ bảng.
- Giai đoạn 2: skill `meeting-prep`, `meeting-capture`.
- Giai đoạn 3: `domain-pack-curator`, domain pack đầu tiên, `ba-status`, xuất Excel/Word/backlog.
- Sau đó: các skill tiếp theo của pipeline (UI/UX, system design).

## 9. Câu hỏi còn mở

| ID | Câu hỏi | Ảnh hưởng |
|---|---|---|
| OQ-1 | Hệ điều hành, phiên bản Python, model Claude Code đang dùng | Bước 8 |
| OQ-2 | Gói claude.ai và owner của tổ chức | Cách phân phối |
| OQ-3 | Chính sách công ty và hợp đồng khách hàng về dữ liệu đưa vào AI | Điều kiện tiên quyết khi dùng thật |
| OQ-4 | Người duyệt domain pack và tiêu chí ẩn danh | Giai đoạn 3 |
| OQ-5 | Công cụ đang dùng để họp, lưu biên bản, quản lý backlog | Connector, script xuất |
| OQ-6 | Domain giả lập cho ví dụ có cần đổi không (D15) | Bước 5 |
