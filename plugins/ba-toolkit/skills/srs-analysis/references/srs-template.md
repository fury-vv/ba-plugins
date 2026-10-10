# SRS Template — Khung Software Requirements Specification (chuẩn 6 phần)

**Mục đích:** khung chuẩn cho `docs/srs/srs.md`, theo chuẩn SRS 6 phần: Giới thiệu, Yêu cầu mức độ tổng thể, Yêu cầu chức năng, Yêu cầu phi chức năng, Yêu cầu bảo mật, Yêu cầu khác & Phụ lục. Quy ước ID, Document Control, requirement block dùng chung với `conventions.md`.

**Khi dùng:** Phase 0 (tạo khung), Phase 3 (soạn), Phase 4 (rà soát), Phase 6 (cập nhật sau CR).

## Danh sách section (bắt buộc đúng số thứ tự)

| # | English title | Tiếng Việt | ID định nghĩa tại đây | N/A |
|---|---|---|---|---|
| 1 | Introduction | Giới thiệu | — | Không |
| 2 | High-Level Requirements | Yêu cầu mức độ tổng thể | — | Không |
| 3 | Functional Requirements | Yêu cầu chức năng | FR, UC, AC | Không |
| 4 | Non-Functional Requirements | Yêu cầu phi chức năng | NFR, UIR, UXP | Không |
| 5 | Security Requirements | Yêu cầu bảo mật | — | Không |
| 6 | Other Requirements and Appendix | Yêu cầu khác và Phụ lục | BR, DR, IR, Q, DEC, SRC, CR | Không |

Không xóa section. Section 4 và 5 **không được** ghi `Not applicable` — mọi hệ thống có ít nhất một thuộc tính chất lượng và một mối quan tâm bảo mật cần ghi nhận (dù chỉ là "chưa có yêu cầu đặc biệt, dùng mức mặc định — TBD").

## Nội dung từng section

- **1. Introduction:** mục tiêu tài liệu SRS, phạm vi kỹ thuật, đối tượng sử dụng (đội phát triển, QA, PM), tài liệu tham chiếu (`docs/brd/brd.md`, `docs/diagrams/diagrams.md`), thuật ngữ/viết tắt kỹ thuật (thuật ngữ nghiệp vụ xem BRD §6).
- **2. High-Level Requirements:** tóm tắt actor và luồng chính; trỏ sang `docs/diagrams/diagrams.md` cho Object/Entity Relationship Diagram, Workflow Diagram, State Transition Diagram, Use Case Diagram (`DIA-xxx`). Không vẽ sơ đồ lại ở đây.
- **3. Functional Requirements:**
  - Danh sách tác nhân (actor) — có thể là bảng tham chiếu Stakeholders ở BRD §5, chỉ nêu actor nào tương tác hệ thống trực tiếp.
  - Danh sách chức năng (tóm tắt theo nhóm nghiệp vụ, mỗi dòng trỏ tới `FR-xxx`).
  - Use case tổng quan và phân rã (danh sách `UC-xxx`, nhóm theo actor hoặc theo luồng).
  - Đặc tả từng use case (khối `UC-` đầy đủ) và từng functional requirement (khối `FR-` đầy đủ, có AC).
