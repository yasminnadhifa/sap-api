from fastapi import FastAPI

from .routers import grn, invoices, pir, po
from .store import seed_all

app = FastAPI(title="SAP API (mock)", version="1.0.0")
app.include_router(grn.router)
app.include_router(po.router)
app.include_router(invoices.router)
app.include_router(pir.router)


@app.on_event("startup")
def on_startup():
    seed_all()


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
