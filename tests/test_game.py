import json
import tempfile
import unittest
from pathlib import Path

import game


class TestGame(unittest.TestCase):
    def test_default_python_challenges_count(self):
        challenges = game.default_python_challenges()
        self.assertEqual(len(challenges), 3)

    def test_default_sql_challenges_count(self):
        challenges = game.default_sql_challenges()
        self.assertEqual(len(challenges), 3)

    def test_sql_database_seeded(self):
        conn = game.setup_sql_db()
        rows = conn.execute("SELECT COUNT(*) FROM learners").fetchone()
        conn.close()
        self.assertEqual(rows[0], 4)

    def test_progress_save_and_load(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original = game.PROGRESS_FILE
            try:
                game.PROGRESS_FILE = Path(temp_dir) / "progress.json"
                payload = {"python_done": 2, "sql_done": 1, "score": 35}
                game.save_progress(payload)
                loaded = game.load_progress()
                self.assertEqual(loaded, payload)
            finally:
                game.PROGRESS_FILE = original

    def test_progress_invalid_json_fallback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original = game.PROGRESS_FILE
            try:
                game.PROGRESS_FILE = Path(temp_dir) / "progress.json"
                game.PROGRESS_FILE.write_text("{not-json", encoding="utf-8")
                loaded = game.load_progress()
                self.assertEqual(loaded, {"python_done": 0, "sql_done": 0, "score": 0})
            finally:
                game.PROGRESS_FILE = original

    def test_progress_type_fallback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original = game.PROGRESS_FILE
            try:
                game.PROGRESS_FILE = Path(temp_dir) / "progress.json"
                game.PROGRESS_FILE.write_text(
                    json.dumps({"python_done": "x", "sql_done": 2, "score": 10}),
                    encoding="utf-8",
                )
                loaded = game.load_progress()
                self.assertEqual(loaded, {"python_done": 0, "sql_done": 0, "score": 0})
            finally:
                game.PROGRESS_FILE = original


if __name__ == "__main__":
    unittest.main()
