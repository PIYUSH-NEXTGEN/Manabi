import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # noqa: E402

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs", "openapi.json"))
with open(out, "w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)
print(f"wrote {out}")
