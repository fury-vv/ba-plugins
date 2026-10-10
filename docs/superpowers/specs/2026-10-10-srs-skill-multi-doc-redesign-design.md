# Thiết kế: Tách srs-analysis thành 3 tài liệu (BRD / SRS / Diagrams) — v2.0.0

## 1. Bối cảnh và mục tiêu

Skill `srs-analysis` (plugin `ba-toolkit` v1.0.0) hiện xuất **một file Markdown duy nhất** (`docs/srs/srs.md`) với 30 section cố định (Document Control, Executive Summary, Goals, Scope, Stakeholders, Glossary, Assumptions, Use Cases, FR, BR, DR, IR, UIR, NFR, User Stories, Permissions, Lifecycle, Reports, Security, Migration, Models/Diagrams, Domain-Specific, Risks, Open Questions, Decision Log, Sources, Elicitation Coverage, Traceability, Approval, Change Requests).

Người dùng đã dùng skill này để tạo SRS cho một dự án thực tế (Lunaria) và nhận thấy:
1. Muốn một **chuẩn SRS khác** — chuẩn phổ biến tại các công ty IT Việt Nam, gồm 6 phần: Giới thiệu, Yêu cầu mức độ tổng thể, Yêu cầu chức năng, Yêu cầu phi chức năng, Yêu cầu bảo mật, Yêu cầu khác & Phụ lục.
2. Muốn **tách file đầu ra theo loại tài liệu**: BRD (yêu cầu nghiệp vụ mức cao) riêng, SRS (theo 6 phần chuẩn) riêng, sơ đồ (ERD/Use Case/Workflow/State) riêng — không gộp chung một file như hiện tại.

Mục tiêu của thay đổi: viết lại skill để xuất ra **3 file tách biệt**, giữ nguyên quy trình elicitation theo phase/gate đã có, giữ nguyên quy ước ID và cơ chế validator (nhưng mở rộng để đọc 3 file).

Đây là **breaking change** về cấu trúc đầu ra — không giữ lại bản 30-section cũ. Nâng `ba-toolkit` lên **v2.0.0**.

## 2. Ba file đầu ra

| File (mặc định) | Vai trò | Nội dung chính |
|---|---|---|
| `docs/brd/brd.md` | Business Requirement Document — yêu cầu nghiệp vụ mức cao | Document Control, Giới thiệu, Bối cảnh & vấn đề nghiệp vụ, Mục tiêu & chỉ số thành công (`GOAL-`), Phạm vi, Các bên liên quan, Thuật ngữ nghiệp vụ, Giả định/ràng buộc/phụ thuộc (`ASM-`), Quy trình nghiệp vụ mức cao (tóm tắt, trỏ sang SRS để xem đặc tả), Rủi ro (`RISK-`), Phê duyệt BRD |
| `docs/srs/srs.md` | SRS theo chuẩn 6 phần | 1. Giới thiệu · 2. Yêu cầu mức độ tổng thể (trỏ `diagrams.md`) · 3. Yêu cầu chức năng (tác nhân, danh sách chức năng, use case tổng quan + phân rã, đặc tả use case — `UC-`, `FR-`, `AC-`) · 4. Yêu cầu phi chức năng (`NFR-`, `UIR-`) · 5. Yêu cầu bảo mật (quyền người dùng, ma trận phân quyền) · 6. Yêu cầu khác & Phụ lục (`IR-`, `DR-`, Open Questions `Q-`, Decision Log `DEC-`, Sources `SRC-`, Elicitation Coverage, Traceability Matrix, Change Requests `CR-`, Approval Record) |
| `docs/diagrams/diagrams.md` | Toàn bộ sơ đồ Mermaid | Context diagram, ERD (từ `DR-`), Use Case Diagram, Workflow/Process Diagram, State Transition Diagram — mỗi sơ đồ một khối `DIA-xxx` |

Ba file dùng **chung một không gian ID** (không trùng ID giữa các file); BRD và SRS có thể tham chiếu chéo ID của nhau và của `diagrams.md` (ví dụ SRS §2 tham chiếu `DIA-001`; BRD §9 tham chiếu `UC-001` đã đặc tả đầy đủ trong SRS).

Vị trí lưu mặc định hỏi ở G0 như hiện tại, mặc định `docs/brd/brd.md`, `docs/srs/srs.md`, `docs/diagrams/diagrams.md` trong thư mục dự án.

## 3. Quy trình elicitation — giữ nguyên, chỉ đổi điểm xuất file

Toàn bộ Phase 0–6, Gate G0–G5, cách hỏi theo lượt P0/P1/P2, các sổ đăng ký (`Q-`, `ASM-`, `DEC-`, `SRC-`, `RISK-`) **giữ nguyên như hiện tại**. Không thêm gate riêng cho BRD — BRD và SRS cùng đi qua một luồng gate, chỉ khác nhau ở **file nào nhận nội dung nào**:

