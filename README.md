# SAP API (mock)

Dummy FastAPI implementation of the SAP Integration Data Contract, for local testing. No database — `GET` endpoints read from JSON files seeded from DMM's sample data, `POST` endpoints append to JSON files.

All endpoints require an `X-API-Key` header (see `API_KEY` in `.env`).

## Endpoints

| Method | Path | Filter / Body | Data file |
|--------|------|----------------|-----------|
| GET | `/grn` | `grn_number` or `po_number` | `app/data/grn.json` |
| GET | `/po` | `pur_doc` | `app/data/po.json` |
| POST | `/invoices` | one row object or a list of rows | `app/data/invoices.json` |
| POST | `/pir` | one row object or a list of rows | `app/data/pir.json` |
| GET | `/health` | — | — |

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 7101
```

## Run with Docker

```bash
docker compose up --build
```

## Example

```bash
curl -H "X-API-Key: sk_e8974940c547c4f8cd16e207e7dc609e6dc3cb9f3c22ada1" \
  "http://localhost:7101/grn?grn_number=5000030671"

curl -X POST -H "X-API-Key: sk_e8974940c547c4f8cd16e207e7dc609e6dc3cb9f3c22ada1" \
  -H "Content-Type: application/json" \
  -d '{"invoice_number":"INV-2026-001","invoice_date":"2026-06-05","currency":"SGD","total":15000,"supplier_name":"Maha Chemicals (Asia) Pte Ltd","material_code":"98A060003","material_description":"Tinuvin 292","uom":"KG","qty":1100,"unit_price":5.5,"price":6050}' \
  "http://localhost:7101/invoices"
```
