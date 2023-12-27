from fastapi import APIRouter, Request, HTTPException, Depends
from environment import check_auth
import responses


router = APIRouter()


@router.post("/")
def post_shortlink(req: Request, sub: Depends(check_auth)):
    raise responses.not_implemented_501()


@router.get("/{shortlink}")
def get_shortlink(shortlink, req: Request, sub: Depends(check_auth)):
    raise responses.not_implemented_501()


@router.delete("/{shortlink}")
def delete_shortlink(shortlink, req: Request, sub: Depends(check_auth)):
    raise responses.not_implemented_501()
