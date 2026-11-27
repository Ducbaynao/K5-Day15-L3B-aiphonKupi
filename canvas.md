# Canvas — aiphonKupi · Track D

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track D · Thương mại điện tử — tách đánh giá về chất lượng sản phẩm khỏi review không có thông tin và review chỉ nói về vận chuyển trên sàn mua sắm |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Người mua trên sàn (Shopee, Lazada, TikTok Shop) đang phân vân một sản phẩm từ 200k trở lên và đọc review trước khi đặt |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Người mua đọc review để quyết định mua, nhưng gặp review chỉ nói giao hàng, chưa dùng hoặc khen chung chung; họ phải tự lọc để tìm thông tin chất lượng. Giả thuyết cần khảo sát: việc này tốn thời gian và có thể dẫn đến quyết định mua sai |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | **5.052/18.543 review 5★ (27,2%) có SpamLabel ≠ 0 theo nhãn gốc ViSpamReviews**, gấp ~2,2 lần tỷ lệ ở review 1–3★ (99/802 = 12,3%); đếm bằng `evidence/count_vispam.py`. Đây là tỷ lệ nhãn spam gốc, chưa đồng nhất với tỷ lệ review thiếu thông tin chất lượng theo quy tắc của nhóm. Trích dẫn (dòng 3243, 5★): "chưa sử dụnh nên k biết chất lượng như thế nào". Khảo sát ≥20 người mua trong lớp đang thu |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | Một người mua · dán danh sách review của một sản phẩm · AI gán nhãn từng review (chất lượng / vận chuyển / không có thông tin / nói về sản phẩm khác) · người mua nhận điểm chất lượng chỉ tính từ review có thông tin, kèm 3 trích dẫn làm căn cứ |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI chỉ gán nhãn và trích căn cứ; điểm chất lượng do code tính; AI không kết luận "shop lừa đảo / review giả", không khuyên mua hay không mua. Lý do: gán sai thì người mua mua phải hàng kém (mất tiền, phải đổi trả) hoặc shop bị mang tiếng oan |
| 7 | Phân công có tên | Phạm Lý Ngọc Đức (đội trưởng): canvas, spec, bảng impact, giữ mạch câu chuyện · Nguyễn Huy Tấn: khảo sát ≥20 người + phỏng vấn · Nguyễn Anh Quân: chép và gán nhãn ~200 review, script đếm · Nguyễn Minh Triết: khung bản chạy thử (LLM gán nhãn + code tính điểm) + data card |
| — | *(CP2)* Đã đổi gì so với CP1 | Nguồn bằng chứng: dùng dataset ViSpamReviews thay cho chép tay 200 review · đếm được 27,2% review 5★ có nhãn spam gốc; khác định nghĩa với giả thuyết ≥40% thiếu thông tin chất lượng nên chưa xác nhận hay bác bỏ giả thuyết · giữ lát cắt để kiểm tiếp bằng gán nhãn và khảo sát · thêm "khen chung chung" vào `khong_thong_tin` |
