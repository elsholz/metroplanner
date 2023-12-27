from fastapi import APIRouter

import links
import plans
import planstates
import user

router = APIRouter()

router.include_router(links.router, prefix="links/", tags=["Color Themes"])
router.include_router(plans.router, prefix="plans/", tags=["Plans"])
router.include_router(planstates.router, prefix="planstates/", tags=["Planstates"])
router.include_router(user.router, prefix="user/", tags=["Users"])
