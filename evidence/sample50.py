"""Lay mau ngau nhien 50 review 5 sao tu test.csv (seed=42) va so sanh nhan goc voi 4 nhan cua nhom."""
import csv
import os
import random
from collections import Counter

# Gan nhan theo dung 4 quy tac trong codebase/agent.py (doc cung product_name trong ViSpamReviews v2)
GROUP_LABELS = {
    30: "khong_thong_tin",
    114: "khong_thong_tin",
    121: "van_chuyen",
    138: "chat_luong",
    146: "chat_luong",
    383: "chat_luong",
    413: "van_chuyen",
    452: "van_chuyen",
    491: "khong_thong_tin",
    610: "khong_thong_tin",
    684: "van_chuyen",
    703: "khong_thong_tin",
    878: "khong_thong_tin",
    946: "chat_luong",
    963: "chat_luong",
    971: "chat_luong",
    983: "chat_luong",
    1023: "chat_luong",
    1076: "chat_luong",
    1208: "khong_thong_tin",
    1221: "khong_thong_tin",
    1222: "khong_thong_tin",
    1478: "chat_luong",
    1494: "chat_luong",
    1833: "khong_thong_tin",
    1843: "san_pham_khac",
    1847: "khong_thong_tin",
    1965: "chat_luong",
    2218: "khong_thong_tin",
    2394: "khong_thong_tin",
    2395: "chat_luong",
    2465: "khong_thong_tin",
    2584: "chat_luong",
    2589: "khong_thong_tin",
    2640: "chat_luong",
    2802: "khong_thong_tin",
    2846: "khong_thong_tin",
    2964: "khong_thong_tin",
    3057: "khong_thong_tin",
    3071: "khong_thong_tin",
    3139: "khong_thong_tin",
    3226: "chat_luong",
    3244: "khong_thong_tin",
    3250: "chat_luong",
    3323: "chat_luong",
    3343: "chat_luong",
    3533: "san_pham_khac",
    3548: "van_chuyen",
    3801: "khong_thong_tin",
    3899: "chat_luong",
}


def load_sample(test_csv_path):
    with open(test_csv_path, encoding="utf-8") as f:
        rows = [
            (i + 2, r)
            for i, r in enumerate(csv.DictReader(f))
            if (r.get("Rating") or r.get("rating", "")).strip() == "5"
        ]
    sample = random.Random(42).sample(rows, 50)
    sample.sort(key=lambda x: x[0])
    return sample


def main():
    p = os.path.join("data", "raw", "dataset", "test.csv")
    sample = load_sample(p)
    assert len(sample) == 50 and set(line for line, _ in sample) == set(GROUP_LABELS)

    by_group = Counter()
    by_spam = Counter()
    spam0_non_quality = 0
    spam_nz_quality = 0

    for line_no, r in sample:
        sp = (r.get("spam_label") or r.get("SpamLabel")).strip()
        gl = GROUP_LABELS[line_no]
        by_group[gl] += 1
        by_spam[sp != "0"] += 1
        if sp == "0" and gl != "chat_luong":
            spam0_non_quality += 1
        if sp != "0" and gl == "chat_luong":
            spam_nz_quality += 1

    non_quality = 50 - by_group["chat_luong"]
    print(f"Mau 50 review 5*: thieu thong tin chat luong (!= chat_luong) = {non_quality}/50 ({100*non_quality/50:.1f}%)")
    for k in ("chat_luong", "khong_thong_tin", "van_chuyen", "san_pham_khac"):
        print(f"  {k}: {by_group[k]}/50 ({100*by_group[k]/50:.1f}%)")
    print(f"Nhan goc SpamLabel != 0 trong mau 50: {by_spam[True]}/50 ({100*by_spam[True]/50:.1f}%)")
    print(f"Do lech: SpamLabel==0 nhung khong co thong tin chat luong = {spam0_non_quality}; SpamLabel!=0 nhung van co chat_luong = {spam_nz_quality}")


if __name__ == "__main__":
    main()
