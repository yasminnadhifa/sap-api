import json
from pathlib import Path

from .db import get_db

# Bundled seed data (grn.json, po.json) - GRN and PO are static reference data with
# no POST endpoint, so they're just read straight from the repo, no DB involved.
DATA_DIR = Path(__file__).parent / "data"


def read_json(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# PIR and invoices are POST-only (data pushed in over time), so they're the only
# collections that actually need persistent storage - MongoDB Atlas.
def insert_rows(collection_name: str, rows: list[dict]) -> None:
    if not rows:
        return
    # insert_many mutates each dict in place, adding "_id" (a bson ObjectId) - copy first so
    # that never leaks into the caller's rows (which routers echo back in the response body;
    # ObjectId isn't JSON-serializable and would crash the response).
    get_db()[collection_name].insert_many([dict(r) for r in rows])
