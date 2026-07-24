import os

from pymongo import MongoClient
from pymongo.database import Database

# Reused across warm serverless invocations (Vercel) - a fresh MongoClient per
# request would exhaust Atlas's connection limit under any real load.
_client: MongoClient | None = None


def get_db() -> Database:
    global _client
    if _client is None:
        _client = MongoClient(os.environ["MONGO_URI"])
    return _client[os.getenv("MONGO_DB_NAME", "sap_api")]
