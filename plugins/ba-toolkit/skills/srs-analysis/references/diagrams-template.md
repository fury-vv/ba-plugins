# Diagrams Template — Khung file sơ đồ

**Mục đích:** khung chuẩn cho `docs/diagrams/diagrams.md` — toàn bộ sơ đồ Mermaid dùng chung cho BRD và SRS. Xem `diagram-standard.md` cho danh mục loại sơ đồ, điều kiện kích hoạt và quy ước Mermaid; `conventions.md` A10 cho khối `DIA-`.

**Khi dùng:** Phase 2 (dựng sơ đồ để xác nhận ở G2), Phase 3 (hoàn thiện), Phase 6 (cập nhật sau CR).

## Danh sách section

| # | English title | Tiếng Việt | ID định nghĩa tại đây | N/A |
|---|---|---|---|---|
| 1 | Diagrams | Sơ đồ | DIA | Không |

Phải có ít nhất một sơ đồ `Type: Context`. Các loại khác (Use case, Process, State, Data model, Sequence, Data flow, Rollout) thêm khi hệ thống có đặc điểm tương ứng — xem `diagram-standard.md` mục 2.

## Khung (sao chép để bắt đầu)

~~~~markdown
# Diagrams — [Tên dự án]

| Field | Value |
|---|---|
| Project | [Tên dự án] |
| Document type | Diagrams |
| Document version | 0.1 |
| Status | DRAFT — NOT APPROVED |
| Current phase | Phase 0 — Intake |
| Last gate passed | None |
| Related documents | docs/brd/brd.md, docs/srs/srs.md |
| Domain | Not confirmed |
| Language | vi |
| Skill version | srs-analysis 2.0.0 |

### Revision History

| Version | Date | Author (role) | Changes |
|---|---|---|---|
| 0.1 | [Ngày] | [Vai trò] | Khởi tạo |

## 1. Diagrams — Sơ đồ

### DIA-001 — Context diagram
- **Type:** Context
- **Source:** FR-001
- **Status:** Proposed

```mermaid
flowchart LR
    ACTOR["Vai trò A"] -->|"FR-001"| SYS["Hệ thống"]
```
~~~~

Thêm các khối `### DIA-00N — <Tên sơ đồ>` khác ngay dưới, mỗi khối một loại sơ đồ (Use case / Process / State / Data model / Sequence …), theo mẫu ở `diagram-standard.md` mục 5.
