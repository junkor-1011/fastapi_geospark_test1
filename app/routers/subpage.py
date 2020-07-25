"""
test subpage
"""

import pathlib

from fastapi import (
    APIRouter,
    Request,
    # Query,
    # Path,
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    HTMLResponse,
)

# const
PATH_TEMPLATES = str(
    pathlib.Path(__file__).resolve().parent.parent / "templates"
)


def create_router():
    """create router"""
    _router = APIRouter()
    return _router


router = create_router()


templates = Jinja2Templates(directory=PATH_TEMPLATES)


@router.get("/", response_class=HTMLResponse)
async def site_root(
    request: Request,
):
    """test subpage"""
    title = "test subpage"
    return templates.TemplateResponse(
        "subpage/index.html",
        context={
            "request": request,
            "title": title,
        }
    )