- **Phase 0 (Intake):** tạo cả 3 file khung cùng lúc từ 3 template (`brd-template.md`, `srs-template.md` mới, `diagrams-template.md`), thay vì 1 file khung 30-section.
- **Phase 1 (Discovery):** không đổi — câu hỏi vẫn ghi vào Open Questions (nay nằm ở SRS §6.4).
- **Phase 2 (Domain & workflow):** mô hình hóa (actor, use case, permission, state) dựng trực tiếp vào đúng section của SRS; sơ đồ dựng vào `diagrams.md`.
- **Phase 3 (Soạn SRS):** nội dung được rải vào đúng file theo bảng mapping ở mục 2, không còn soạn vào một file 30-section.
- **Phase 4 (Self-review):** chạy validator mới (mục 4) trên cả 3 file; checklist thủ công áp dụng tương ứng cho từng file.
- **Phase 5 (Phê duyệt G5):** một lần duyệt áp dụng cho cả 3 file cùng lúc (ví dụ `DUYỆT BRD+SRS v1.0`), không duyệt riêng từng file.
- **Phase 6 (Change control):** CR áp dụng, có thể ảnh hưởng một hoặc nhiều trong 3 file; cập nhật traceability tương ứng.

## 4. ID, quy ước và validator

- Giữ nguyên toàn bộ quy ước ID hiện có (`GOAL-`, `ASM-`, `RISK-`, `FR-`, `BR-`, `DR-`, `IR-`, `UIR-`, `NFR-`, `UC-`, `AC-`, `DIA-`, `Q-`, `DEC-`, `SRC-`, `CR-`, `UXP-`) và cách định nghĩa/tham chiếu ID (heading H3 bắt đầu bằng ID, hoặc ô đầu bảng, hoặc dòng AC trong khối cha) — áp dụng xuyên suốt cả 3 file, không theo riêng từng file.
- **Validator mới**: `scripts/validate_docs.py` thay cho `validate_srs.py`.
  - Nhận 3 argument đường dẫn: `--brd`, `--srs`, `--diagrams` (có thể cho phép thiếu 1–2 file với cảnh báo, để hỗ trợ rà soát từng phần khi đang viết).
  - Đọc cả 3 file, dựng một bảng ID toàn cục để kiểm tra: ID định nghĩa trùng (kể cả trùng giữa hai file khác nhau), tham chiếu tới ID chưa định nghĩa ở bất kỳ file nào, đúng ngữ pháp ID.
  - Mỗi file được kiểm tra đúng cấu trúc section riêng của nó (BRD theo khung BRD, SRS theo khung 6 phần, diagrams theo khung sơ đồ).
  - Giữ các rule độc lập-file hiện có: `Not applicable` có lý do, không section rỗng, AC nằm trong khối cha, Priority/Status hợp lệ, mỗi `DIA-` có đúng 1 khối mermaid và loại mermaid hợp lệ, `DIA-` kiểu Context luôn có.
  - Exit code và format output giữ như cũ (0/1/2; ERROR/WARNING/INFO).

## 5. Thay đổi file trong plugin

Trong `plugins/ba-toolkit/`:

| File | Thay đổi |
|---|---|
| `.claude-plugin/plugin.json` | `version`: `1.0.0` → `2.0.0`; cập nhật `description` phản ánh 3 file đầu ra |
| `CHANGELOG.md` | Thêm mục `2.0.0` mô tả breaking change |
| `skills/srs-analysis/SKILL.md` | Cập nhật Phase 0 (tạo 3 file), Phase 3 (mapping nội dung → file), mục "Chạy validator" (lệnh `validate_docs.py` với 3 path), mọi chỗ nhắc `docs/srs/srs.md` → 3 đường dẫn mặc định |
| `skills/srs-analysis/references/srs-template.md` | Viết lại hoàn toàn theo khung 6 phần chuẩn cho riêng SRS (bỏ phần BRD-content và diagram-content ra khỏi file này) |
| `skills/srs-analysis/references/brd-template.md` (mới) | Khung BRD theo mục 2 |
| `skills/srs-analysis/references/diagrams-template.md` (mới) | Khung file sơ đồ theo mục 2 |
| `skills/srs-analysis/references/conventions.md` (mới) | Tách phần "Quy ước chung" (ngữ pháp ID, A6 khối requirement, A7 Priority/Status, A12 nhãn chưa xác nhận...) từ `srs-template.md` cũ ra một file dùng chung, được cả 3 template tham chiếu — tránh lặp lại |
| `skills/srs-analysis/references/diagram-standard.md` | Cập nhật tham chiếu: sơ đồ giờ nằm trong `diagrams.md`, không còn trong SRS §21 |
| `skills/srs-analysis/scripts/validate_srs.py` | Xóa, thay bằng `validate_docs.py` |
| `skills/srs-analysis/scripts/validate_docs.py` (mới) | Theo mục 4 |
| `skills/srs-analysis/tests/fixtures/*` | Thay fixture 1-file bằng fixture 3-file (`valid-minimal-brd.md`, `valid-minimal-srs.md`, `valid-minimal-diagrams.md`, cùng vài biến thể lỗi để test validator) |
| `skills/srs-analysis/tests/test_validate_srs.py` | Đổi tên/viết lại thành `test_validate_docs.py`, cập nhật test case cho logic đọc 3 file và kiểm tra ID xuyên file |
| `skills/srs-analysis/examples/sample-srs-excerpt.md` | Cập nhật ví dụ cho khớp cấu trúc 6 phần mới (và có thể thêm `sample-brd-excerpt.md`) |
| `skills/srs-analysis/docs/implementation-spec.md` | Rà soát, cập nhật nếu tài liệu này mô tả cấu trúc cũ |

