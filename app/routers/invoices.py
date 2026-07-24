from typing import Union

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from ..security import require_api_key
from ..store import insert_rows

router = APIRouter(prefix="/invoices", tags=["invoices"], dependencies=[Depends(require_api_key)])


class InvoiceRow(BaseModel):
    invoice_number: str
    invoice_date: str
    currency: str
    total: float
    supplier_name: str
    material_code: str
    material_description: str
    uom: str
    qty: float
    unit_price: float
    price: float


@router.post("", status_code=status.HTTP_201_CREATED)
def post_invoices(payload: Union[InvoiceRow, list[InvoiceRow]]):
    rows = payload if isinstance(payload, list) else [payload]
    dumped = [row.model_dump() for row in rows]
    insert_rows("invoices", dumped)
    return {"received": len(dumped), "rows": dumped}
