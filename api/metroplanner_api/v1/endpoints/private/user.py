from fastapi import APIRouter, Request, HTTPException, Depends
from environment import check_auth


router = APIRouter()


@router.get("/")
async def get_user(req: Request, sub: Depends(check_auth)):
    return {"message": "user!"}


@router.patch("/")
async def patch_user(req: Request, sub: Depends(check_auth)):
    return {"message": "user!"}
