# Đào data — cách đếm và kết quả

> Repo chỉ chứa số đã tổng hợp và vài dòng ví dụ — không chép lại nguyên dataset.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** ViSpamReviews v1 (Van Dinh, Luu & Nguyen, 2022 — [arXiv 2207.14636](https://arxiv.org/abs/2207.14636)), review thật của người mua trên sàn TMĐT Việt Nam, do nhóm tác giả UIT gán nhãn. Tải từ https://github.com/sonlam1102/vispamdetection (`dataset/vispamdetection_dataset.zip`), xem 27/11/2026. Dataset dùng cho nghiên cứu → **không commit vào repo**.
- **Đếm gì:** số review 5★ **có nhãn spam gốc** · trên cả 3 file train + dev + test · lọc `Rating = 5`.
- **Nhãn spam gốc =** `SpamLabel ≠ 0` theo nhãn của nhóm tác giả: 1 = review giả (khen theo mẫu) · 2 = chỉ nói shop / giao hàng / giá · 3 = không liên quan, vô nghĩa. Nhóm **không tự gán lại** ở bước này. Tên nhãn không phải kết luận của nhóm về tính xác thực của từng review; các nhãn này không đồng nhất với bốn nhãn phục vụ đánh giá thông tin chất lượng của nhóm.
- **Mẫu số:** toàn bộ review 5★ (N = 18.543). So sánh thêm với review 1–4★.
- **Script:** `evidence/count_vispam.py` — chạy `python evidence/count_vispam.py <thư mục dataset>` ra đúng các số dưới.

## 2. Đọc trước, đếm sau

Đã đọc ~100 dòng đầu file test và mô tả nhãn trong bài báo. Các kiểu review thấy được:
- Khen theo mẫu gần như giống hệt nhau giữa nhiều review ("Chất lượng sản phẩm tuyệt vời. Đóng gói… Giao hàng nhanh.").
- Chỉ nói giao hàng / đóng gói / shipper, có khi ghi thẳng "chưa sử dụng".
- Ký tự vô nghĩa, kéo dài chữ ("Okkkk…", "Nhanhhhh…") — đủ độ dài để nhận xu.
- Khen chung chung "Khá ok. Hài lòng" — nhãn gốc là bình thường (0) nhưng không có chi tiết nào về sản phẩm.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Review 5★ có nhãn spam gốc (`SpamLabel ≠ 0`) | 5.052 / 18.543 | 27,2% | Số chính |
| · trong đó vô nghĩa / không liên quan (3) | 3.338 / 18.543 | 18,0% | |
| · chỉ nói shop / giao hàng / giá (2) | 1.440 / 18.543 | 7,8% | |
| · khen theo mẫu (1) | 274 / 18.543 | 1,5% | |
| So sánh: review 1–3★ có nhãn spam gốc | 99 / 802 | 12,3% | 5★ gấp ~2,2 lần |
| Review 5★ trên tổng số review | 18.543 / 19.870 | 93,3% | Phân bố sao lệch về 5★ trong dataset; chưa đo khả năng phân biệt giữa các sản phẩm |

**Kết luận bước 1 (nhãn spam gốc):** trong dataset này, 27,2% review 5★ có nhãn spam gốc; tỷ lệ này cao khoảng 2,2 lần nhóm 1–3★. Vì nhãn gốc không đồng nhất với 4 nhãn của nhóm (ví dụ 4 và 5 cho thấy độ lệch theo cả hai hướng), nhóm thực hiện thêm bước gán lại mẫu 50 review bên dưới để kiểm chứng giả thuyết CP1 (≥40%).

**Tái lập:** chạy `python evidence/count_vispam.py data/raw/dataset`: 19.870 review, 18.543 review 5★; số lượng nhãn 0/1/2/3 lần lượt là 13.491/274/1.440/3.338.

## 3b. Gán lại mẫu 50 review 5★ theo 4 nhãn của nhóm (`evidence/sample50.py`)

- **Cách lấy mẫu:** Lấy ngẫu nhiên 50 review 5★ trong `test.csv` bằng `random.Random(42).sample(...)` (trên bản ViSpamReviews v2 có `product_name` đi kèm để nhận diện `san_pham_khac`). Gán nhãn theo đúng quy tắc 4 nhãn trong `codebase/agent.py`.
- **Kết quả (`python evidence/sample50.py`):**

| Nhãn của nhóm | x / 50 | % | Ghi chú |
|---|---|---|---|
| **Thiếu thông tin chất lượng** (`≠ chat_luong`) | **30 / 50** | **60,0%** | **Vượt ngưỡng giả thuyết ≥40%** |
| · `khong_thong_tin` | 23 / 50 | 46,0% | Khen chung chung, chưa dùng, ký tự vô nghĩa, quảng cáo |
| · `van_chuyen` | 5 / 50 | 10,0% | Chỉ nói giá, giao hàng, nạp nhanh |
| · `san_pham_khac` | 2 / 50 | 4,0% | Dòng 1843 (thẻ Vina khen mùi thơm), dòng 3533 (Hộp đựng giày nhưng review giày đế cao) |
| Có thông tin chất lượng (`chat_luong`) | 20 / 50 | 40,0% | Có ≥1 chi tiết cụ thể về sản phẩm |

- **Đối chiếu nhãn gốc trong cùng 50 mẫu:** `SpamLabel ≠ 0` chỉ bắt được **12/50 (24,0%)** — **bỏ sót 19 review** được gắn bình thường (`0`) nhưng thực tế chỉ khen chung chung / giao hàng / sai sản phẩm, và có 1 review nhãn `1` nhưng vẫn nêu chi tiết sử dụng (`dòng 3343`: dùng cho remote cửa cuốn cửa xếp). Điều này giải thích vì sao tỷ lệ 27,2% của nhãn spam gốc thấp hơn nhiều so với tỷ lệ thiếu thông tin chất lượng thực tế (60,0%).

## 4. ≥5 ví dụ cụ thể (dòng trong `test.csv`, không có tên người viết trong dataset)

1. Dòng 1665 · 5★ · nhãn 1: "Chất lượng sản phẩm tuyệt vời. Đóng gói sản phẩm chắc chắc." — cùng mẫu với dòng 3483, 1302, 1564.
2. Dòng 422 · 5★ · nhãn 3: "Nhanhhhhhhhh…" (kéo dài ~50 ký tự).
3. Dòng 3243 · 5★ · nhãn 2: "…chưa sử dụnh nên k biết chất lượng như thế nào".
4. Dòng 2855 · 5★ · nhãn 0: "Khá ok. Hài lòng" — nhãn gốc bình thường nhưng không có chi tiết sản phẩm.
5. Dòng 3260 · 5★ · nhãn 2: "hình ảnh đánh giá nhận xu thôi ạ nhưng đi 37 đặt 36 vẫn rộng quá" — nhãn gốc "chỉ nói shop" nhưng thực ra có thông tin size quan trọng.

## 5. Giới hạn của data

- Thu thập khoảng 2021–2022, chủ yếu Shopee / Tiki; chưa có TikTok Shop. Bộ v1 không có tên sản phẩm.
- Nhãn là của nhóm tác giả, không phải của nhóm mình; ví dụ 4 và 5 cho thấy định nghĩa lệch nhau.
- Data cho biết review **trông thế nào**, không cho biết người mua **có bị ảnh hưởng không**.

→ Kiểm lại bằng khảo sát ≥20 người mua ngoài nhóm (`evidence/survey/`): có đọc review không, từng mua phải hàng khác hẳn review 5★ không.
