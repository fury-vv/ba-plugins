# BRD Template — Khung Business Requirement Document

**Mục đích:** khung chuẩn cho `docs/brd/brd.md` — tài liệu yêu cầu nghiệp vụ mức cao, chốt trước khi đi sâu vào đặc tả kỹ thuật ở SRS. Quy ước ID, Document Control, requirement block dùng chung với `conventions.md`.

**Khi dùng:** Phase 0 (tạo khung), Phase 1–2 (điền Goals/Scope/Stakeholders/Assumptions khi đã xác nhận), Phase 5 (duyệt cùng SRS).

## Danh sách section (bắt buộc đúng số thứ tự)

| # | English title | Tiếng Việt | ID định nghĩa tại đây | N/A |
|---|---|---|---|---|
| 1 | Introduction | Giới thiệu | — | Không |
| 2 | Business Context and Problem Statement | Bối cảnh và vấn đề nghiệp vụ | — | Không |
| 3 | Goals and Success Metrics | Mục tiêu và chỉ số thành công | GOAL | Không |
| 4 | Scope | Phạm vi | — | Không |
| 5 | Stakeholders and Users | Các bên liên quan và người dùng | — | Không |
| 6 | Glossary | Thuật ngữ nghiệp vụ | — | Có |
| 7 | Assumptions, Constraints and Dependencies | Giả định, ràng buộc và phụ thuộc | ASM | Không |
| 8 | High-Level Business Processes | Quy trình nghiệp vụ mức cao | — | Có |
| 9 | Risks | Rủi ro | RISK | Không |
| 10 | Approval Record | Phê duyệt | — | Không |

Section 8 chỉ tóm tắt quy trình ở mức nghiệp vụ (vài câu hoặc một sơ đồ tham chiếu `diagrams.md`); đặc tả use case đầy đủ (actor, flow, exception) nằm ở SRS §3, không lặp lại ở đây — trỏ sang `UC-xxx` tương ứng.

## Khung (sao chép để bắt đầu)

~~~~markdown
# Business Requirement Document — [Tên dự án]

| Field | Value |
|---|---|
| Project | [Tên dự án] |
| Document type | BRD |
| Document version | 0.1 |
| Status | DRAFT — NOT APPROVED |
| Current phase | Phase 0 — Intake |
| Last gate passed | None |
| Related documents | docs/srs/srs.md, docs/diagrams/diagrams.md |
| Domain | Not confirmed |
| Business owner | [Vai trò] |
| Approver | [Vai trò] |
| Language | vi |
| Skill version | srs-analysis 2.0.0 |

### Revision History

| Version | Date | Author (role) | Changes |
|---|---|---|---|
| 0.1 | [Ngày] | [Vai trò] | Khởi tạo từ brief |

## 1. Introduction — Giới thiệu

[Mục tiêu của tài liệu BRD này, phạm vi đọc, đối tượng sử dụng (business owner, PM, BA, đội phát triển), tài liệu tham chiếu (docs/srs/srs.md, docs/diagrams/diagrams.md), thuật ngữ/viết tắt dùng trong BRD nếu khác Glossary §6.]

## 2. Business Context and Problem Statement — Bối cảnh và vấn đề nghiệp vụ

[Vấn đề, bối cảnh, hiện trạng, kết quả mong muốn. Câu chưa xác nhận kèm ASM-/Q-.]

## 3. Goals and Success Metrics — Mục tiêu và chỉ số thành công

| ID | Goal | Success metric | Baseline | Target | Source | Status |
|---|---|---|---|---|---|---|
| GOAL-001 | [Mục tiêu] | [Cách đo] | [Hiện tại] | TBD (Q-001) | SRC-001 | Proposed |

## 4. Scope — Phạm vi

### In scope
- [Nội dung]

### Non-goals
- [Nội dung]

### Release boundaries
- [MVP và các giai đoạn sau]

## 5. Stakeholders and Users — Các bên liên quan và người dùng

| Stakeholder / Role | Responsibility | Decision authority | Characteristics |
|---|---|---|---|
| [Vai trò] | [Trách nhiệm] | [Quyền quyết định] | [Số lượng, tần suất, thiết bị, môi trường] |

## 6. Glossary — Thuật ngữ nghiệp vụ

| Term | Definition | Source |
|---|---|---|
| [Thuật ngữ] | [Định nghĩa] | SRC-001 |

## 7. Assumptions, Constraints and Dependencies — Giả định, ràng buộc và phụ thuộc

### Assumptions

| ID | Assumption | Source | Confirm with | Status |
|---|---|---|---|---|
| ASM-001 | [Giả định] | SRC-001 | [Vai trò] | Open |

### Constraints
- [Ràng buộc kèm nguồn]

### Dependencies
- [Phụ thuộc kèm nguồn]

## 8. High-Level Business Processes — Quy trình nghiệp vụ mức cao

[Tóm tắt 1 đoạn/một vài gạch đầu dòng về luồng nghiệp vụ chính, nêu actor chính và tham chiếu use case đầy đủ ở SRS (UC-xxx). Sơ đồ quy trình/Context xem tại docs/diagrams/diagrams.md (DIA-xxx).]

## 9. Risks — Rủi ro

| ID | Risk | Impact | Likelihood | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| RISK-001 | [Rủi ro] | [Tác động] | [Khả năng] | [Giảm thiểu] | [Vai trò] | Open |

## 10. Approval Record — Phê duyệt

Phê duyệt BRD diễn ra đồng thời với SRS ở Gate G5 — xem Approval Record đầy đủ trong `docs/srs/srs.md`. Dòng dưới đây chỉ ghi lại tham chiếu sau khi duyệt:

| Version | Decision | Approver (role, as stated) | Date | Notes |
|---|---|---|---|---|
~~~~