- **4. Non-Functional Requirements:** hiệu suất, bảo mật kỹ thuật (mã hóa, xác thực — không gồm ma trận phân quyền, xem §5), giao diện người dùng (khối `NFR-` cho mục tiêu đo được + bảng `UIR-`/`UXP-` cho ràng buộc/mong muốn UI), tính khả dụng. Theo danh mục đầy đủ ở `nfr-checklist.md`.
- **5. Security Requirements:** quyền người dùng theo role/actor, ma trận phân quyền (bảng Permissions — xem `conventions.md` A8), quy tắc kiểm soát truy cập theo dữ liệu (business rule về phạm vi dữ liệu đặt ở §6 dưới dạng `BR-`, tham chiếu từ đây).
- **6. Other Requirements and Appendix:** gợi ý chia theo mục nhỏ (không cần đánh số H2 mới, dùng H3/H4 thường hoặc chỉ là heading mô tả — không ảnh hưởng validator):
  - Tích hợp (`IR-`)
  - Dữ liệu (`DR-`)
  - Business Rules (`BR-`)
  - Workflow chi tiết / vòng đời và chuyển trạng thái (bảng State transitions — xem `conventions.md` A8)
  - Open Questions (`Q-`)
  - Decision Log (`DEC-`)
  - Sources (`SRC-`)
  - Elicitation Coverage
  - Traceability Matrix
  - Change Requests (`CR-`)
  - Approval Record (phê duyệt đồng thời cho BRD + SRS, xem `conventions.md` A11)

## Khung (sao chép để bắt đầu)

~~~~markdown
# Software Requirements Specification — [Tên dự án]

| Field | Value |
|---|---|
| Project | [Tên dự án] |
| Document type | SRS |
| Document version | 0.1 |
| Status | DRAFT — NOT APPROVED |
| Current phase | Phase 0 — Intake |
| Last gate passed | None |
| Related documents | docs/brd/brd.md, docs/diagrams/diagrams.md |
| Domain | Not confirmed |
| Business owner | [Vai trò] |
| Approver | [Vai trò] |
| Language | vi |
| Skill version | srs-analysis 2.0.0 |

### Revision History

| Version | Date | Author (role) | Changes |
|---|---|---|---|
| 0.1 | [Ngày] | [Vai trò] | Khởi tạo |

## 1. Introduction — Giới thiệu

- **Mục tiêu tài liệu:** [Vì sao viết SRS này, dùng cho ai]
- **Phạm vi:** [Phạm vi kỹ thuật, trỏ sang docs/brd/brd.md cho phạm vi nghiệp vụ]
- **Đối tượng sử dụng:** [Đội phát triển, QA, PM...]
- **Tài liệu tham chiếu:** docs/brd/brd.md, docs/diagrams/diagrams.md
- **Thuật ngữ & viết tắt:** [Thuật ngữ kỹ thuật, nếu có — thuật ngữ nghiệp vụ xem BRD §6]

## 2. High-Level Requirements — Yêu cầu mức độ tổng thể

[Tóm tắt actor chính và luồng chính. Sơ đồ chi tiết (Object/Entity Relationship Diagram, Workflow Diagram, State Transition Diagram, Use Case Diagram) xem docs/diagrams/diagrams.md — DIA-001, DIA-002...]

## 3. Functional Requirements — Yêu cầu chức năng

### Danh sách tác nhân

| Actor | Mô tả | Liên quan BRD |
|---|---|---|
| [Vai trò] | [Mô tả ngắn] | Stakeholders §5 BRD |

### Danh sách chức năng

| Nhóm nghiệp vụ | Chức năng | FR liên quan |
|---|---|---|
| [Nhóm] | [Tên chức năng] | FR-001 |

### Use case tổng quan và phân rã

[Danh sách UC-xxx theo nhóm/actor.]

### UC-001 — [Tên use case]
- **Actors:** [Vai trò]
- **Trigger:** [Sự kiện]
- **Preconditions:** [Điều kiện]
- **Main flow:** [Các bước]
- **Alternate flows:** [Luồng thay thế]
- **Exception flows:** [Luồng lỗi]
- **Postconditions:** [Kết quả]
- **Related:** FR-001
- **Source:** SRC-001
- **Status:** Proposed

### FR-001 — [Tên ngắn]
- **Statement:** Hệ thống phải [nghĩa vụ].
- **Rationale:** [Lý do]
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Proposed
- **Related:** UC-001
- **Acceptance criteria:**
  - AC-FR-001-01: Given [bối cảnh], when [hành động], then [kết quả].
- **Verification:** Test

