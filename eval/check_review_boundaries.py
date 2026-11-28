"""Thử quy tắc nhãn bằng review dựng ngoài benchmark; gọi model đã cấu hình.

Chạy: python eval/check_review_boundaries.py
Thử prompt lưu lại: python eval/check_review_boundaries.py --prompt eval/prompts/run-2-system.txt
Đáp án được ghi trước khi gọi model. Không phải lượt đánh giá chính thức.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))

import agent
from ai import API_KEY, MODEL_NAME, MODEL_PROVIDER
from tracing import begin, end

CASES = [
    ("Thùng giấy bị ép ở góc, bên trong chưa mở kiểm.", "van_chuyen"),
    ("Chai hơi lõm khi nhận, chưa thấy rỉ, người giao tới sớm hơn hẹn.", "van_chuyen"),
    ("Vừa mở ra thấy ổn, hàng tốt, giao sớm, để dùng thêm mới rõ.", "khong_thong_tin"),
    ("Sử dụng được, sản phẩm xịn, đóng hộp đẹp.", "khong_thong_tin"),
    ("Nắp bình vặn kín vẫn rò ở ren khi để nghiêng.", "chat_luong"),
    ("Quạt chạy nấc thấp không rung, thổi liên tục hai giờ vẫn mát.", "chat_luong"),
    ("Đơn bị thiếu hai túi so với số lượng đặt.", "van_chuyen"),
    ("Shop trả lời nhanh, gói trong hai lớp xốp.", "van_chuyen"),
    ("Vải dày nhưng sợi vải xù ngay sau một lần giặt.", "chat_luong"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", type=Path, help="Đọc SYSTEM thử nghiệm từ file; không sửa agent.py")
    args = parser.parse_args()
    if args.prompt:
        agent.SYSTEM = args.prompt.read_text(encoding="utf-8-sig")
    if MODEL_PROVIDER == "fake" or not API_KEY:
        sys.exit("Cần model thật và key trong .env để kiểm chất lượng nhãn.")
    text = " ".join(f"[{i}] {review}" for i, (review, _) in enumerate(CASES, 1))
    begin("development-boundaries")
    result = agent.answer(text)
    summary, _ = end()
    labels = dict(re.findall(r"(\d+)=(\w+)", result["output"]))
    passed = 0
    for i, (_, expected) in enumerate(CASES, 1):
        actual = labels.get(str(i), "MISSING")
        passed += actual == expected
        print(f"[{i}] expected={expected}; actual={actual}")
    print(f"Model: {MODEL_NAME}; development labels: {passed}/{len(CASES)}")
    print(f"Tokens: {summary['tokens_in']} in / {summary['tokens_out']} out")
    return int(passed != len(CASES))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
