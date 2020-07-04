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


@router.get("/api/databases/{db}")
async def describe_database(
    db: str,
    orient: str = "dict",
    extended: Optional[bool] = True,
):
    """describe database"""
    result = exec_spark.describe_database(
        db=db,
        orient=orient,
        extended=extended,
    )
    return result


@router.post("/api/databases/{db}")
async def create_database(db: str):
    result = exec_spark.create_database(db=db)
    return result


@router.put("/api/databases/{db}")
async def put_database(db: str):
    """
    PUT database

    WARNING:

        - NOT implemented yet.
    """
    return {"message": "Sorry, Not Implemented yet."}


@router.delete("/api/databases/{db}")
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


@router.get("/api/databases/{db}/tables/")
async def get_tables(
    # db: Optional[str],  # = "default",
    db: str = "default",
    orient: str = "dict",
):
    """get table lists."""
    return exec_spark.get_tables(
        db=db,
        orient=orient,
    )


@router.get("/api/databases/{db}/tables/{table}")
async def read_table(
    db: str = "default",
    table: str = "",
    limit: int = 100,
    orient: str = "list",
    # **kwargs
):
    """
    read table

    ToDo:
        - validation
        - read option
            - such as ``order``
    """
    return exec_spark.read_table(
        table=table,
        db=db,
        limit=limit,
        orient=orient,
        # **kwargs
    )
