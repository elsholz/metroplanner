from fastapi import APIRouter, Request, HTTPException, Depends
from environment import check_auth


router = APIRouter()


@router.post("/{planID}/_planstates")
async def post_planstate(planID, req: Request, sub: Depends(check_auth)):
    return {"message": "planstates!"}


@router.get("/{planID}/_planstates/{planstateID}")
async def get_planstate(planID, planstateID, req: Request, sub: Depends(check_auth)):
    return {"message": "planstates!"}
