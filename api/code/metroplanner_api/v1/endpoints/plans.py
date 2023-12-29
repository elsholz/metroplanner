from starlette.requests import Request
from fastapi import APIRouter
from bson.objectid import ObjectId

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.get("/{shortlink}")
def get_plans(shortlink, request: Request) -> type_definitions.RetrievePlan:
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
                                "totalCount": 1,
                                "_id": 0,
                            },
                        )
                        or {}
                    )
                    print("Stats found:", stats_result)
                    plan_result["totalViewCount"] = stats_result.get("totalCount", 0)
                    for k, v in plan_result.items():
                        if isinstance(v, ObjectId):
                            plan_result[k] = str(v)
                    plan_result.pop("deleted", None)
                    plan_result.pop("history", None)
                    plan_result.pop("_id", None)
                    plan_result: dict
                    return {
                        k: v
                        for k, v in plan_result.items()
                        if k
                        in [
                            "planName",
                            "forkedFrom",
                            "ownedBy",
                            "createdAt",
                            "lastModifiedAt",
                            "likeCount",
                            "currentColorTheme",
                            "currentNumberOfEdges",
                            "currentNumberOfLabels",
                            "currentNumberOfLines",
                            "currentNumberOfNodes",
                            "totalViewCount",
                            "planDescription",
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
