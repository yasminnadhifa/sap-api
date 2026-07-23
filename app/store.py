import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def read_json(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def append_json(filename: str, rows: list[dict]) -> None:
    path = DATA_DIR / filename
    existing = read_json(filename)
    existing.extend(rows)
    with path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
        f.write("\n")
