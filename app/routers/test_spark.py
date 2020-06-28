"""test spark"""

from fastapi import APIRouter

from .. import exec_spark


def create_router():
    """create router"""
    _router = APIRouter()
    return _router


router = create_router()


@router.get("/")
async def site_root(orient: str="dict"):
    dict_db = exec_spark.get_databases(orient=orient)
    dict_table = exec_spark.get_tables(orient=orient)
    return {
        "db": dict_db,
        "table": dict_table,
    }


@router.post("/")
async def create_db(db: str):
    result = exec_spark.create_database(db=db)
    return result
