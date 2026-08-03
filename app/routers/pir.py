from typing import Union

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from ..security import require_api_key
from ..store import insert_rows

router = APIRouter(prefix="/pir", tags=["pir"], dependencies=[Depends(require_api_key)])


class PirRow(BaseModel):
    supplierMaterial: str
    Material: str
    Supplier: str


@router.post("", status_code=status.HTTP_201_CREATED)
def post_pir(payload: Union[PirRow, list[PirRow]]):
    rows = payload if isinstance(payload, list) else [payload]
    dumped = [row.model_dump() for row in rows]
    insert_rows("pir", dumped)
    return {"received": len(dumped), "rows": dumped}
