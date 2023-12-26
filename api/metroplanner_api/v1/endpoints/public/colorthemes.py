from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()

@router.get("/{colorThemeID}")
async def get_colorthemes(request: Request):
    return {"message": "colorthemes!"}
