
from fastapi import APIRouter

router = APIRouter()

@router.get("/{shortlink}")
async def get_planstates():
    return {"message": "planstates!"}
