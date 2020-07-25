"""
test api
"""

# from fastapi import APIRouter, HTTPException, Query, Path
from fastapi import (
    APIRouter,
    Query,
    Path,
)


# router = APIRouter()
def create_router():
    """create router"""
    _router = APIRouter()
    return _router


router = create_router()


@router.get("/")
async def get_test1(
    string: str = Query(None, min_length=2, max_length=5, regex=r'[a-c]+.'),
    integer: int = Query(..., gt=1, le=3),
    alias_query: str = Query('default', alias='alias-query'),
):
    return {
        "string": string,
        "integer": integer,
        "alias-query": alias_query,
    }


@router.get("/validation/{path}")
async def validation(
    string: str = Query(None, min_length=2, max_length=5, regex=r'[a-c]+.'),
    integer: int = Query(..., gt=1, le=3),
    alias_query: str = Query('default', alias='alias-query'),
    path: int = Path(10),
):
    return {
        "string": string,
        "integer": integer,
        "alias-query": alias_query,
        "path": path,
    }
