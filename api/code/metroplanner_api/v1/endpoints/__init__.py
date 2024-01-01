from fastapi import APIRouter

router = APIRouter()


from . import _links

router.include_router(_links.router, prefix="/_links", tags=["Private"])

from . import _planstates

router.include_router(_planstates.router, tags=["Private"])

from . import _plans

router.include_router(_plans.router, tags=["Private"])


from . import _user

router.include_router(_user.router, prefix="/_user", tags=["Private"])


from . import colorthemes

router.include_router(colorthemes.router, prefix="/colorthemes", tags=["Public"])

from . import plans

router.include_router(plans.router, prefix="/plans", tags=["Public"])

from . import planstates

router.include_router(planstates.router, prefix="/planstates", tags=["Public"])

from . import users

router.include_router(users.router, prefix="/users", tags=["Public"])
