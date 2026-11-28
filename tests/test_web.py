"""Server giao diện web (codebase/web.py). Chạy: python -m unittest discover -s tests -v"""
import json
import os
import sys
import threading
import unittest
import urllib.request
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "codebase"))
import agent  # noqa: E402
import tools  # noqa: E402
import web  # noqa: E402

LABELS = json.dumps({"labels": [{"id": 1, "label": "chat_luong", "sentiment": "tot", "quote": "Sáng"}]})


def fake_model(system, user):
    return {"text": LABELS, "model": "m", "tokens_in": 10, "tokens_out": 5}


class ComposeTest(unittest.TestCase):
    def test_lines_and_stars(self):
        got = web.compose_text("Nồi chiên", "", ["5★ Nồi to", "", "4 sao Giao nhanh", "Hàng đẹp",
                                                 "3* lòng [1] nhỏ", "  5★  ", "   "])
        self.assertEqual(got, "Sản phẩm: Nồi chiên || [1] 5★ Nồi to [2] 4★ Giao nhanh [3] Hàng đẹp [4] 3★ lòng (1) nhỏ")
        parsed = tools.parse_reviews(got)
        self.assertEqual(parsed["product"], "Nồi chiên")
        self.assertEqual([r["stars"] for r in parsed["reviews"]], [5, 4, None, 3])

    def test_question_keeps_product(self):
        got = web.compose_text("Đèn", "Có nên mua không?", ["5★ Sáng"])
        self.assertEqual(got, "Sản phẩm: Đèn || Có nên mua không? || [1] 5★ Sáng")
        self.assertEqual(tools.parse_reviews(got)["product"], "Đèn")
        self.assertEqual(len(agent._scope_notes(got)), 1)

    def test_no_product(self):
        self.assertEqual(web.compose_text("", "", ["Tốt"]), "[1] Tốt")


class AnalyzeTest(unittest.TestCase):
    def test_empty_reviews(self):
        code, body = web.analyze({"product": "x", "reviews": ["", "  "]})
        self.assertEqual(code, 400)
        self.assertIn("error", body)

    def test_model_error_hides_details(self):
        with mock.patch.object(web, "answer", side_effect=RuntimeError("key sk-abc")):
            code, body = web.analyze({"product": "x", "reviews": ["5★ Tốt"]})
        self.assertEqual(code, 502)
        self.assertNotIn("sk-abc", json.dumps(body))

    def test_ok_has_trace(self):
        with mock.patch.object(agent, "call_model", fake_model):
            code, body = web.analyze({"product": "Đèn", "reviews": ["5★ Sáng"]})
        self.assertEqual(code, 200)
        self.assertEqual(body["detail"]["reviews"][0]["quote"], "Sáng")
        self.assertEqual(body["trace"]["tokens_in"], 0)  # call_model bị thay → không qua @model_call
        self.assertIn("seconds", body["trace"])


class ServerTest(unittest.TestCase):
    def test_routes(self):
        srv = web.make_server(0)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = "http://127.0.0.1:%d" % srv.server_address[1]
        try:
            with urllib.request.urlopen(base + "/") as r:
                self.assertEqual(r.status, 200)
                self.assertIn("ReviewLọc", r.read().decode("utf-8"))
            with urllib.request.urlopen(base + "/api/status") as r:
                self.assertIn("mode", json.loads(r.read()))
            req = urllib.request.Request(base + "/api/analyze", method="POST",
                                         data=json.dumps({"product": "Đèn", "reviews": ["5★ Sáng"]}).encode(),
                                         headers={"Content-Type": "application/json"})
            with mock.patch.object(agent, "call_model", fake_model), urllib.request.urlopen(req) as r:
                self.assertEqual(json.loads(r.read())["detail"]["product"], "Đèn")
        finally:
            srv.shutdown()
            srv.server_close()


if __name__ == "__main__":
    unittest.main()
