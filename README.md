# SAP API (mock)

Dummy FastAPI implementation of the SAP Integration Data Contract, for local testing. Two storage models, split by whether an endpoint is read-only reference data or accumulates pushed rows:
- `GET /grn` and `GET /po` — static reference data, read straight from the bundled JSON files in `app/data/`. No database involved.
- `POST /invoices` and `POST /pir` — rows pushed in over time, stored in MongoDB Atlas so they actually persist across serverless invocations (unlike the old JSON-append-to-`/tmp` approach, which didn't survive a cold start on Vercel).

All endpoints require an `X-API-Key` header (see `API_KEY` in `.env`). `/invoices` and `/pir` additionally require `MONGO_URI` (an Atlas connection string) and optionally `MONGO_DB_NAME` (defaults to `sap_api`).

## Endpoints

| Method | Path | Filter / Body | Storage |
|--------|------|----------------|-----------|
| GET | `/grn` | `grn_number` or `po_number` | `app/data/grn.json` |
| GET | `/po` | `pur_doc` | `app/data/po.json` |
| POST | `/invoices` | one row object or a list of rows | MongoDB `invoices` collection |
| POST | `/pir` | one row object or a list of rows | MongoDB `pir` collection |
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
