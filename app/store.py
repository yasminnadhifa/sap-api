import json
from pathlib import Path

from .db import get_db

# Bundled seed data (grn.json, po.json, ...) - only used to populate a collection
# once, the first time it's found empty (e.g. right after wiring up a fresh Atlas cluster).
DATA_DIR = Path(__file__).parent / "data"

SEEDED_COLLECTIONS = ["grn", "po", "pir", "invoices"]


def seed_all() -> None:
    for name in SEEDED_COLLECTIONS:
        _seed_if_empty(name)


def _seed_if_empty(collection_name: str) -> None:
    coll = get_db()[collection_name]
    if coll.estimated_document_count() > 0:
        return
    seed_path = DATA_DIR / f"{collection_name}.json"
    if not seed_path.exists():
        return
    with seed_path.open(encoding="utf-8") as f:
        rows = json.load(f)
    if rows:
        coll.insert_many(rows)


def find_rows(collection_name: str, query: dict | None = None, skip: int = 0, limit: int | None = None) -> list[dict]:
    cursor = get_db()[collection_name].find(query or {}, {"_id": 0}).skip(skip)
    if limit is not None:
        cursor = cursor.limit(limit)
    return list(cursor)


def count_rows(collection_name: str, query: dict | None = None) -> int:
    return get_db()[collection_name].count_documents(query or {})


def insert_rows(collection_name: str, rows: list[dict]) -> None:
    if rows:
        get_db()[collection_name].insert_many(rows)
