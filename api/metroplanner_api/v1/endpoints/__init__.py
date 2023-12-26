from fastapi import APIRouter, Request, Depends


from . import private
from . import public

router = APIRouter()
router.include_router(
    private.router,
    prefix="/_",
    tags=["Private"],
    # dependencies=[Depends(check_auth)],  # TODO
)
router.include_router(public.router, prefix="/", tags=["Public"])
