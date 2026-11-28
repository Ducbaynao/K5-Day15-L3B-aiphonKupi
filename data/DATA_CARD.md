# Data card — aiphonKupi · CP3

> Cập nhật 28/11/2026. Phân biệt dữ liệu bằng chứng, bộ câu thử và đầu ra model. Không commit nguyên dataset trong `data/raw/` hoặc `.env`.

## 1. ViSpamReviews v1 — nguồn review và nhãn gốc

| Thuộc tính | Nội dung |
|---|---|
| Nguồn trong hồ sơ | Van Dinh, Luu & Nguyen (2022), Detecting Spam Reviews on Vietnamese E-commerce Websites; [bài báo](https://arxiv.org/abs/2207.14636), [repo nguồn](https://github.com/sonlam1102/vispamdetection). Nhóm ghi ngày xem 27/11/2026 |
| Mục đích | Đếm nhãn spam gốc, trích review vào benchmark. Không dùng nhãn spam gốc làm đáp án tự động cho bốn nhãn sản phẩm |
| Bản hiện có | `data/raw/dataset/train.csv`, `dev.csv`, `test.csv`; cột `Rating, Comment, Label, SpamLabel`, không có `product_name` |
| Quy mô kiểm lại | Train 14.306, dev 1.590, test 3.974; tổng **19.870 review**, trong đó **18.543 review 5★** |
| Kết quả đếm | **5.052/18.543 (27,2%)** review 5★ có SpamLabel ≠ 0; nhóm 1–3★: **99/802 (12,3%)**. Không đồng nhất nhãn spam với thiếu thông tin chất lượng theo định nghĩa của nhóm |
| Xử lý | Giữ nguyên file gốc ngoài Git; trích review cần thiết, ghi số dòng/nhãn gốc trong source. Không gửi nhãn gốc vào model. Một số câu ghép review của nhiều sản phẩm vì v1 thiếu tên sản phẩm |
| Nhãn gốc | SpamLabel: 0 bình thường, 1 khen theo mẫu, 2 shop/giao hàng/giá, 3 không liên quan theo mô tả nguồn của nhóm. Không phải kết luận của sản phẩm về tính xác thực của từng review |
| Quyền sử dụng | Hồ sơ CP2 ghi dùng cho nghiên cứu; cần đối chiếu điều khoản tác giả trước khi phân phối lại/dùng thương mại. Repo nhóm chỉ lưu trích đoạn và số tổng hợp |
| Giới hạn | Hồ sơ ghi thu khoảng 2021–2022, chủ yếu Shopee/Tiki; chưa xác nhận tính đại diện với thị trường hiện tại. Review không tự chứng minh tác động lên quyết định mua |

Tái lập: `python evidence/count_vispam.py data/raw/dataset`.

SHA-256 của bản v1 kiểm tại CP3 (nhận diện đúng file, không phải bằng chứng quyền sử dụng):

| File | SHA-256 |
|---|---|
| train.csv | `9722b5e2f13eb6acf327bb695f3f8795472983f1676884a784c8904af3e5fa64` |
| dev.csv | `7f73e46c885151409e428747343b7c81dbf081e003d4c00afaeee1012224b841` |
| test.csv | `d801f9bddfd8ef5b000ec8a875e7a2c0211fe8f3296b2cb22e9f013a196e6bd1` |

## 2. Mẫu 50 gán lại — chưa tái lập trên đúng phiên bản

- `evidence/sample50.py` lưu nhãn theo mã dòng trong GROUP_LABELS, chọn 50 review 5★ với seed = 42. Bảng nhãn có 20 chat_luong, 23 khong_thong_tin, 5 van_chuyen, 2 san_pham_khac; 30/50 không phải chat_luong.
- `evidence/data-mining.md` ghi dùng **ViSpamReviews v2 có product_name**. File hiện có là v1, không có cột này.
- Kiểm CP3: `python evidence/sample50.py` dừng bằng **AssertionError** vì mã dòng lấy mẫu không khớp bảng nhãn. Chưa xác nhận nhãn gắn đúng review hoặc trường hợp sản phẩm khác loại trên đúng nguồn.
- **60,0% là số trong báo cáo/bảng nhãn, chưa phải kết quả đã tái lập.** Cần đúng file v2, phiên bản/hash và người kiểm nhãn trước khi dùng để xác nhận giả thuyết ≥40%. Không sửa nhãn/số nguồn để ép phép kiểm chạy qua.

## 3. Bộ câu thử CP3 — eval/benchmark.csv

| Thuộc tính | Nội dung |
|---|---|
| Quy mô / phiên bản | **29 câu**: 8 thuong, 15 kho, 6 tu_choi; CP3 ngày 28/11/2026, giữ 14 câu CP2 và bổ sung 15 câu |
| Cấu trúc | id, input, expected, pass_criterion, type, source; một dòng là một tình huống có thể gồm nhiều review |
| Nguồn theo source | **19 data_that (65,5%)**, **10 tu_viet**; 0 nguoi_dung, 0 sinh_seed. B14 thuộc tu_viet nhưng dùng trích đoạn thật; B16 thuộc data_that nhưng tên sản phẩm được nhóm đặt để dựng tình huống |
| Đầu vào | **128 lượt review được đánh số**, có lặp; không phải 128 review độc lập hoặc 128 người dùng |
| Câu data_that | R01–R18 và B16 |
| Câu tu_viet | B03, B07, B08, B10, B11, B12, B13, B14, B15, B17 |
| Expected | Bốn nhãn chat_luong, van_chuyen, khong_thong_tin, san_pham_khac; cảm xúc tot, xau, trung_tinh. Do nhóm đặt theo quy tắc sản phẩm, khác nhãn spam gốc. Chưa có kết quả người thứ hai kiểm độc lập nhãn |
| Xử lý lúc chạy | Tách ID/sao/nội dung; đánh dấu trùng sau chuẩn hoá; model gán nhãn/cảm xúc/trích dẫn; code kiểm trích dẫn và tính k/n. Chỉ chat_luong không trùng vào mẫu số; cần ≥3 căn cứ để xuất điểm |
| Độ phủ | Khen chung chung, vận chuyển, chi tiết chất lượng, thiếu căn cứ, sản phẩm khác, trùng, mỉa mai, không dấu, cảm xúc lệch số sao, yêu cầu ngoài thẩm quyền/chèn lệnh |
| Dữ liệu dựng | Chỉ dùng kiểm tình huống, không phải bằng chứng pain; viết tay nên không có seed sinh tự động |
| Giới hạn | Một số đầu vào ghép review khác sản phẩm hoặc thiếu tên, chưa đại diện luồng thực một sản phẩm. Benchmark đã được xem khi xây prompt, không phải holdout độc lập. Không suy rộng 29 câu thành độ chính xác thị trường |

Kiểm bằng `python run.py check`. Giữ nguyên metric/chuẩn đạt CP2; không xoá câu trượt hoặc sửa expected để khớp output.

## 4. Khảo sát người mua — evidence/survey/results.csv

- **Mục đích:** kiểm pain và hành vi tự báo cáo; không gửi khảo sát vào model hoặc dùng làm câu thử lượt 1.
- **Nguồn theo khai báo nhóm:** Google Form gửi người quen/người mua ngoài nhóm; đóng 17:45 ngày 27/11/2026, 24 phiếu. Câu hỏi: `evidence/survey/questions.md`. Có CSV để kiểm phép đếm, chưa kiểm Form gốc độc lập.
- **Cấu trúc:** dấu thời gian và 7 câu hỏi; không có cột tên/email/số điện thoại trong file cung cấp. Không thể xác minh độc lập người ngoài nhóm chỉ từ bản ẩn danh.
- **Số kiểm lại:** 21/24 có đọc review, 12/24 mất ≥2 phút lọc review; 14/24 gặp review thiếu thông tin rất thường xuyên, thêm 7/24 thỉnh thoảng; 21/24 từng mua hàng kém/khác mô tả dù sao cao.
- **Lỗi/giới hạn nguồn:** một phiếu chọn đồng thời "Chưa từng gặp" và hậu quả mua nhầm. Lựa chọn >5 lần/tháng có hậu tố nhập liệu `tháng3` ở 6 phiếu; đọc theo nhãn >5 trong hồ sơ, không sửa CSV. Câu hậu quả chọn nhiều nên tỷ lệ không cộng thành 100%.
- **Giới hạn suy luận:** mẫu thuận tiện n=24, hồi tưởng, chưa đại diện thị trường; chưa đo thời gian tiết kiệm sau dùng hoặc chứng minh review gây mua nhầm. Impact tự ước tính ghi riêng ở spec §2. Kiểm trường tự do để ẩn danh trước khi chia sẻ thêm.

## 5. Đầu ra đánh giá và bảo toàn kết quả

- **Lượt 1:** `eval/run-1.csv`, `traces/run-1.jsonl`; run ID **run-1@20261128-085253**, model OpenAI **gpt-6-luna**.
- **Quy mô:** 29/29 chạy xong, 0 lỗi kỹ thuật; tổng token API ghi nhận **18.550 vào / 9.075 ra**. Câu xử lý trực tiếp bằng code có thể không gọi model.
- **Chấm:** AI hỗ trợ đối chiếu dữ liệu và đọc hành vi; **28/29 đạt (96,6%)**, thường 8/8, khó 14/15, từ chối 6/6. Chưa có người thứ hai chấm độc lập. 67/67 trích dẫn khớp nguồn sau chuẩn hoá.
- **Sai khác lượt 1:** R16 không đạt; R07 và R18 khác expected nhưng vẫn đạt pass_criterion, đã ghi trong ghi_chu. Chi tiết `eval/report.md`; chưa tổng hợp đủ bốn metric.
- **Lượt 2 (CP4):** `run-2@20261128-102256`, model gpt-6-luna, 0 lỗi kỹ thuật; 27/29 đạt (93,1%), R16/R17 không đạt; token 22.681 vào / 9.356 ra. Chỉ điền pass/ghi_chu. Prompt thử nghiệm lưu ở `eval/prompts/run-2-system.txt`; kết quả giảm nên đã khôi phục prompt đang dùng về bản lượt 1. Giữ nguyên cả hai lượt và trace tương ứng.
- **Bảo toàn:** không sửa input, expected, output, token, run ID hoặc trace đã chạy; chỉ điền pass/ghi_chu. Chạy lại tạo lượt mới. Không lưu key trong kết quả hoặc quay .env trong video.

## 6. Dữ liệu mô phỏng chi phí CP4

- **simulate-1@20261128-103718:** 50 phiên/0 lỗi, đo prompt đang dùng của lượt 1, rate 28/29; giữ CSV, summary và trace làm lịch sử.
- **simulate-2@20261128-110412 — dùng báo cáo form CP4:** 50 phiên/0 lỗi, một lượt/phiên, seed 42, 45 lần gọi OpenAI gpt-6-luna; 37.819 token vào / 15.961 ra. Dùng đúng prompt thử nghiệm `eval/prompts/run-2-system.txt` trong tiến trình riêng và rate 27/29 của lượt 2; không thay agent.py đang dùng.
- Nguồn: `cost/simulate-2.csv`, `cost/simulate-2-summary.md`, `traces/simulate-2.jsonl`. Các phiên lấy mẫu có lặp từ benchmark, không phải 50 người dùng thật hoặc 50 tình huống độc lập mới. Năm phiên không gọi model có token 0, không phải lỗi.
- Luna khoảng $0,00025/task thành công và $0,0097/tháng cho cơ sở giả định 12 người; Sol chỉ quy đổi giá trên token Luna. Chưa chấm riêng 50 output mô phỏng; tỷ lệ thành công lấy từ benchmark. Chi tiết giả định, nguồn giá và giới hạn ở `cost/cost-estimate.md`.
- Không sửa CSV, summary hoặc trace đã sinh, không gộp hai lượt thành một mẫu 100 phiên. Chỉ bổ sung diễn giải trong tài liệu.
