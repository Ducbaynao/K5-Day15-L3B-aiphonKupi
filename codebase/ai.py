"""Nối model — chỗ DUY NHẤT gọi model AI. Hợp đồng: call_model(system, user) -> {"text","model","tokens_in","tokens_out"}.
Token lấy từ trường usage của API, không ước lượng. .env: MODEL_PROVIDER = fake | gemini | openai | anthropic.
Chế độ giả (fake): gán mọi review là khong_thong_tin để luồng chạy hết — KHÔNG phải kết quả thật, không tính vào eval.
"""
import json
import os
import re
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
SHOW_RAW = False   # True: in nguyên phản hồi API khi cần tìm tên trường


def post_json(url, headers, body, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def _fake(user):
    """CHẾ ĐỘ GIẢ: gán mọi review là khong_thong_tin — chỉ để luồng chạy hết, KHÔNG phải kết quả thật."""
    ids = [int(i) for i in re.findall(r"^\[(\d+)\]", user, flags=re.M)]
    labels = [{"id": i, "label": "khong_thong_tin", "sentiment": None, "quote": ""} for i in ids]
    return json.dumps({"labels": labels}, ensure_ascii=False)


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        return {"text": _fake(user), "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER == "gemini":
        r = call_gemini(system, user)
    elif MODEL_PROVIDER == "openai":
        r = call_openai(system, user)
    elif MODEL_PROVIDER == "anthropic":
        r = call_claude(system, user)
    else:
        raise NotImplementedError("MODEL_PROVIDER=%s chưa hỗ trợ — dùng gemini / openai / anthropic" % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME, "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}


def call_gemini(system, user):
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME
    data = post_json(url, {"x-goog-api-key": API_KEY}, {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"}})
    parts = data["candidates"][0]["content"]["parts"]
    u = data.get("usageMetadata", {})
    return {"text": "".join(p.get("text", "") for p in parts),
            "tokens_in": u.get("promptTokenCount", 0),
            "tokens_out": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)}


def call_openai(system, user):
    data = post_json("https://api.openai.com/v1/chat/completions", {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "response_format": {"type": "json_object"},
                      "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"],
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


def call_claude(system, user):
    data = post_json("https://api.anthropic.com/v1/messages",
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 2048, "system": system,
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}
