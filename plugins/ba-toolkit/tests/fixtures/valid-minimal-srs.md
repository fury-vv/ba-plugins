# Software Requirements Specification — Dự án thử nghiệm validator

> Fixture kiểm thử: nội dung trừu tượng, không thuộc lĩnh vực nào, không phải yêu cầu thật.

| Field | Value |
|---|---|
| Project | Dự án thử nghiệm validator |
| Document type | SRS |
| Document version | 0.3 |
| Status | DRAFT — NOT APPROVED |
| Current phase | Phase 4 — Self-review |
| Last gate passed | G2 |
| Related documents | docs/brd/brd.md, docs/diagrams/diagrams.md |
| Domain | Not confirmed |
| Business owner | Chủ nghiệp vụ |
| Approver | Chủ nghiệp vụ |
| Language | vi |
| Skill version | srs-analysis 2.0.0 |

### Revision History

| Version | Date | Author (role) | Changes |
|---|---|---|---|
| 0.1 | 2026-10-01 | BA | Khởi tạo |
| 0.3 | 2026-10-05 | BA | Hoàn thiện bản nháp |

## 1. Introduction — Giới thiệu

Tài liệu SRS này đặc tả kỹ thuật cho dự án thử nghiệm validator. Đối tượng đọc: đội phát triển, QA. Tài liệu tham chiếu: docs/brd/brd.md, docs/diagrams/diagrams.md.

## 2. High-Level Requirements — Yêu cầu mức độ tổng thể

Hai actor chính: Vai trò A (tạo đối tượng X), Vai trò B (duyệt đối tượng X). Sơ đồ Context và State xem docs/diagrams/diagrams.md — DIA-001, DIA-002.

## 3. Functional Requirements — Yêu cầu chức năng

### Danh sách tác nhân

| Actor | Mô tả | Liên quan BRD |
|---|---|---|
| Vai trò A | Tạo đối tượng X | Stakeholders §5 BRD |
| Vai trò B | Duyệt đối tượng X | Stakeholders §5 BRD |

### Danh sách chức năng

| Nhóm nghiệp vụ | Chức năng | FR liên quan |
|---|---|---|
| Đối tượng X | Tạo đối tượng X | FR-001 |
| Đối tượng X | Duyệt đối tượng X | FR-002 |

### UC-001 — Tạo và duyệt đối tượng X
- **Actors:** Vai trò A, Vai trò B
- **Trigger:** Vai trò A cần ghi nhận một công việc mới
- **Preconditions:** Người dùng đã đăng nhập
- **Main flow:** 1. Vai trò A tạo đối tượng X. 2. Vai trò B duyệt.
- **Alternate flows:** Vai trò B từ chối, vai trò A sửa và gửi lại.
- **Exception flows:** Thiếu thông tin bắt buộc thì không gửi được.
- **Postconditions:** Đối tượng X ở trạng thái Đã duyệt hoặc Bị từ chối.
- **Related:** FR-001, FR-002
- **Source:** SRC-001
- **Status:** Confirmed

### FR-001 — Tạo đối tượng X
- **Statement:** Hệ thống phải cho phép vai trò A tạo đối tượng X với các trường bắt buộc đã thống nhất.
- **Rationale:** Thay cho ghi nhận thủ công.
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Confirmed
- **Related:** UC-001, DR-001
- **Acceptance criteria:**
  - AC-FR-001-01: Given vai trò A đã đăng nhập, when gửi đối tượng X đủ trường bắt buộc, then đối tượng X được lưu ở trạng thái Chờ duyệt.
  - AC-FR-001-02: Given vai trò A đã đăng nhập, when gửi đối tượng X thiếu trường bắt buộc, then hệ thống từ chối và chỉ ra trường còn thiếu.
- **Verification:** Test

### FR-002 — Duyệt đối tượng X
- **Statement:** Hệ thống phải cho phép vai trò B duyệt hoặc từ chối đối tượng X đang chờ duyệt.
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Confirmed
- **Related:** UC-001, BR-001
- **Acceptance criteria:**
  - AC-FR-002-01: Given đối tượng X ở trạng thái Chờ duyệt, when vai trò B duyệt, then đối tượng X chuyển sang Đã duyệt.
- **Verification:** Test

### US-001 — Tạo đối tượng X
- **Story:** As a vai trò A, I want tạo đối tượng X, so that công việc được ghi nhận và theo dõi.
- **Related:** FR-001
- **Priority:** Must
- **Status:** Confirmed
- **Acceptance criteria:** see AC-FR-001-01, AC-FR-001-02

## 4. Non-Functional Requirements — Yêu cầu phi chức năng

### NFR-001 — Thời gian mở danh sách
- **Category:** Hiệu năng
- **Statement:** Hệ thống phải hiển thị danh sách đối tượng X trong thời gian đã thống nhất.
- **Metric:** Thời gian từ lúc mở trang đến lúc danh sách hiển thị
- **Target:** 3 giây với 95% lượt mở trong giờ làm việc
- **Source:** SRC-001
- **Priority:** Should
- **Status:** Confirmed
- **Verification:** Test

