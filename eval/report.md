# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261128-085253 | 28/29 | 96,6% | 8/8 (100%) | 14/15 (93,3%) | 6/6 (100%) | Đạt ngưỡng tổng ≥80%; chưa tổng hợp đủ kết quả từng metric |
| 2 | Chưa chạy | — | — | — | — | — | Chưa đánh giá |

Kết quả từng câu lượt 1: [run-1.csv](run-1.csv). Trace: [run-1.jsonl](../traces/run-1.jsonl). Model: `gpt-6-luna`; 29/29 câu chạy xong, 0 lỗi kỹ thuật. Lượt 2 chưa chạy.

Lệnh `python run.py score eval/run-1.csv` làm tròn tỷ lệ tổng thành 97%, nhóm `kho` thành 93%. Bảng trên ghi đến một chữ số thập phân.

Chấm bằng đối chiếu nhãn, điểm và trích dẫn với dữ liệu đầu vào, kết hợp đọc yêu cầu hành vi từng câu; chỉ điền `pass` và `ghi_chu`. AI hỗ trợ chấm; chưa có kết quả một thành viên khác chấm độc lập. Tổng cộng 67/67 trích dẫn khớp review tương ứng sau chuẩn hoá dấu câu, chữ hoa và Unicode. Tỷ lệ câu đạt không thay thế việc tổng hợp riêng từng metric đã chốt.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Nhầm thông tin đóng gói / trải nghiệm dùng chung chung với chất lượng | 1 câu không đạt | R16 |
| Sai nhãn nhưng vẫn đạt ngưỡng của câu | 1 câu đạt | R07 |
| Cảm xúc khác expected nhưng không vi phạm pass_criterion của câu | 1 câu đạt | R18 |

**Các sai khác cụ thể** (nhiều sai khác có thể thuộc cùng một câu; chỉ R16 có `pass = 0`):

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| R16 — review 4 | "cũng có chai hơi móp nhưng k sao" trong review chủ yếu nói giao hàng | `chat_luong` | Expected là `van_chuyen`; tiêu chí yêu cầu review 4 là vận chuyển |
| R16 — review 5 | "Giao nhanh, mới xài thì ok, lâu dài thì chưa bít." | `van_chuyen` | Expected là `khong_thong_tin`; toàn câu chỉ đúng 3/5 nhãn, dưới ngưỡng 4/5 |
| R16 — điểm | Expected 3 review chất lượng, 1 tích cực | `1/4` | Expected `1/3`; review 4 bị tính thêm vào mẫu số |
| R07 — review 4 | "Giao hàng nhanh. Đã mua lần 2. Sp tốt. Hình ảnh mang tính chất nhận xu" | `khong_thong_tin` | Expected `van_chuyen`; vẫn đúng 4/5 nhãn và điểm 1/3 nên câu đạt theo tiêu chí |
| R18 — review 5 | "thiết kế đẹp. mình rất thít nhưng âm bass nghe không sâu" | `xau` | Expected `trung_tinh`; tiêu chí câu chỉ yêu cầu bỏ trùng, nhãn, review dài và điểm 2/3, đều đạt. Ghi nhận sai khác nhưng không thêm điều kiện loại sau khi chạy |

## 3. Một lần cải tiến

- Nhóm lỗi dự kiến cải tiến: ranh giới chất lượng / đóng gói / khen chung chung. R16 cho thấy nhãn sai làm lệch mẫu số điểm người mua nhìn thấy.
- Đã sửa gì: chưa thực hiện cải tiến sau lượt 1; dự kiến rà quy tắc chung, không chèn input benchmark vào code và không đổi expected, metric hoặc chuẩn đạt.
- Kết quả trước cải tiến: 28/29 (96,6%); sau cải tiến chưa có lượt 2, chưa kết luận hiệu quả.
- Câu nào **tệ đi** sau khi sửa: chưa xác định vì chưa chạy lượt 2.

## 4. Còn lại

- Lỗi chưa sửa: các sai khác R16, R07, R18 ở trên; nhầm nhãn có thể làm điểm tích cực bị lệch. Chưa có bằng chứng về tác động lên quyết định mua thực tế.
- Nếu có thêm 1 tuần: thu thêm review chưa dùng để chỉnh prompt và tổ chức chấm độc lập để kiểm độ nhất quán nhãn/cảm xúc.
