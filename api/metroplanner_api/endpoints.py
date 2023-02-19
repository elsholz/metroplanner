from abc import ABC
from typing import Dict
from methods import GET, POST, PATCH, DELETE


class Endpoint(ABC):
    children: Dict[str, "Endpoint"] = None

    def __init__(self, request, context) -> None:
        self.request = request
        self.context = context
        super().__init__()


class PublicEndpoint(Endpoint):
    def __init__(self, request, context) -> None:
        super().__init__(request, context)


class PrivateEndpoint(Endpoint):
    def __init__(self, request, context) -> None:
        super().__init__(request, context)


class PlanEndpoints(PublicEndpoint):
    def __init__(self, request, context) -> None:
        super().__init__(request, context)


class GetPlan(PlanEndpoints):
    def __init__(self, request, context) -> None:
        super().__init__(request, context)
        
        # planRoutes.route("/api/plan/:shortlink").get(async function (req, res) {
        #   const shortLink = req.params["shortlink"]
        #   const link = await Link.findById({
        #     _id: shortLink
        #   })
        # 
        #   if (link && link.active) {
        #     let plan = await Plan.findById({
        #       _id: link.plan
        #     })
        # 
        #     if (plan) {
        #       const stats = await Stats.findById({
        #         plan: link.plan,
        #         link: shortLink,
        #       }, {
        #         totalCount: 1,
        #       })
        # 
        #       JSON200(res, {
        #         plan: plan,
        #         stats: stats
        #       }, 0)
        #     } else HTTP404(res)
        # 
        #   } else HTTP404(res)
        # })
class GetPlanstate(PlanEndpoints):
    def __init__(self, request, context) -> None:
        super().__init__(request, context)


PlanEndpoints.children = {GET: GetPlan}
PublicEndpoint.children = {
    "plans": PlanEndpoints
}
