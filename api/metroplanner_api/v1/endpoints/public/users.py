
from fastapi import APIRouter

router = APIRouter()

@router.get("/{sub}")
async def get_users():
    return {"message": "users!"}
