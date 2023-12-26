from fastapi import APIRouter, Request, HTTPException, Depends
from environment import check_auth


router = APIRouter()


@router.post("/")
async def post_plan(req: Request, sub: Depends(check_auth)):
    return {"message": "plans!"}


@router.patch("/{planID}")
async def patch_plan(planID, req: Request, sub: Depends(check_auth)):
    return {"message": "plans!"}


@router.get("/{planID}")
async def get_plan(planID, req: Request, sub: Depends(check_auth)):
    return {"message": "plans!"}
