import json
import tempfile
from pathlib import Path

# Bundled seed data (grn.json, po.json, ...) — read-only at runtime on serverless hosts
# like Vercel, whose deployed filesystem can't be written to.
DATA_DIR = Path(__file__).parent / "data"

# Where POST endpoints (invoices, pir) append rows. Vercel only allows writes under
# /tmp; a local run gets the OS temp dir too, which is fine for a dummy API.
WRITE_DIR = Path(tempfile.gettempdir()) / "sap-api-data"
WRITE_DIR.mkdir(parents=True, exist_ok=True)


def read_json(filename: str) -> list[dict]:
    # Prefer previously-written rows in this runtime instance, if any, over the bundled seed.
    for base in (WRITE_DIR, DATA_DIR):
        path = base / filename
        if path.exists():
            with path.open(encoding="utf-8") as f:
                return json.load(f)
    return []


def append_json(filename: str, rows: list[dict]) -> None:
    existing = read_json(filename)
    existing.extend(rows)
    path = WRITE_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
        f.write("\n")
