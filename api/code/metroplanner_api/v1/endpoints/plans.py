from starlette.requests import Request
from fastapi import APIRouter
from bson.objectid import ObjectId

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.get("/{shortlink}")
def get_plans(shortlink, request: Request) -> type_definitions.PlanPublicGetResponse:
    print(f"GET Request for plan for shortlink {shortlink}")
    db = ENV.database
    link_result = db.links.find_one({"_id": shortlink})
    print("Link result:", link_result)

    if link_result:
        if link_result["active"]:
            print("Link is active")
            plan_id = link_result["plan"]
            print("Plan ID is:", plan_id)
            plan_result = db.plans.find_one(
                {"_id": plan_id},
            )
            print("Plan result:", plan_result)
            if plan_result:
                if plan_result.get("deleted", None):
                    print(
                        f"Error: Plan with ID {plan_id} for "
                        f"Shortlink {shortlink} has been deleted."
                    )
                    return responses.gone_410()
                else:
                    print("Plan found and not deleted, getting stats")
                    stats_result = (
                        db.stats.find_one(
                            {
                                "_id": {
                                    "plan": ObjectId(plan_id),
                                    "link": shortlink,
                                }
                            },
                            {
                                "total_count": 1,
                                "_id": 0,
                            },
                        )
                        or {}
                    )
                    print("Stats found:", stats_result)
                    plan_result["total_view_count"] = stats_result.get("total_count", 0)
                    for k, v in plan_result.items():
                        if isinstance(v, ObjectId):
                            plan_result[k] = str(v)
                    plan_result.pop("deleted", None)
                    plan_result.pop("history", None)
                    plan_result.pop("_id", None)
                    plan_result: dict
                    plan_result['owned_by'] = str(plan_result['owned_by'])
                    return {
                        k: v
                        for k, v in plan_result.items()
                        if k
                        in [
                            "plan_name",
                            "forked_from",
                            "owned_by",
                            "created_at",
                            "last_modified_at",
                            "like_count",
                            "current_colorTheme",
                            "current_number_of_nodes",
                            "current_number_of_lines",
                            "current_number_of_labels",
                            "current_number_of_edges",
                            "total_view_count",
                            "plan_description",
                        ]
                    }
            else:
                print(
                    f"Error: Plan with ID {plan_id} for "
                    f"Shortlink {shortlink} does not exist."
                )
                raise responses.gone_410()
        else:
            print("Link is inactive")
            raise responses.gone_410()
    else:
        print("Link not found")
        raise responses.gone_410()
