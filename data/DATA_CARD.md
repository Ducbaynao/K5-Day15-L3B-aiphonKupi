# Data card — dữ liệu bản chạy thử dùng

> Bản đầu (CP2). Cập nhật đủ ở CP3 khi có review thật đã chép.
> Không commit dữ liệu cá nhân thật: bỏ tên người viết review, tên shop, link ảnh đại diện; mỗi review trích tối đa 2 câu.

## Dataset 1 · ViSpamReviews v1 (review thật, nhãn của nhóm tác giả)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (`evidence/count_vispam.py`) · nguồn review cho 7/14 câu thử (`source = data_that`) |
| Từ đâu | Van Dinh, Luu & Nguyen (2022), *Detecting Spam Reviews on Vietnamese E-commerce Websites* — [arXiv 2207.14636](https://arxiv.org/abs/2207.14636). Tải từ https://github.com/sonlam1102/vispamdetection (`dataset/vispamdetection_dataset.zip`). Tác giả ghi dùng cho mục đích nghiên cứu |
| Xử lý những bước gì | Không commit dataset (giải nén ra ngoài repo / `data/raw/` đã có trong `.gitignore`) · chỉ chép ~35 review ngắn vào bộ câu thử, ghi số dòng gốc + nhãn gốc · dataset không có tên người viết · nhóm gán lại nhãn theo 4 nhãn của mình cho các review được chọn (quy tắc ở `codebase/agent.py`, biến `SYSTEM`) |
| Số dòng / số đoạn | 19.870 review (train 14.306 · dev 1.590 · test 3.974); 18.543 review 5★ |
| Phiên bản / ngày lấy | v1, xem 27/11/2026 |
| Nhãn | thật. Cột gốc: `Rating, Comment, Label, SpamLabel` (0 bình thường · 1 khen theo mẫu · 2 chỉ nói shop / giao hàng / giá · 3 không liên quan) |
| Giới hạn | Thu khoảng 2021–2022, chủ yếu Shopee / Tiki · v1 không có tên sản phẩm, nên câu thử ghép review của nhiều sản phẩm và bỏ tên sản phẩm · nhãn gốc rộng hơn định nghĩa của nhóm (vd "Khá ok. Hài lòng" = bình thường) |

## Dataset 2 · Review dựng cho bộ câu thử (`eval/benchmark.csv`, source = `tu_viet`)

| | |
|---|---|
| Dùng để làm gì | 7/14 câu thử: tình huống khó hiếm gặp trong mẫu thật: seeding trùng văn phong, review sản phẩm khác bị gắn sang, chèn lệnh vào review, đòi thông tin cá nhân |
| Từ đâu | Nhóm tự viết theo văn phong review thật trên sàn; tình huống "nồi chiên 6 lít" lấy từ file track D của BTC |
| Xử lý những bước gì | Mỗi câu ghi sẵn nhãn đúng từng review ở cột `expected`; người thứ hai trong nhóm đọc lại nhãn |
| Số dòng / số đoạn | 7 câu thử (B03, B07, B08, B10–B13) · bộ câu thử CP2 = 14 câu, mở rộng 20–30 ở CP3 |
| Phiên bản / ngày lấy | 27/11/2026 |
| Nhãn | `synthetic` — viết tay, không sinh bằng script nên không có seed |
| Giới hạn | Văn phong do nhóm viết, có thể "sạch" hơn review thật (ít viết tắt, ít emoji). **Không phải bằng chứng pain.** |
