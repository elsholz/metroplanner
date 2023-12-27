from fastapi import APIRouter

import colorthemes
import plans
import planstates
import users

router = APIRouter()

router.include_router(colorthemes.router, prefix="colorthemes/", tags=["Color Themes"])
router.include_router(plans.router, prefix="plans/", tags=["Plans"])
router.include_router(planstates.router, prefix="planstates/", tags=["Planstates"])
router.include_router(users.router, prefix="users/", tags=["Users"])
