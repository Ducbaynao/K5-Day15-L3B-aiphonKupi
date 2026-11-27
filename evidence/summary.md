# Tổng hợp bằng chứng pain

> Đạt ngưỡng ở **2/3 nguồn** (Đào data + Khảo sát `n = 24`). Nhóm không thực hiện phỏng vấn riêng (`interviews/`), dùng khảo sát người dùng ngoài nhóm để kiểm chứng chéo với phân tích dataset.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | [x] | `evidence/data-mining.md` · `evidence/count_vispam.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | [ ] *(không làm)* | — |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | [x] (`n = 24`) | `evidence/survey/questions.md` · `evidence/survey/results.csv` |

## 2. Số chính

- **Đào data (ViSpamReviews v1 — `evidence/count_vispam.py`):**
  - Tổng dataset: **19.870** review thật trên sàn TMĐT Việt Nam; trong đó **18.543/19.870 (93,3%)** là review 5★.
  - Review 5★ có nhãn spam gốc (`SpamLabel ≠ 0`): **5.052/18.543 (27,2%)**, gồm:
    - Vô nghĩa / không liên quan (nhãn 3): **3.338/18.543 (18,0%)**
    - Chỉ nói shop / giao hàng / giá (nhãn 2): **1.440/18.543 (7,8%)**
    - Khen theo mẫu (nhãn 1): **274/18.543 (1,5%)**
  - So sánh với nhóm 1–3★: **99/802 (12,3%)** có nhãn spam gốc — tỷ lệ ở review 5★ cao gấp **~2,2 lần**.
  - **Gán lại mẫu 50 review 5★ theo 4 nhãn của nhóm (`evidence/sample50.py`):** **30/50 (60,0%)** thiếu thông tin chất lượng (`khong_thong_tin` 23/50 = 46,0% · `van_chuyen` 5/50 = 10,0% · `san_pham_khac` 2/50 = 4,0%); chỉ **20/50 (40,0%)** có chi tiết chất lượng (`chat_luong`). Trong cùng 50 mẫu đó, nhãn spam gốc chỉ bắt được **12/50 (24,0%)** (bỏ sót 19 review chỉ khen chung chung / giao hàng / sai sản phẩm).
- **Khảo sát (`n = 24` phiếu hợp lệ ngoài nhóm, chốt 17:45 ngày 27/11/2026 — `evidence/survey/results.csv`):**
  - **23/24 (95,8%)** có mua đơn ≥200.000đ/tháng (1–2 lần: 8 người · 3–5 lần: 9 người · >5 lần: 6 người).
  - **21/24 (87,5%)** đọc review trước khi đặt đơn ≥200k (**12/24 = 50,0%** luôn luôn đọc; **9/24 = 37,5%** thỉnh thoảng đọc).
  - **12/24 (50,0%)** mất từ 2 phút trở lên để lọc review chất lượng trong lần mua gần nhất (2–5 phút: 5 người · 5–10 phút: 5 người · >10 phút: 2 người).
  - **21/24 (87,5%)** gặp review 5★ không nói về chất lượng sản phẩm (**14/24 = 58,3%** rất thường xuyên / chiếm đa số; **7/24 = 29,2%** thỉnh thoảng).
  - **21/24 (87,5%)** từng mua phải sản phẩm kém chất lượng hoặc khác hẳn mô tả dù điểm đánh giá 4.8★–5.0★ (**11/24 = 45,8%** bị nhiều lần; **10/24 = 41,7%** bị 1–2 lần).
  - **Hậu quả khi mua nhầm (chọn nhiều):** **14/24 (58,3%)** ngại đổi trả nên giữ lại dùng tạm / bỏ đi (mất tiền oan); **9/24 (37,5%)** mất công làm thủ tục đổi/trả, hoàn tiền; **6/24 (25,0%)** mất thời gian nhắn tin khiếu nại với shop.

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

**Từ khảo sát người mua thật (`evidence/survey/results.csv`):**
1. *"Hôm trước mình định mua chai kem chống nắng 4.9★ nhưng lướt gần 50 cái đánh giá toàn thấy 'giao hàng nhanh, đóng gói kỹ, chưa dùng nhưng cho 5 sao lấy xu'. Cuối cùng mua về bôi bị vón cục và bí da, lúc quay lại lọc kỹ đánh giá 1–2★ mới thấy rất nhiều người bị y hệt."* — Phiếu khảo sát #5 (27/11/2026 17:24)
2. *"Mình mua cục sạc dự phòng thấy hơn nghìn lượt bán toàn khen 5★, nhưng dùng được khoảng 2 tuần thì sạc rất nóng và tụt pin nhanh. Đọc lại mới nhận ra đa số đánh giá đều viết ngay lúc vừa bóc hộp chứ gần như không ai quay lại cập nhật độ bền sau khi dùng."* — Phiếu khảo sát #7 (27/11/2026 17:25)
3. *"Định đặt cái áo khoác gió thấy lượt đánh giá cao ngất ngưởng, bấm vào xem ảnh thật thì toàn là ảnh áo thun với quần đùi từ năm ngoái. Hóa ra shop tráo sản phẩm mới vào link cũ có sẵn điểm cao, mất công ngồi lướt mãi mới phát hiện ra."* — Phiếu khảo sát #10 (27/11/2026 17:26)
4. *"Mua cái ốp điện thoại thấy toàn 5★ mà lướt xuống toàn lời bài hát với ảnh mèo lấy xu, chả biết chất lượng thật sao luôn."* — Phiếu khảo sát #21 (27/11/2026 17:35)
5. *"Hôm trước tính mua cái nồi chiên không dầu, thấy lượt bán cao nên định chốt nhưng ngồi kéo mãi không thấy ai đánh giá sau khi dùng 1–2 tháng xem lớp chống dính có bị bong không. Đọc mỏi mắt toàn thấy khen shipper thân thiện với đóng gói chắc chắn, cuối cùng nản quá tắt app khỏi mua luôn."* — Phiếu khảo sát #23 (27/11/2026 17:38)

**Từ dữ liệu thực tế ViSpamReviews v1 (`test.csv` trong `evidence/data-mining.md`):**
6. *"…chưa sử dụnh nên k biết chất lượng như thế nào"* — Dòng 3243 (`test.csv`, 5★, nhãn spam gốc 2)
7. *"Nhanhhhhhhhh…"* (kéo dài ~50 ký tự) — Dòng 422 (`test.csv`, 5★, nhãn spam gốc 3)
8. *"Chất lượng sản phẩm tuyệt vời. Đóng gói sản phẩm chắc chắc."* — Dòng 1665 (`test.csv`, 5★, nhãn spam gốc 1, lặp lại gần như nguyên văn ở nhiều dòng khác)

## 4. Các nguồn có khớp nhau không

- **Điểm khớp rõ rệt:**
  - Dữ liệu ViSpamReviews cho thấy phân bố sao lệch nặng về 5★ (93,3% tổng review) và review 5★ chứa tỷ lệ rác/không nói chất lượng cao gấp ~2,2 lần review 1–3★ (27,2% so với 12,3%). Điều này khớp với trải nghiệm thực tế của người dùng trong khảo sát: **21/24 (87,5%)** gặp review 5★ chỉ khen giao hàng/chưa dùng một cách thường xuyên hoặc thỉnh thoảng, và **21/24 (87,5%)** từng mua nhầm hàng kém dù điểm tổng rất cao (4.8★–5.0★).
  - Các kiểu review nhiễu thấy trong dataset (nhận xu bằng chữ vô nghĩa, khen theo mẫu, ghi "chưa sử dụng") xuất hiện y nguyên trong lời kể của người khảo sát (Phiếu #5, #21, #23).
- **Điểm lệch / bổ sung giữa hai nguồn:**
  - Nếu chỉ nhìn nhãn spam gốc ViSpamReviews (`27,2%`), tỷ lệ này thấp hơn cảm nhận của người dùng khảo sát (`58,3%` gặp rất thường xuyên). Khi gán lại đúng 50 mẫu ngẫu nhiên theo 4 nhãn của nhóm (`evidence/sample50.py`), tỷ lệ review 5★ thiếu thông tin chất lượng thực tế là **30/50 (60,0%)** — **khớp hoàn toàn** với trải nghiệm người dùng.
  - Khảo sát còn làm rõ thêm một dạng pain đặc thù là **shop tráo sản phẩm mới vào link cũ có sẵn nhiều đánh giá 5★** (Phiếu #10); khi kiểm lại trên mẫu 50 dòng ViSpamReviews v2 (có `product_name`), nhóm cũng gặp **2/50 (4,0%)** trường hợp `san_pham_khac` (vd dòng 3533: sản phẩm là *Hộp đựng giày* nhưng review nói về *giày đế cao*), khẳng định sự cần thiết của nhãn `san_pham_khac`.

## 5. Kết luận

- **Về giả thuyết ở `evidence/hypothesis.md`:** **ĐÚNG** — cả dữ liệu lẫn người dùng thật đều xác nhận giả thuyết CP1:
  - Trên mẫu ngẫu nhiên 50 review 5★ (`evidence/sample50.py`), **60,0% (30/50)** không chứa thông tin về chất lượng sản phẩm — vượt ngưỡng `≥40%` đặt ra ban đầu.
  - Trên khảo sát người mua (`n = 24`), **87,5% (21/24)** có đọc review trước khi đặt đơn ≥200k, **58,3% (14/24)** gặp review 5★ rỗng rất thường xuyên, **87,5% (21/24)** từng mua phải hàng kém/khác mô tả dù điểm 4.8★–5.0★ và **58,3% (14/24)** chấp nhận mất tiền oan vì ngại đổi trả.
- **Điều vẫn chưa biết:**
  1. Mức độ nghiêm trọng trên TikTok Shop hiện nay (vì ViSpamReviews thu thập giai đoạn 2021–2022 trên Shopee/Tiki).
  2. Mẫu khảo sát `n = 24` chủ yếu là người quen/học viên hay mua sắm online, chưa đại diện cho nhóm người dùng lớn tuổi hoặc ít mua TMĐT.
