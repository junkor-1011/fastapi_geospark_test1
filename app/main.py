"""
app main
"""

import pathlib

# from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    RedirectResponse,
)

# from .routers import test_api
from .routers import (
    test_api,
    test_crud,
    test_spark,
    subpage,
)
# from .test_static import router as router_static   # TMP

# const
PATH_STATIC = str(pathlib.Path(__file__).resolve().parent / "static")


def create_app():
    """create app"""
    _app = FastAPI()

    _app.include_router(
        test_api.router,
        prefix="/test_api",
        tags=["test_api"],
        responses={404: {"description": "not found"}},
    )
    _app.include_router(
        test_crud.router,
        prefix="/test_crud",
        tags=["test_crud"],
        responses={404: {"description": "not found"}},
    )
    _app.include_router(
        test_spark.router,
        prefix="/test_spark",
        tags=["test_spark"],
        responses={404: {"description": "not found"}},
    )
    _app.include_router(
        subpage.router,
        prefix="/subpage",
        tags=["subpage"],
        responses={404: {"description": "not found"}},
    )

    # static
    _app.mount(
        "/static",
        StaticFiles(directory=PATH_STATIC, html=False),
        name="static",
    )

    return _app


app = create_app()


@app.get('/')
async def site_root():
    """hello-world(TMP)"""
    return {"message": "Hello, WORLD!"}


@app.get('/redirect_subpage')
async def redirect_subpage():
    """redirect test"""
    # status_codeは何故か効かない
    return RedirectResponse(
        "/subpage",
        # status_code=303,
    )
