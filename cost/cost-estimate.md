# Chi phí khi dùng thật — aiphonKupi · CP4

## 1. Đầu vào và phạm vi

- Cấu hình: `cost/personas.yaml`, 50 phiên, seed 42; mỗi phiên một lượt dán danh sách review độc lập. Lấy đầu vào từ cả 29 câu benchmark, gồm thuong/kho/tu_choi; đây là hỗn hợp kiểm thử, chưa phải phân bố nhu cầu ngoài đời.
- Ba persona: ít/vừa/nhiều, share tham khảo 8/23, 9/23, 6/23 trên 23 phiếu có mua trong khảo sát n=24 (`evidence/survey/results.csv`, câu 1). Số phiên/người/tháng 1/4/6 và một lượt/phiên đều **tự ước tính**, chưa đo hành vi dùng sản phẩm.
- Kịch bản người dùng hoạt động: thấp **6**, cơ sở **12**, cao **24** — **tự ước tính**, không phải số người đã dùng hoặc cam kết dùng. Cơ sở 12 tham chiếu quy mô kịch bản ở spec §2.
- Giá Standard USD/triệu token: Luna vào **0,10**, ra **0,50**; Sol vào **2,00**, ra **10,00**. Nguồn kiểm ngày 28/11/2026: [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), [Sol](https://developers.openai.com/api/docs/models/gpt-6.2-sol). Không áp giảm giá cache/Batch/Flex.
- Token đo thật trên **gpt-6-luna**. **Đo trên Luna, tính giá Luna và quy đổi theo giá Sol**; không gọi Sol trong lượt mô phỏng, không khẳng định Sol có cùng lượng token hay chất lượng.
- Tỷ lệ đạt dùng tính chi phí: **28/29 = 96,55%**, lượt **run-1@20261128-085253**. Dùng lượt 1 vì prompt đã khôi phục về bản đó sau thử cải tiến lượt 2; không dùng tỷ lệ 27/29 của prompt thử nghiệm. Đây là ước lượng dựa trên benchmark, không phải chấm lại kết quả 50 phiên mô phỏng.

## 2. Kết quả mô phỏng chính thức

- Run ID: **simulate-1@20261128-103718**.
- Kết quả: [simulate-1.csv](simulate-1.csv); bảng gốc: [simulate-1-summary.md](simulate-1-summary.md); trace: [simulate-1.jsonl](../traces/simulate-1.jsonl).
- **50/50 phiên hoàn tất, 0 lỗi**; ít 18 phiên, vừa 17, nhiều 15. Có 45 lần gọi model; năm phiên xử lý bằng code (S015, S017, S019, S030, S049) có token 0, không phải lỗi API.
- Tổng token: **30.934 vào / 17.057 ra**. Lượt `simulate-try` chỉ thử khung, không cộng vào 50 phiên chính thức; lượt thử tự chọn rate của run-2, còn bản chính thức đã chỉ định rate run-1 đúng cấu hình đang dùng.

Bảng dưới chép nguyên từ summary, đơn vị USD:

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (6 người) | Chi phí / tháng — cơ sở (12 người) | Chi phí / tháng — cao (24 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.00023 | $0.00024 | $0.00024 | $0.0049 | $0.0098 | $0.0197 | $0.00082 |
| gpt-6.2-sol (vào 2.0 · ra 10.0 $/1M) | $0.0046 | $0.0048 | $0.0048 | $0.0983 | $0.1966 | $0.3933 | $0.0164 |

Kiểm tính độc lập từ CSV: chi phí Luna/phiên = (30.934 × 0,10 + 17.057 × 0,50) / 1.000.000 / 50 = **$0,000232438**; chia 28/29 được **$0,000240739/task thành công**. Giá trị trong bảng được làm tròn. Mỗi phiên có một lượt nên chi phí/task thành công trùng chi phí/câu hỏi đạt trong mô hình này.

Chi phí/tháng tính theo từng persona: số người × share × số phiên/người/tháng × chi phí trung bình/phiên của persona, rồi cộng lại. Dùng share cấu hình, không lấy tỷ lệ 18/50, 17/50, 15/50 của lượt lấy mẫu thay cho share người dùng. Tỷ lệ thành công không giả định là 100%.

## 3. So với impact dự kiến

- Spec §2: giả định 12 người × 3 lần/tháng × 1 phút tiết kiệm = 36 phút/tháng, tương đương **3 phút/người/tháng**; chưa đo lợi ích thực tế.
- Với cùng quy mô 12 người, kịch bản persona hiện tại có tần suất bình quân khoảng **3,48 phiên/người/tháng**. Nếu giữ giả định tiết kiệm 1 phút/phiên thì tương đương **41,7 phút/tháng**, không phải lợi ích đã quan sát. Khác số 36 vì spec dùng tần suất làm tròn 3 lần.
- Chi phí model cơ sở Luna khoảng **$0,00082/người/tháng**, tổng **$0,0098/tháng**.
- **Kết luận:** chi phí token không phải trở ngại chính trong kịch bản nhỏ này; chưa đủ căn cứ kết luận sản phẩm đáng triển khai thương mại khi chưa đo thời gian thực tiết kiệm, tỷ lệ sử dụng và chi phí ngoài model.

## 4. Giới hạn và độ nhạy

- Quy đổi cùng token sang giá Sol cho chi phí cao gấp **20 lần** Luna theo bảng giá đã chọn; đây là so sánh giá, không phải thử nghiệm chất lượng Sol. Tỷ lệ đạt Luna không chứng minh tỷ lệ đạt Sol.
- Đầu vào là bộ benchmark ngắn và có lặp. Review dài hơn, nhiều lượt hỏi, retry, model hoặc prompt khác sẽ làm chi phí đổi. Seed cố định chỉ tái lập kế hoạch phiên, không bảo đảm model sinh đúng cùng số token.
- Chưa tính hosting, lưu trữ, thu thập dữ liệu, giờ công kiểm duyệt, thuế hoặc chi phí phục hồi lỗi. Chỉ báo USD vì chưa có nguồn tỷ giá VND.
- Hai lượt eval cho thấy chất lượng nhãn còn lỗi; chưa chấm độc lập bởi người thứ hai. Cần kiểm mẫu người dùng mới và đo trước/sau trước khi suy rộng kết quả.
