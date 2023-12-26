
from starlette.requests import Request
from fastapi import APIRouter

router = APIRouter()

@router.get("/{shortlink}")
async def get_plans(request: Request):
    return {"message": "plans!"}
