# Quality Checklist — Tự rà soát BRD / SRS / Diagrams

**Mục đích:** danh sách kiểm tra chất lượng duy nhất cho Phase 4, áp dụng cho cả 3 file (BRD, SRS, Diagrams). Mục `[AUTO <mã>]` do validator (`scripts/validate_docs.py`) kiểm tra; mục `[MANUAL]` phải tự rà soát.
**Khi dùng:** Phase 4, trước khi trình G5; sau mỗi CR ở Phase 6.

Validator chỉ kiểm tra cấu trúc và lỗi cơ học. Pass validator không có nghĩa là nội dung đúng về nghiệp vụ.

## Mục lục

1. Cấu trúc
2. ID và tham chiếu (xuyên 3 file)
3. Từng requirement
4. Nhất quán giữa các phần
5. Dữ liệu, quyền, luồng
6. NFR
7. UI/UX
8. Sơ đồ
9. Phạm vi và nguồn
10. Phê duyệt (cả 3 file)

## 1. Cấu trúc

- [AUTO DOC001, DOC002] Mỗi file không rỗng; mọi khối code đều được đóng.
- [AUTO DOC003] Mỗi file có bảng Document Control ở phần mở đầu (trước section 1).
- [AUTO SEC001, SEC002] Mỗi file đủ section theo đúng khung của nó (BRD 10 section, SRS 6 section, Diagrams 1 section), đúng số và tên tiếng Anh.
- [AUTO SEC003] Không có section trùng trong cùng file.
- [AUTO SEC004] Không có section rỗng.
- [AUTO SEC005, SEC006] `Not applicable` có lý do và chỉ dùng ở section cho phép (SRS §4 và §5 không được `Not applicable`).
- [AUTO SEC007] Không có section H2 ngoài danh sách chuẩn của loại file đó.
- [AUTO PH001, PH002] Không còn TBD/TODO/placeholder ngoài các mục đã có `Q-`.
- [AUTO IO002] Nếu một trong 3 file chưa được cung cấp cho validator, kiểm tra đã nhận biết và hạ mức tham chiếu treo liên quan xuống WARNING.

## 2. ID và tham chiếu (xuyên 3 file)

- [AUTO ID001] Không có ID định nghĩa trùng — kể cả trùng giữa hai file khác nhau.
- [AUTO ID002] Không có tham chiếu tới ID chưa được định nghĩa ở file nào trong 3 file.
- [AUTO ID003] Không có ID sai định dạng.
- [AUTO ID004] AC nằm trong khối cha của nó.
- [AUTO DOC004, DOC005] Document version và Status khớp nhau giữa các file đang có.
- [MANUAL] Không tái sử dụng ID của requirement đã loại (so với Revision History và bản chụp trước).

## 3. Từng requirement

- [AUTO REQ001] Có đủ Statement, Source, Priority, Status.
- [AUTO REQ002, REQ003] Status và Priority hợp lệ.
- [AUTO REQ004, REQ005] FR có AC; BR, DR, IR, UIR có AC hoặc Verification.
- [AUTO REQ007] Requirement `Superseded` có `Superseded by`.
- [AUTO REQ008] User story có Story, liên kết FR và AC.
- [MANUAL] Mỗi requirement chỉ một nghĩa vụ; không có "và/hoặc" gộp nhiều nghĩa vụ.
- [MANUAL] Rõ ràng: không có từ mơ hồ ("nhanh", "dễ dùng", "phù hợp", "v.v.") thiếu cách đo.
- [MANUAL] Cần thiết: mỗi requirement truy về một GOAL (BRD §3) hoặc nguồn.
- [MANUAL] Khả thi trong ràng buộc đã biết (BRD §7).
- [MANUAL] Không mô tả giải pháp kỹ thuật thay cho nhu cầu.
- [MANUAL] AC kiểm thử được, xét đủ danh mục tình huống trong `acceptance-criteria-standard.md`.

## 4. Nhất quán giữa các phần

