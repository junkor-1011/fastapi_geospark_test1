"""test spark"""

from typing import (
    Optional,
)

from fastapi import APIRouter

from .. import exec_spark


def create_router():
    """create router"""
    _router = APIRouter()
    return _router


router = create_router()


@router.get("/api/test")
async def site_root(orient: str="dict"):
    """
    test
    """
    dict_db = exec_spark.get_databases(orient=orient)
    dict_table = exec_spark.get_tables(orient=orient)
    return {
        "db": dict_db,
        "table": dict_table,
    }


@router.get("/api/databases/")
async def get_databases(orient: str = "dict"):
    return exec_spark.get_databases(orient=orient)


@router.post("/api/databases/")
async def create_database(db: str):
    result = exec_spark.create_database(db=db)
    return result


@router.delete("/api/databases")
async def delete_database(
    db: str,
    ifexists: Optional[bool] = True,
    mode: Optional[str] = "RESTRICT",
):
    return exec_spark.delete_database(
        db=db,
        ifexists=ifexists,
        mode=mode,
    )
