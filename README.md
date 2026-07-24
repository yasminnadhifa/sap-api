# SAP API (mock)

Dummy FastAPI implementation of the SAP Integration Data Contract, for local testing. Storage is MongoDB Atlas — each collection (`grn`, `po`, `pir`, `invoices`) is auto-seeded from the bundled JSON files in `app/data/` the first time it's found empty, so a fresh Atlas cluster works out of the box.

All endpoints require an `X-API-Key` header (see `API_KEY` in `.env`). Requires `MONGO_URI` (an Atlas connection string) and optionally `MONGO_DB_NAME` (defaults to `sap_api`).

## Endpoints

| Method | Path | Filter / Body | Collection |
|--------|------|----------------|-----------|
| GET | `/grn` | `grn_number` or `po_number` | `grn` |
| GET | `/po` | `pur_doc` | `po` |
| POST | `/invoices` | one row object or a list of rows | `invoices` |
| POST | `/pir` | one row object or a list of rows | `pir` |
| GET | `/health` | — | — |

## Run locally

```bash
pip install -r requirements.txt
# set MONGO_URI (and API_KEY) in .env first
uvicorn app.main:app --reload --port 7101
```

## Run with Docker

```bash
docker compose up --build
```

## Deploy to Vercel

Set `MONGO_URI` (and `MONGO_DB_NAME` if not using the `sap_api` default) as environment variables in the Vercel project settings, alongside the existing `API_KEY`. No other change is needed — the Mongo client is created lazily and reused across warm invocations.

## Example

```bash
curl -H "X-API-Key: sk_e8974940c547c4f8cd16e207e7dc609e6dc3cb9f3c22ada1" \
  "http://localhost:7101/grn?grn_number=5000030671"

curl -X POST -H "X-API-Key: sk_e8974940c547c4f8cd16e207e7dc609e6dc3cb9f3c22ada1" \
  -H "Content-Type: application/json" \
  -d '{"invoice_number":"INV-2026-001","invoice_date":"2026-06-05","currency":"SGD","total":15000,"supplier_name":"Maha Chemicals (Asia) Pte Ltd","material_code":"98A060003","material_description":"Tinuvin 292","uom":"KG","qty":1100,"unit_price":5.5,"price":6050}' \
  "http://localhost:7101/invoices"
```
