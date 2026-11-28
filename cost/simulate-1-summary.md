# Tóm tắt mô phỏng simulate-1@20261128-103718

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| nguoi_mua_it | 18 | 1 | 643 | 322 | 0.9 | 7.5 |
| nguoi_mua_vua | 17 | 1 | 643 | 338 | 0.9 | 7.4 |
| nguoi_mua_nhieu | 15 | 1 | 562 | 368 | 0.8 | 6.5 |

Tỉ lệ đạt dùng để tính: 28/29 (97%) — lượt run-1@20261128-085253

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-1.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (6 người) | Chi phí / tháng — cơ sở (12 người) | Chi phí / tháng — cao (24 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.00023 | $0.00024 | $0.00024 | $0.0049 | $0.0098 | $0.0197 | $0.00082 |
| gpt-6.2-sol (vào 2.0 · ra 10.0 $/1M) | $0.0046 | $0.0048 | $0.0048 | $0.0983 | $0.1966 | $0.3933 | $0.0164 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
