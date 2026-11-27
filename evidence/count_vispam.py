"""Đếm bằng chứng pain từ ViSpamReviews (Van Dinh, Luu & Nguyen, 2022 — arXiv 2207.14636).

Câu hỏi: trong review 5★ trên sàn TMĐT Việt Nam, bao nhiêu review KHÔNG cho người mua thông tin về sản phẩm?
Quy tắc đếm (ghi trước khi chạy):
  - Mẫu: mọi review có Rating = 5 trong cả 3 file train / dev / test.
  - "Không cho thông tin về sản phẩm" = SpamLabel ≠ 0 (nhãn gốc của nhóm tác giả):
      1 = review giả (khen theo mẫu) · 2 = chỉ nói shop / giao hàng / giá · 3 = không liên quan, vô nghĩa.
  - Không tự gán lại nhãn ở bước này.

Dataset KHÔNG commit vào repo (dùng cho nghiên cứu, repo nhóm công khai). Tải từ
https://github.com/sonlam1102/vispamdetection → dataset/vispamdetection_dataset.zip, giải nén ra ngoài repo.

Chạy: python evidence/count_vispam.py <thư mục chứa train.csv, dev.csv, test.csv>
"""
import csv
import os
import sys
from collections import Counter

NAMES = {"0": "bình thường", "1": "review giả (khen theo mẫu)", "2": "chỉ nói shop / giao hàng / giá",
         "3": "không liên quan / vô nghĩa"}


def main(folder):
    rows = []
    for name in ("train.csv", "dev.csv", "test.csv"):
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            rows += list(csv.DictReader(f))
    five = [r for r in rows if r["Rating"].strip() == "5"]
    c = Counter(r["SpamLabel"] for r in five)
    spam = sum(v for k, v in c.items() if k != "0")
    print("Tổng review: %d · review 5★: %d" % (len(rows), len(five)))
    print("Review 5★ không cho thông tin về sản phẩm: %d/%d = %.1f%%" % (spam, len(five), 100 * spam / len(five)))
    for k in sorted(c):
        print("  SpamLabel %s (%s): %d (%.1f%%)" % (k, NAMES.get(k, "?"), c[k], 100 * c[k] / len(five)))
    by_star = Counter((r["Rating"].strip(), r["SpamLabel"] != "0") for r in rows)
    print("Tỉ lệ spam theo số sao:")
    for s in "12345":
        n = by_star[(s, True)] + by_star[(s, False)]
        if n:
            print("  %s★: %d/%d = %.1f%%" % (s, by_star[(s, True)], n, 100 * by_star[(s, True)] / n))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
