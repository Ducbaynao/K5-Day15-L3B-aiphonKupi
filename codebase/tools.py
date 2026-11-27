"""Công cụ của bài toán — lọc review sản phẩm trên sàn. Khớp bảng công cụ ở spec.md §4.

Mọi công cụ ở đây CHẠY BẰNG CODE, không gọi AI, và KHÔNG tác động ra ngoài (chỉ đọc / tính trên đầu vào).
Quyết định AI duy nhất (gán nhãn từng review) nằm ở agent.py → ai.call_model.
"""
import re
import unicodedata

from tracing import tool, TOOLS  # noqa: F401

LABELS = ["chat_luong", "van_chuyen", "khong_thong_tin", "san_pham_khac"]
SENTIMENTS = ["tot", "xau", "trung_tinh"]
MIN_INFORMATIVE = 3   # G10: dưới ngưỡng này thì không chấm điểm


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


@tool
def parse_reviews(text: str) -> dict:
    """parse_reviews · Input: đoạn người dùng dán (str), dạng
        "Sản phẩm: <tên> || [1] 5★ <review> [2] 4★ <review> ..."
    Output: {"product": str, "reviews": [{"id": int, "stars": int|None, "text": str}]}.
    Không tác động ra ngoài."""
    text = unicodedata.normalize("NFC", text or "")
    product = ""
    m = re.match(r"\s*s[ảa]n ph[ẩa]m\s*:\s*(.*?)\s*\|\|", text, flags=re.I)
    if m:
        product = m.group(1).strip()
        text = text[m.end():]
    reviews = []
    for m in re.finditer(r"\[(\d+)\]\s*(?:(\d)\s*(?:★|sao|\*))?\s*(.*?)(?=\s*\[\d+\]|$)", text, flags=re.S):
        body = m.group(3).strip()
        if body:
            reviews.append({"id": int(m.group(1)), "stars": int(m.group(2)) if m.group(2) else None, "text": body})
    return {"product": product, "reviews": reviews}


@tool
def find_duplicates(reviews: list) -> dict:
    """find_duplicates · Input: danh sách review. Output: {id_bị_trùng: id_gốc} cho review trùng nguyên văn
    (sau khi bỏ dấu câu, chữ hoa). Review trùng chỉ tính 1 lần. Không tác động ra ngoài."""
    seen, dup = {}, {}
    for r in reviews:
        key = _norm(r["text"])
        if key in seen:
            dup[r["id"]] = seen[key]
        else:
            seen[key] = r["id"]
    return dup


@tool
def verify_quote(quote: str, review_text: str) -> bool:
    """verify_quote · Input: trích dẫn AI đưa ra, nội dung review gốc. Output: True nếu trích dẫn có nguyên văn
    trong review (bỏ qua dấu câu, chữ hoa). Chặn trích dẫn bịa. Không tác động ra ngoài."""
    q = _norm(quote)
    return bool(q) and q in _norm(review_text)


@tool
def compute_score(labels: list, duplicates: dict) -> dict:
    """compute_score · Input: nhãn AI gán [{"id", "label", "sentiment"}], bản đồ review trùng.
    Output: {"informative": n, "positive": k, "negative": j, "enough": bool, "counts": {...}}.
    Điểm chất lượng = k/n review CÓ thông tin chất lượng là tích cực — tính bằng code, AI không tự cộng.
    Không tác động ra ngoài."""
    counts = {l: 0 for l in LABELS}
    pos = neg = 0
    for x in labels:
        if x["id"] in duplicates:
            continue
        counts[x["label"]] = counts.get(x["label"], 0) + 1
        if x["label"] == "chat_luong":
            pos += x.get("sentiment") == "tot"
            neg += x.get("sentiment") == "xau"
    n = counts["chat_luong"]
    return {"informative": n, "positive": pos, "negative": neg,
            "enough": n >= MIN_INFORMATIVE, "counts": counts}