Các reference khác (`elicitation-guide.md`, `domain-discovery-guide.md`, `product-type-guide.md`, `nfr-checklist.md`, `user-story-standard.md`, `acceptance-criteria-standard.md`, `quality-checklist.md`, `change-control.md`) về nội dung câu hỏi/tiêu chuẩn chất lượng không đổi logic, chỉ cập nhật các chỗ trỏ tới "SRS §xx" cho khớp số section mới hoặc trỏ sang file khác (BRD/diagrams) khi cần.

## 6. Luồng dữ liệu

```
Brief / meeting notes
      │
      ▼
Phase 0 Intake ──► tạo khung: brd.md + srs.md + diagrams.md (từ 3 template)
      │
      ▼
Phase 1 Discovery ──► câu hỏi ghi vào SRS §6.4 (Open Questions)
      │
      ▼
Phase 2 Domain & workflow ──► actor/use case/permission/state → SRS; sơ đồ → diagrams.md
      │
      ▼
Phase 3 Soạn tài liệu ──► rải nội dung theo bảng mapping (mục 2) vào 3 file
      │
      ▼
Phase 4 Self-review ──► validate_docs.py đọc cả 3 file + checklist thủ công
      │
      ▼
Phase 5 Gate G5 ──► một quyết định duyệt áp dụng cho cả 3 file
      │
      ▼
Phase 6 Change control (khi có CR) ──► cập nhật file bị ảnh hưởng + traceability
```

## 7. Xử lý lỗi / trường hợp biên

- **Thiếu một trong 3 file khi chạy validator**: báo WARNING (không phải ERROR) cho file thiếu, vẫn kiểm tra ID nội bộ của các file có mặt; không chặn self-review giữa chừng khi người dùng đang soạn từng file một.
- **Tham chiếu ID xuyên file tới file chưa tồn tại**: ERROR rõ ràng, ghi tên ID và file đang tham chiếu.
- **Dự án cũ đã có `docs/srs/srs.md` theo bản 30-section (v1.0.0)**: skill mới không tự động migrate. Ở Phase 0, nếu phát hiện file cũ theo cấu trúc 30-section, báo cho người dùng và hỏi có muốn BA thủ công tách nội dung sang 3 file mới hay bắt đầu lại từ đầu — không tự xóa hay tự chuyển đổi ngầm.
- **Tên file/đường dẫn khác mặc định**: vẫn hỏi ở G0 như cũ, áp dụng cho cả 3 đường dẫn (có thể đặt tên khác nhau cho từng file).

## 8. Kiểm thử

- Cập nhật `tests/test_validate_docs.py`: test ID trùng trong cùng file, ID trùng giữa hai file khác nhau, tham chiếu ID xuyên file hợp lệ/không hợp lệ, thiếu 1 trong 3 file (WARNING không ERROR), đủ cấu trúc riêng từng loại file, sai ngữ pháp ID, exit code đúng theo 3 mức.
- Cập nhật `tests/scan_domain_terms.py` nếu có áp dụng domain-neutral check lên nội dung 3 file thay vì 1 file.
- Giữ nguyên `tests/brief-answer-key.md`, `tests/srs-test-cases.md` về nội dung câu hỏi, chỉ cập nhật phần mô tả đầu ra mong đợi (giờ là 3 file).
- Sau khi cập nhật, chạy thử toàn bộ eval/test hiện có của plugin (`claude plugin eval` nếu có) để đảm bảo không hồi quy.

## 9. Ngoài phạm vi

- Không viết công cụ tự động migrate SRS cũ (30-section) sang cấu trúc mới.
- Không thêm gate phê duyệt riêng cho BRD.
- Không đổi nội dung câu hỏi elicitation (chỉ đổi nơi lưu kết quả).
