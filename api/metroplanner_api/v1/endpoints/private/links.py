from fastapi import APIRouter, Request, HTTPException, Depends
from metroplanner_api.environment import check_auth


router = APIRouter()

@router.post("/")
async def post_shortlink(req: Request, sub: Depends(check_auth)):
    return {"message": "links!"}

@router.get("/{shortlink}")
async def get_shortlink(shortlink, req: Request, sub: Depends(check_auth)):
    return {"message": "links!"}