### UIR-001 — Màu thương hiệu
- **Statement:** Giao diện phải dùng màu chủ đạo #1A73E8 theo guideline đã nhận.
- **Source:** SRC-002
- **Priority:** Should
- **Status:** Confirmed
- **Verification:** Inspection

### Design Inputs (UX Brief)

| ID | Type | Description | Source | Status |
|---|---|---|---|---|
| UXP-001 | Preference | Giao diện thoáng, ít màu | SRC-001 | Confirmed |

## 5. Security Requirements — Yêu cầu bảo mật

### Quyền người dùng theo role

Vai trò A chỉ tạo được đối tượng X của mình; Vai trò B chỉ duyệt, không tự duyệt đối tượng do chính mình tạo (BR-001).

### Ma trận phân quyền (Permissions)

| Action | Vai trò A | Vai trò B |
|---|---|---|
| Tạo đối tượng X | Allow | Deny |
| Duyệt đối tượng X | Deny | Conditional (BR-001) |

## 6. Other Requirements and Appendix — Yêu cầu khác và Phụ lục

### Tích hợp

Not applicable — phạm vi đã loại trừ tích hợp với hệ thống bên ngoài (BRD §4).

### Business Rules

### BR-001 — Không tự duyệt
- **Statement:** Người tạo đối tượng X không được duyệt chính đối tượng đó.
- **Source:** SRC-001
- **Priority:** Must
- **Status:** Confirmed
- **Verification:** Test

### Dữ liệu

### DR-001 — Lưu lịch sử trạng thái
- **Statement:** Hệ thống phải lưu lịch sử chuyển trạng thái của đối tượng X, gồm người thực hiện và thời điểm.
- **Source:** SRC-001
- **Priority:** Should
- **Status:** Confirmed
- **Classification:** Nội bộ
- **Acceptance criteria:**
  - AC-DR-001-01: Given đối tượng X vừa được duyệt, when xem lịch sử, then thấy người duyệt và thời điểm duyệt.

### Workflow chi tiết / Vòng đời và chuyển trạng thái

| From | Event / Trigger | Condition | To | Actor | Related |
|---|---|---|---|---|---|
| Chờ duyệt | Duyệt | Không phải người tạo | Đã duyệt | Vai trò B | FR-002, BR-001 |

### Open Questions — Câu hỏi mở

| ID | Question | Priority | Ask whom | Status | Answer / Notes |
|---|---|---|---|---|---|
| Q-001 | Có cần báo cáo trong bản phát hành đầu không? | P1 | Chủ nghiệp vụ | Answered | Không cần (DEC-001) |

### Decision Log — Nhật ký quyết định

| ID | Date | Decision | Decided by (role, as stated) | Related |
|---|---|---|---|---|
| DEC-001 | 2026-10-03 | Chưa làm báo cáo, thông báo trong bản phát hành đầu | Chủ nghiệp vụ | Q-001 |

### Sources — Nguồn thông tin

| ID | Type | Description | Date | Provided by (role) | Notes |
|---|---|---|---|---|---|
| SRC-001 | Brief | Brief dự án thử nghiệm | 2026-10-01 | Chủ nghiệp vụ | |
| SRC-002 | Document | Guideline nhận diện thử nghiệm | 2026-10-02 | Chủ nghiệp vụ | |

### Elicitation Coverage — Độ phủ thu thập

| Topic | Status | Notes / Q-ID |
|---|---|---|
| Business context | Answered | |
| Goals | Answered | |
| Scope | Answered | |
| Stakeholders | Answered | |
| Glossary | Answered | |
| Assumptions | Answered | |
| Use cases | Answered | |
| Functional requirements | Answered | |
| Business rules | Answered | |
| Data | Answered | |
| Integration | Not applicable | Ngoài phạm vi |
| UI | Answered | |
| Non-functional requirements | Answered | |
| Permissions | Answered | |
| Workflow | Answered | |
| Diagrams | Answered | |

### Traceability Matrix — Ma trận truy vết

| Goal / Source | Requirement | User story | Acceptance criteria | Diagram | Verification | Design ref | Test ref |
|---|---|---|---|---|---|---|---|
| GOAL-001 | FR-001 | US-001 | AC-FR-001-01, AC-FR-001-02 | DIA-001 | Test | | |
| GOAL-001 | FR-002 | | AC-FR-002-01 | DIA-002 | Test | | |
| GOAL-001 | BR-001 | | | DIA-002 | Test | | |
| GOAL-001 | DR-001 | | AC-DR-001-01 | | Test | | |
| SRC-002 | UIR-001 | | | | Inspection | | |
| GOAL-001 | NFR-001 | | | | Test | | |

### Change Requests — Yêu cầu thay đổi

Not applicable — chưa có baseline được phê duyệt.

### Approval Record — Hồ sơ phê duyệt

Áp dụng đồng thời cho BRD + SRS + Diagrams.

| Version | Decision | Approver (role, as stated) | Date | Notes |
|---|---|---|---|---|
