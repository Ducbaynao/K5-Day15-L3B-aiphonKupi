"""answer() trả thêm "detail" cho giao diện web; "output" (eval chấm) phải giữ nguyên từng ký tự.

Chạy: python -m unittest discover -s tests -v
Golden output dưới đây chụp từ agent.py TRƯỚC khi thêm detail (cùng model giả lập).
"""
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "codebase"))
import agent  # noqa: E402

B07 = ("Sản phẩm: Giày chạy bộ || [1] 5★ Giày êm, chạy 10km không đau chân [2] 5★ Giày êm, chạy 10km không đau chân! "
       "[3] 5★ Giày êm chạy 10km không đau chân [4] 2★ Đế mòn sau 1 tháng, keo bung mũi [5] 4★ Nhẹ, thoáng chân")
LABELS = {"labels": [
    {"id": 1, "label": "chat_luong", "sentiment": "tot", "quote": "Giày êm, chạy 10km không đau chân"},
    {"id": 2, "label": "chat_luong", "sentiment": "tot", "quote": "Giày êm"},
    {"id": 3, "label": "chat_luong", "sentiment": "tot", "quote": "không đau chân"},
    {"id": 4, "label": "chat_luong", "sentiment": "xau", "quote": "Đế mòn sau 1 tháng"},
    {"id": 5, "label": "chat_luong", "sentiment": "tot", "quote": "siêu bền 5 năm"},   # trích dẫn bịa
]}
GOLDEN_B07 = ('NHÃN: 1=chat_luong 2=chat_luong 3=chat_luong 4=chat_luong 5=chat_luong\n'
              'Trùng nguyên văn (chỉ tính 1 lần): [2]=[1], [3]=[1]\n'
              'Có thông tin chất lượng: 3 · chỉ vận chuyển: 0 · không có thông tin: 0 · sản phẩm khác: 0\n'
              'ĐIỂM CHẤT LƯỢNG: 2/3 review có thông tin là tích cực (1 tiêu cực)\n'
              '  [1] (tot) "Giày êm, chạy 10km không đau chân"\n'
              '  [4] (xau) "Đế mòn sau 1 tháng"')


def fake_model(text):
    return lambda system, user: {"text": text, "model": "m", "tokens_in": 1, "tokens_out": 1}


class DetailTest(unittest.TestCase):
    def test_output_unchanged_and_detail(self):
        with mock.patch.object(agent, "call_model", fake_model(json.dumps(LABELS, ensure_ascii=False))):
            res = agent.answer(B07)
        self.assertEqual(res["output"], GOLDEN_B07)
        d = res["detail"]
        self.assertEqual(d["product"], "Giày chạy bộ")
        self.assertEqual(len(d["reviews"]), 5)
        by = {r["id"]: r for r in d["reviews"]}
        self.assertEqual(by[2]["duplicate_of"], 1)
        self.assertEqual(by[3]["duplicate_of"], 1)
        self.assertIsNone(by[1]["duplicate_of"])
        self.assertEqual(by[1]["stars"], 5)
        self.assertEqual(by[4]["sentiment"], "xau")
        self.assertEqual(by[5]["quote"], "")
        self.assertFalse(by[5]["quote_ok"])
        self.assertTrue(by[1]["quote_ok"])
        self.assertEqual((d["informative"], d["positive"], d["negative"]), (3, 2, 1))
        self.assertTrue(d["enough"])
        self.assertEqual(d["counts"]["chat_luong"], 3)
        self.assertEqual(d["notes"], [])

    def test_no_reviews_asks(self):
        res = agent.answer("shop có uy tín không?")
        self.assertEqual(res["output"],
                         "Bạn dán giúp danh sách review theo dạng: Sản phẩm: <tên> || [1] 5★ <review> [2] 4★ <review> ...")
        self.assertTrue(res["detail"]["ask"])
        self.assertEqual(res["detail"]["reviews"], [])

    def test_bad_json_error(self):
        with mock.patch.object(agent, "call_model", fake_model("xin lỗi")):
            res = agent.answer(B07)
        self.assertEqual(res["output"], "Lỗi: không đọc được kết quả gán nhãn, vui lòng thử lại.")
        self.assertTrue(res["detail"]["error"])

    def test_scope_note_in_detail(self):
        with mock.patch.object(agent, "call_model", fake_model(json.dumps(LABELS, ensure_ascii=False))):
            res = agent.answer("Mình có nên mua không? || " + B07)
        self.assertEqual(len(res["detail"]["notes"]), 1)
        self.assertTrue(res["output"].startswith(res["detail"]["notes"][0]))


if __name__ == "__main__":
    unittest.main()
