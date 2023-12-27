from fastapi import APIRouter
from starlette.requests import Request
import responses


router = APIRouter()


@router.get("/{color_theme_id}")
def get_colorthemes(color_theme_id, request: Request):
    raise responses.not_implemented_501()
