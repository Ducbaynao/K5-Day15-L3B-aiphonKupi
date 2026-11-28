# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261128-085253 | 28/29 | 96,6% | 8/8 (100%) | 14/15 (93,3%) | 6/6 (100%) | Đạt ngưỡng tổng ≥80%; chưa tổng hợp đủ kết quả từng metric |
| 2 | run-2@20261128-102256 | 27/29 | 93,1% | 7/8 (87,5%) | 14/15 (93,3%) | 6/6 (100%) | Đạt ngưỡng tổng ≥80%; chưa tổng hợp đủ kết quả từng metric |

Kết quả từng câu: [run-1.csv](run-1.csv), [run-2.csv](run-2.csv). Trace: [run-1.jsonl](../traces/run-1.jsonl), [run-2.jsonl](../traces/run-2.jsonl). Cả hai lượt dùng `gpt-6-luna`, chạy 29/29 câu, 0 lỗi kỹ thuật, cùng benchmark và chuẩn chấm. Prompt thử nghiệm lượt 2 lưu đầy đủ tại [run-2-system.txt](prompts/run-2-system.txt); sau đánh giá đã đưa prompt đang dùng về bản lượt 1 vì kết quả giảm.

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

- Nhóm lỗi nhắm tới: ranh giới chất lượng / đóng gói / khen chung chung. R16 cho thấy nhãn sai làm lệch mẫu số điểm người mua nhìn thấy.
- Đã thử: ưu tiên loại sản phẩm khác; phân biệt chi tiết chất lượng sử dụng với hư hại giao nhận nhẹ; tách cảm nhận chung chung khỏi trải nghiệm dịch vụ. Chỉ sửa prompt chung, không so khớp nguyên văn câu thử và không đổi công thức hoặc benchmark.
- Bộ phát triển ngoài benchmark: 9 review dựng, đáp án ghi sẵn trước khi gọi model, tại `eval/check_review_boundaries.py`. Prompt cũ đạt 8/9 nhãn, prompt thử nghiệm đạt 9/9 (mỗi bản một lần, không phải kết quả kiểm thử độc lập hoặc đánh giá trên người thật).
- Kết quả chính thức: **28/29 (96,6%) → 27/29 (93,1%)**, giảm 1 câu đạt (3,4 điểm phần trăm, tính từ tỷ lệ chưa làm tròn). **Giả thuyết cải tiến chưa thành công**; không chọn prompt thử nghiệm làm bản đang dùng. Đã khôi phục `agent.py` về prompt trước cải tiến, giữ nguyên lượt 2 và lưu prompt thử nghiệm để tái lập.
- Nhóm lỗi R16: 0/1 câu đạt → 0/1; review 4 đã đúng `van_chuyen`, nhưng review 1 bị gán `van_chuyen` thay vì `chat_luong`, review 5 vẫn sai. Output trở thành KHÔNG ĐỦ CĂN CỨ thay vì điểm 1/3.
- Câu **tệ đi về pass**: R17, từ đạt sang không đạt; review 5 bị coi là chất lượng làm điểm 4/5 thay vì 3/4. R01 review 5, R12 review 4 và B14 review 4 cũng phát sinh sai nhãn, nhưng vẫn đạt pass_criterion. R07 sửa được nhãn review 4 (5/5); R18 vẫn khác cảm xúc so với expected nhưng đạt tiêu chí.
- Kiểm bằng cùng cách chấm: 66/66 trích dẫn lượt 2 khớp review sau chuẩn hoá; không thấy hành vi vượt thẩm quyền trong 6 câu tu_choi. AI hỗ trợ chấm, chưa có người thứ hai chấm độc lập. Không suy rộng từ một lần chạy rằng thay đổi prompt là nguyên nhân duy nhất; model có thể biến thiên giữa các lần.

## 4. Còn lại

- Bản đang dùng đã trở về prompt lượt 1, nên các sai khác R16/R07/R18 của lượt 1 vẫn là vấn đề chưa giải quyết. Lượt 2 bổ sung bằng chứng ranh giới nhãn chưa ổn định; nhầm nhãn có thể làm điểm tích cực bị lệch. Chưa có bằng chứng về tác động lên quyết định mua thực tế.
- Nếu có thêm 1 tuần: thu thêm review chưa dùng để chỉnh prompt và tổ chức chấm độc lập để kiểm độ nhất quán nhãn/cảm xúc.
