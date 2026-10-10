# Business Requirement Document — Dự án thử nghiệm validator

> Fixture kiểm thử: nội dung trừu tượng, không thuộc lĩnh vực nào, không phải yêu cầu thật.

| Field | Value |
|---|---|
| Project | Dự án thử nghiệm validator |
| Document type | BRD |
| Document version | 0.3 |
| Status | DRAFT — NOT APPROVED |
| Current phase | Phase 4 — Self-review |
| Last gate passed | G2 |
| Related documents | docs/srs/srs.md, docs/diagrams/diagrams.md |
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

Tài liệu BRD này mô tả yêu cầu nghiệp vụ mức cao cho dự án thử nghiệm validator. Đối tượng đọc: chủ nghiệp vụ, BA, đội phát triển. Tài liệu liên quan: docs/srs/srs.md, docs/diagrams/diagrams.md.

## 2. Business Context and Problem Statement — Bối cảnh và vấn đề nghiệp vụ

Vai trò A hiện xử lý đối tượng X thủ công. Hệ thống giúp vai trò A tạo và theo dõi đối tượng X, vai trò B duyệt đối tượng X.

## 3. Goals and Success Metrics — Mục tiêu và chỉ số thành công

| ID | Goal | Success metric | Baseline | Target | Source | Status |
|---|---|---|---|---|---|---|
| GOAL-001 | Rút ngắn thời gian xử lý đối tượng X | Thời gian từ lúc tạo đến lúc duyệt | 5 ngày | 2 ngày | SRC-001 | Confirmed |

## 4. Scope — Phạm vi

### In scope
- Tạo, xem, duyệt đối tượng X.

### Non-goals
- Tích hợp với hệ thống bên ngoài.

### Release boundaries
- Bản phát hành đầu gồm toàn bộ phạm vi trên.

## 5. Stakeholders and Users — Các bên liên quan và người dùng

| Stakeholder / Role | Responsibility | Decision authority | Characteristics |
|---|---|---|---|
| Chủ nghiệp vụ | Chịu trách nhiệm nghiệp vụ | Phê duyệt BRD và SRS | 1 người |
| Vai trò A | Tạo đối tượng X | Không | Khoảng 20 người, dùng hằng ngày |
| Vai trò B | Duyệt đối tượng X | Duyệt từng đối tượng | Khoảng 3 người |

## 6. Glossary — Thuật ngữ nghiệp vụ

| Term | Definition | Source |
|---|---|---|
| Đối tượng X | Bản ghi công việc do vai trò A tạo | SRC-001 |

## 7. Assumptions, Constraints and Dependencies — Giả định, ràng buộc và phụ thuộc

### Assumptions

| ID | Assumption | Source | Confirm with | Status |
|---|---|---|---|---|
| ASM-001 | Mọi người dùng có tài khoản trong hệ thống đăng nhập sẵn có | SRC-001 | Bộ phận IT | Confirmed |

### Constraints
- Phát hành trước ngày đã thống nhất (DEC-001).

### Dependencies
- Hệ thống đăng nhập sẵn có của tổ chức (ASM-001).

## 8. High-Level Business Processes — Quy trình nghiệp vụ mức cao

Vai trò A tạo đối tượng X, vai trò B duyệt. Đặc tả use case đầy đủ: UC-001 (xem docs/srs/srs.md §3). Sơ đồ: DIA-001 (xem docs/diagrams/diagrams.md).

## 9. Risks — Rủi ro

| ID | Risk | Impact | Likelihood | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| RISK-001 | Vai trò B vắng mặt làm chậm duyệt | Trung bình | Trung bình | Theo dõi trong vận hành | Chủ nghiệp vụ | Open |

## 10. Approval Record — Phê duyệt

Phê duyệt BRD diễn ra đồng thời với SRS — xem Approval Record đầy đủ trong docs/srs/srs.md.

| Version | Decision | Approver (role, as stated) | Date | Notes |
|---|---|---|---|---|
