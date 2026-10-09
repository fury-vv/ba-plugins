# Quality Checklist — Tự rà soát SRS

**Mục đích:** danh sách kiểm tra chất lượng duy nhất cho Phase 4. Mục `[AUTO <mã>]` do validator kiểm tra; mục `[MANUAL]` phải tự rà soát.
**Khi dùng:** Phase 4, trước khi trình G5; sau mỗi CR ở Phase 6.

Validator chỉ kiểm tra cấu trúc và lỗi cơ học. Pass validator không có nghĩa là SRS đúng về nghiệp vụ.

## Mục lục

1. Cấu trúc
2. ID và tham chiếu
3. Từng requirement
4. Nhất quán giữa các phần
5. Dữ liệu, quyền, luồng
6. NFR
7. UI/UX
8. Sơ đồ
9. Phạm vi và nguồn
10. Phê duyệt

## 1. Cấu trúc

- [AUTO DOC001, DOC002] File không rỗng; mọi khối code đều được đóng.
- [AUTO SEC001, SEC002] Đủ 30 section, đúng số và tên tiếng Anh.
- [AUTO SEC003] Không có section trùng.
- [AUTO SEC004] Không có section rỗng.
- [AUTO SEC005, SEC006] `Not applicable` có lý do và chỉ dùng ở section cho phép.
- [AUTO SEC007] Không có section H2 ngoài danh sách chuẩn.
- [AUTO PH001, PH002] Không còn TBD/TODO/placeholder ngoài các mục đã có `Q-`.

## 2. ID và tham chiếu

- [AUTO ID001] Không có ID định nghĩa trùng.
- [AUTO ID002] Không có tham chiếu tới ID chưa định nghĩa.
- [AUTO ID003] Không có ID sai định dạng.
- [AUTO ID004] AC nằm trong khối cha của nó.
- [MANUAL] Không tái sử dụng ID của requirement đã loại (so với Revision History và bản chụp trước).

## 3. Từng requirement

- [AUTO REQ001] Có đủ Statement, Source, Priority, Status.
- [AUTO REQ002, REQ003] Status và Priority hợp lệ.
- [AUTO REQ004, REQ005] FR có AC; BR, DR, IR, UIR có AC hoặc Verification.
- [AUTO REQ007] Requirement `Superseded` có `Superseded by`.
- [AUTO REQ008] User story có Story, liên kết FR và AC.
- [MANUAL] Mỗi requirement chỉ một nghĩa vụ; không có "và/hoặc" gộp nhiều nghĩa vụ.
- [MANUAL] Rõ ràng: không có từ mơ hồ ("nhanh", "dễ dùng", "phù hợp", "v.v.") thiếu cách đo.
- [MANUAL] Cần thiết: mỗi requirement truy về một GOAL hoặc nguồn.
- [MANUAL] Khả thi trong ràng buộc đã biết (§7).
- [MANUAL] Không mô tả giải pháp kỹ thuật thay cho nhu cầu.
- [MANUAL] AC kiểm thử được, xét đủ danh mục tình huống trong `acceptance-criteria-standard.md`.

## 4. Nhất quán giữa các phần

- [AUTO TR001, TR002] Mọi requirement còn hiệu lực và mọi GOAL có trong ma trận truy vết.
- [MANUAL] Actor trong use case, story, ma trận quyền đều có trong §5.
- [MANUAL] Trạng thái nhắc trong FR/BR khớp bảng §17.
- [MANUAL] Thuật ngữ dùng nhất quán với Glossary §6.
- [MANUAL] Không có hai requirement trùng nghĩa hoặc mâu thuẫn nhau.

## 5. Dữ liệu, quyền, luồng

- [MANUAL] Mỗi hành động trong ma trận quyền có giá trị; không mặc định `Allow` khi chưa rõ.
- [MANUAL] Mỗi use case có luồng ngoại lệ, hủy hoặc khôi phục khi phù hợp.
- [MANUAL] Mỗi loại dữ liệu chính có nguồn chuẩn, phân loại, thời gian lưu và cách xóa (hoặc `Q-`).

## 6. NFR

- [AUTO REQ006] Mỗi NFR có Target và Verification.
- [MANUAL] Target là con số có nguồn, hoặc `TBD (Q-xxx)`; không có con số tự đặt.
- [MANUAL] Đã cân nhắc mọi hạng mục trong `nfr-checklist.md`.

## 7. UI/UX

- [AUTO UI001] Mã màu đúng định dạng HEX.
- [AUTO UI002, UI003] Dòng `UXP-` có Source và Type hợp lệ.
- [MANUAL] Ràng buộc giao diện nằm trong `UIR-`; mong muốn và tham chiếu nằm trong `UXP-`.
- [MANUAL] Không có màu, font, layout do skill tự chọn mà chưa được xác nhận.

## 8. Sơ đồ

- [AUTO DIA001–DIA005] Khối sơ đồ đầy đủ, loại hợp lệ, có Context diagram.
- [MANUAL] Sơ đồ khớp văn bản (xem `diagram-standard.md` mục 6).

## 9. Phạm vi và nguồn

- [AUTO DOM001] §22 không có nội dung khi domain chưa xác nhận.
- [AUTO COV001, COV002] Bảng coverage đủ dòng 2–22, trạng thái hợp lệ.
- [AUTO Q001] Câu hỏi mở có Priority và Status hợp lệ.
- [MANUAL] Không có scope creep: requirement mới đều nằm trong phạm vi §4 hoặc có `DEC-`.
- [MANUAL] Đề xuất của Claude không bị ghi thành `Confirmed`.
- [MANUAL] Không chứa dữ liệu cá nhân hoặc thông tin bí mật thật.
- [MANUAL] Không chứa thông tin của khách hàng hoặc dự án khác.

## 10. Phê duyệt

- [AUTO APR004, APR005] Status và version của tài liệu hợp lệ.
- [AUTO APR001] Tài liệu `APPROVED` có dòng phê duyệt khớp version.
- [AUTO APR002] Tài liệu `APPROVED` không còn requirement `Proposed`.
- [AUTO APR003] Tài liệu `APPROVED` không còn câu hỏi P0 `Open`.
- [MANUAL] Câu hỏi P0 được chấp nhận rủi ro có `DEC-` tương ứng.
