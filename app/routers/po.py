from fastapi import APIRouter, Depends, HTTPException, Query

from ..security import require_api_key
from ..store import count_rows, find_rows

router = APIRouter(prefix="/po", tags=["po"], dependencies=[Depends(require_api_key)])


@router.get("")
def get_po(
    pur_doc: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=1000),
):
    query = {"pur_doc": pur_doc} if pur_doc else {}

    # Same rule as /grn: a given filter that matches nothing is a 404, an
    # unfiltered empty page (bulk pull) is just the end of the list.
    if pur_doc and count_rows("po", query) == 0:
        raise HTTPException(status_code=404, detail="No PO line items found.")

    return find_rows("po", query, skip=skip, limit=limit)
