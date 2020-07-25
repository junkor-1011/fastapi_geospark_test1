"""
APIRouter static test.
"""

from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/test_static/templates")


def create_router():
    """create router"""
    _router = APIRouter()

    _router.mount("/dir",
                  StaticFiles(directory="app/test_static/dir", html=True),
                  name="static_test",)
    return _router


router = create_router()


# @router.get("/test_static/get")
@router.get("/get")
async def hello():
    """hello(tmp)"""
    return {"message": "hello from APIRouter"}


@router.get("/page")
async def page(request: Request,):
    """test page"""
    return templates.TemplateResponse("index.html",
                                      {"request": request})