- [AUTO TR001, TR002] Mọi requirement còn hiệu lực và mọi GOAL có trong Traceability Matrix (SRS §6).
- [MANUAL] Actor trong use case, story, ma trận quyền đều có trong Stakeholders (BRD §5).
- [MANUAL] Trạng thái nhắc trong FR/BR khớp bảng workflow chi tiết (SRS §6).
- [MANUAL] Thuật ngữ dùng nhất quán với Glossary (BRD §6).
- [MANUAL] Không có hai requirement trùng nghĩa hoặc mâu thuẫn nhau, kể cả giữa BRD và SRS.

## 5. Dữ liệu, quyền, luồng

- [MANUAL] Mỗi hành động trong ma trận quyền (SRS §5) có giá trị; không mặc định `Allow` khi chưa rõ.
- [MANUAL] Mỗi use case có luồng ngoại lệ, hủy hoặc khôi phục khi phù hợp.
- [MANUAL] Mỗi loại dữ liệu chính (DR- ở SRS §6) có nguồn chuẩn, phân loại, thời gian lưu và cách xóa (hoặc `Q-`).

## 6. NFR

- [AUTO REQ006] Mỗi NFR có Target và Verification.
- [MANUAL] Target là con số có nguồn, hoặc `TBD (Q-xxx)`; không có con số tự đặt.
- [MANUAL] Đã cân nhắc mọi hạng mục trong `nfr-checklist.md`.

## 7. UI/UX

- [AUTO UI001] Mã màu đúng định dạng HEX.
- [AUTO UI002, UI003] Dòng `UXP-` có Source và Type hợp lệ.
- [MANUAL] Ràng buộc giao diện nằm trong `UIR-`; mong muốn và tham chiếu nằm trong `UXP-` (cả hai ở SRS §4).
- [MANUAL] Không có màu, font, layout do skill tự chọn mà chưa được xác nhận.

## 8. Sơ đồ

- [AUTO DIA001–DIA004] Khối sơ đồ (trong `diagrams.md`) đầy đủ, loại hợp lệ.
- [AUTO DIA005] Có ít nhất một sơ đồ `Type: Context` trong `diagrams.md`.
- [MANUAL] Sơ đồ khớp văn bản ở BRD/SRS (xem `diagram-standard.md` mục 6).

## 9. Phạm vi và nguồn

- [AUTO COV001, COV002] Bảng Elicitation Coverage (SRS §6) có mặt, trạng thái hợp lệ. Danh sách chủ đề giờ tự do (không còn gắn cứng theo số section cố định) — tự rà soát xem đã đủ chủ đề quan trọng chưa.
- [AUTO Q001] Câu hỏi mở có Priority và Status hợp lệ.
- [MANUAL] Không có scope creep: requirement mới đều nằm trong phạm vi Scope (BRD §4) hoặc có `DEC-`.
- [MANUAL] Đề xuất của Claude không bị ghi thành `Confirmed`.
- [MANUAL] Không chứa dữ liệu cá nhân hoặc thông tin bí mật thật.
- [MANUAL] Không chứa thông tin của khách hàng hoặc dự án khác.
- [MANUAL] Nội dung đặc thù lĩnh vực (nếu có, ở BRD §2) chỉ xuất hiện sau khi Domain đã `Confirmed` trong Document Control.

## 10. Phê duyệt (cả 3 file)

- [AUTO APR004, APR005] Status và version của mỗi file hợp lệ.
- [AUTO APR001] Khi có file `APPROVED`, Approval Record (trong SRS) có dòng phê duyệt khớp version.
- [AUTO APR002] Khi `APPROVED`, không còn mục Status `Proposed` ở bất kỳ file nào.
- [AUTO APR003] Khi `APPROVED`, không còn câu hỏi nào ở trạng thái `Open` trong SRS — bất kỳ mức P0, P1 hay P2.
- [MANUAL] Câu hỏi được chấp nhận rủi ro hoặc chuyển `Deferred` (ở bất kỳ mức) có `DEC-` tương ứng.
- [MANUAL] Cả 3 file có cùng Document version và Status trước khi trình G5.
