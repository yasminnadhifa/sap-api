from fastapi import APIRouter, Depends, HTTPException, Query

from ..security import require_api_key
from ..store import read_json

router = APIRouter(prefix="/grn", tags=["grn"], dependencies=[Depends(require_api_key)])

# Fields returned per line item, per the SAP Integration Data Contract. grn_number
# itself is a filter parameter only, not part of the response shape.
RESPONSE_FIELDS = [
    "do_number", "po_number", "material_code", "material_desc",
    "manufacture_date", "qty", "unit", "qty_une", "supplier_name", "supplier_code",
]


@router.get("")
def get_grn(
    grn_number: str | None = Query(None),
    po_number: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=1000),
):
    rows = read_json("grn.json")
    filtered = rows
    if grn_number:
        filtered = [r for r in filtered if r["grn_number"] == grn_number]
    if po_number:
        filtered = [r for r in filtered if r["po_number"] == po_number]

    # A filter was given but matched nothing -> not found. No filter at all means
    # this is a bulk/paginated pull (e.g. DMM's target-source sync), so an empty
    # page there is just the end of the list, not an error.
    if (grn_number or po_number) and not filtered:
        raise HTTPException(status_code=404, detail="No GRN line items found.")

    page = filtered[skip: skip + limit]
    return [{k: r[k] for k in RESPONSE_FIELDS} for r in page]
