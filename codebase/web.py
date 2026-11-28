"""Giao diện web cho bản chạy thử — chỉ dùng thư viện chuẩn của Python.

Chạy:  python codebase/web.py          (tự mở trình duyệt ở http://127.0.0.1:8000)
       python codebase/web.py 8080     (chọn cổng khác)
       python codebase/web.py --no-browser   (không tự mở trình duyệt)

Trang gọi ĐÚNG luồng answer() trong agent.py mà bộ eval chấm, với model thật trong .env.
Bản dòng lệnh `python run.py` vẫn giữ nguyên.
"""
import json
import os
import re
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ai  # noqa: E402
import tracing  # noqa: E402
from agent import answer  # noqa: E402

PAGE = os.path.join(HERE, "web", "index.html")
_LOCK = threading.Lock()   # tracing giữ trạng thái chung → mỗi lúc chỉ phân tích một yêu cầu
_STAR = re.compile(r"^\s*([1-5])\s*(?:★|sao|\*)\s*(.*)$", re.I | re.S)


def compose_text(product: str, question: str, lines: list) -> str:
    """Ghép ô nhập của trang thành định dạng parse_reviews đọc được:
    "Sản phẩm: <tên> || <câu hỏi> || [1] 5★ <review> [2] <review> ..."."""
    parts = []
    if (product or "").strip():
        parts.append("Sản phẩm: %s" % product.strip())
    if (question or "").strip():
        parts.append(question.strip())
    items = []
    for line in lines or []:
        line = " ".join(str(line).split())
        m = _STAR.match(line)
        stars, body = (m.group(1), m.group(2).strip()) if m else (None, line)
        body = body.replace("[", "(").replace("]", ")")   # không để nội dung bị tách nhầm thành review mới
        if not body:
            continue
        items.append("[%d] %s%s" % (len(items) + 1, stars + "★ " if stars else "", body))
    if not items:
        return ""
    return " || ".join(parts + [" ".join(items)])


def status() -> dict:
    fake = ai.MODEL_PROVIDER == "fake"
    return {"mode": "fake" if fake else "real", "model": "chế độ giả" if fake else (ai.MODEL_NAME or ai.MODEL_PROVIDER)}


def analyze(payload: dict) -> tuple:
    """→ (mã HTTP, JSON). Không bao giờ trả traceback hay nội dung lỗi thô (có thể chứa key)."""
    lines = payload.get("reviews") or []
    if isinstance(lines, str):
        lines = lines.splitlines()
    text = compose_text(payload.get("product", ""), payload.get("question", ""), lines)
    if not text:
        return 400, {"error": "Bạn chưa dán review nào. Mỗi review một dòng."}
    with _LOCK:
        tracing.begin("web")
        t0 = time.perf_counter()
        try:
            res = answer(text)
        except Exception as e:  # mạng, key sai, hết lượt, chưa nối model…
            tracing.end()
            print("[web] lỗi gọi AI: %s" % type(e).__name__)
            return 502, {"error": "Không gọi được AI (%s). Kiểm tra mạng và API_KEY trong .env rồi thử lại."
                                  % type(e).__name__}
        s, _ = tracing.end()
    return 200, {"input": text, "output": res.get("output", ""), "detail": res.get("detail", {}),
                 "mode": status()["mode"],
                 "trace": {"model": ", ".join(s["models"]) or "—", "model_calls": s["model_calls"],
                           "tokens_in": s["tokens_in"], "tokens_out": s["tokens_out"],
                           "seconds": round(time.perf_counter() - t0, 1)}}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(PAGE, "rb") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        elif self.path == "/api/status":
            self._send(200, status())
        else:
            self._send(404, {"error": "không có trang này"})

    def do_POST(self):
        if self.path != "/api/analyze":
            return self._send(404, {"error": "không có trang này"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            return self._send(400, {"error": "Dữ liệu gửi lên không hợp lệ."})
        self._send(*analyze(payload))

    def log_message(self, fmt, *args):  # gọn terminal khi quay video
        pass


def make_server(port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(port: int = 8000, open_browser: bool = True) -> int:
    srv = None
    for p in range(port, port + 11):
        try:
            srv = make_server(p)
            break
        except OSError:
            continue
    if srv is None:
        print("Không mở được cổng %d–%d. Thử: python codebase/web.py <cổng khác>" % (port, port + 10))
        return 1
    url = "http://127.0.0.1:%d" % srv.server_address[1]
    st = status()
    print("ReviewLọc đang chạy ở %s  ·  AI: %s" % (url, st["model"]))
    if st["mode"] == "fake":
        print("Chưa nối model (chế độ giả) — điền MODEL_PROVIDER, MODEL_NAME, API_KEY trong .env.")
    print("Dừng: Ctrl+C")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--no-browser"]
    sys.exit(main(int(args[0]) if args else 8000, "--no-browser" not in sys.argv))
