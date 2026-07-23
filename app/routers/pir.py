from typing import Union

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from ..security import require_api_key
from ..store import append_json

router = APIRouter(prefix="/pir", tags=["pir"], dependencies=[Depends(require_api_key)])


class PirRow(BaseModel):
    sap_item_code: str
    sap_item_description: str
    sap_supplier_code: str
    supplier_item_code: str
    supplier_description: str


@router.post("", status_code=status.HTTP_201_CREATED)
def post_pir(payload: Union[PirRow, list[PirRow]]):
    rows = payload if isinstance(payload, list) else [payload]
    dumped = [row.model_dump() for row in rows]
    append_json("pir.json", dumped)
    return {"received": len(dumped), "rows": dumped}
