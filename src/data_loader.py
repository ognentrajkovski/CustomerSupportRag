from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]
FAQ_PATH = BASE_DIR / "data" / "faqs.json"

def load_faqs():
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