## 4. Non-Functional Requirements — Yêu cầu phi chức năng

### NFR-001 — [Tên ngắn]
- **Category:** [Hạng mục — hiệu suất, bảo mật kỹ thuật, tính khả dụng...]
- **Statement:** Hệ thống phải [thuộc tính chất lượng].
- **Metric:** [Cách đo]
- **Target:** TBD (Q-001)
- **Source:** SRC-001
- **Priority:** Should
- **Status:** Proposed
- **Verification:** Test

### Design Inputs (UX Brief)

| ID | Type | Description | Source | Status |
|---|---|---|---|---|
| UXP-001 | Preference | [Mong muốn] | SRC-001 | Open |

## 5. Security Requirements — Yêu cầu bảo mật

### Quyền người dùng theo role

[Tóm tắt vai trò và phạm vi quyền tương ứng — xem đầy đủ ở ma trận dưới.]

### Ma trận phân quyền (Permissions)

| Action | [Vai trò A] | [Vai trò B] |
|---|---|---|
| [Hành động] | TBD (Q-001) | TBD (Q-001) |

## 6. Other Requirements and Appendix — Yêu cầu khác và Phụ lục

### Tích hợp

### IR-001 — [Tên ngắn]
- **Statement:** Hệ thống phải [tích hợp gì, với ai].
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Proposed
- **Related:** FR-001
- **Counterpart:** [Hệ thống ngoài]
- **Direction:** [Chiều dữ liệu]
- **Failure handling:** [Xử lý lỗi]
- **Verification:** Test

### Business Rules

### BR-001 — [Tên ngắn]
- **Statement:** [Quy tắc nghiệp vụ].
- **Rationale:** [Vì sao]
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Proposed
- **Related:** FR-001
- **Verification:** Test

### Dữ liệu

### DR-001 — [Tên ngắn]
- **Statement:** Hệ thống phải lưu trữ [loại dữ liệu].
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Proposed
- **Classification:** [Cá nhân/Nghiệp vụ]
- **Retention:** TBD (Q-001)
- **Related:** FR-001
- **Verification:** Inspection

### Workflow chi tiết / Vòng đời và chuyển trạng thái

| From | Event / Trigger | Condition | To | Actor | Related |
|---|---|---|---|---|---|
| [*] | [Sự kiện] | [Điều kiện] | [Trạng thái] | [Vai trò] | FR-001 |

### Open Questions — Câu hỏi mở

| ID | Question | Priority | Ask whom | Status | Answer / Notes |
|---|---|---|---|---|---|
| Q-001 | [Câu hỏi] | P1 | [Vai trò] | Open | |

### Decision Log — Nhật ký quyết định

| ID | Date | Decision | Decided by (role, as stated) | Related |
|---|---|---|---|---|
| DEC-001 | [Ngày] | [Quyết định] | [Vai trò] | [ID] |

### Sources — Nguồn thông tin

| ID | Type | Description | Date | Provided by (role) | Notes |
|---|---|---|---|---|---|
| SRC-001 | Brief | [Mô tả] | [Ngày] | [Vai trò] | |

### Elicitation Coverage — Độ phủ thu thập

| Topic | Status | Notes / Q-ID |
|---|---|---|
| [Chủ đề] | TBD | |

### Traceability Matrix — Ma trận truy vết

| Goal / Source | Requirement | User story | Acceptance criteria | Diagram | Verification | Design ref | Test ref |
|---|---|---|---|---|---|---|---|
| GOAL-001 | FR-001 | | AC-FR-001-01 | DIA-001 | Test | | |

### Change Requests — Yêu cầu thay đổi

Not applicable — chưa có baseline được phê duyệt.

### Approval Record — Hồ sơ phê duyệt

Áp dụng đồng thời cho BRD + SRS + Diagrams (xem `conventions.md` A11).

| Version | Decision | Approver (role, as stated) | Date | Notes |
|---|---|---|---|---|
~~~~
