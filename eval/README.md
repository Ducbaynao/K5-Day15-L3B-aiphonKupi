# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Dataset nào, xử lý gì: tóm 2–3 dòng từ `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: __ câu (thuong __ · kho __ · tu_choi __, trong đó __ câu tấn công)
- Nguồn (`python run.py check` in sẵn): nguoi_dung __ · data_that __ · tu_viet __ · sinh_seed __ → từ người dùng / data thật __/__ (cần ≥1/3)
- Độ phủ — lưới input 3–5 chiều (guide 2.4 bước 5): __
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1: __ · lớp 2: __ · lớp 3: __ · lớp 4: __

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| | code / llm / nguoi | |
| | | |
| | | |

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): đã kiểm tay __ câu, khớp __/__
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "__"

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | run-1@20261128-085253 | gpt-6-luna | Workflow lọc review; cấu hình đã dùng được ghi trong traces/run-1.jsonl; 29 câu, 0 lỗi kỹ thuật | 28/29 | 96,6% (score làm tròn 97%) | Đạt ngưỡng tổng ≥80%; chưa tổng hợp đủ kết quả từng metric |
| 2 | Chưa chạy | — | Chưa thực hiện cải tiến sau lượt 1 | — | — | Chưa đánh giá |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

- Lượt 1: thường 8/8 (100%), khó 14/15 (93,3%), từ chối 6/6 (100%). Chỉ R16 không đạt: đúng 3/5 nhãn và điểm 1/4 thay vì 1/3.
- R07 sai một nhãn nhưng vẫn đạt ngưỡng 4/5; R18 khác cảm xúc review 5 so với expected nhưng vẫn đạt pass_criterion. Chi tiết: [report.md](report.md), cột `ghi_chu` trong [run-1.csv](run-1.csv).
- Chưa cải tiến hoặc chạy lượt 2. AI hỗ trợ chấm lượt 1 bằng đối chiếu dữ liệu và đọc hành vi; chưa có kết quả người thứ hai chấm độc lập. Không thay đổi output, expected, metric hoặc chuẩn đạt.
