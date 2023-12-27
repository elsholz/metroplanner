from starlette.requests import Request
from fastapi import APIRouter
import responses
from bson.objectid import ObjectId
from environment import ENV
import type_definitions


router = APIRouter()


@router.get("/{shortlink}")
def get_plans(shortlink, request: Request) -> type_definitions.Plan:
    print(f"GET Request for plan for shortlink {shortlink}")
    try:
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
                        plan_result["totalViewCount"] = stats_result.get(
                            "totalCount", 0
                        )
                        for k, v in plan_result.items():
                            if isinstance(v, ObjectId):
                                plan_result[k] = str(v)
                        plan_result.pop("deleted", None)
                        plan_result.pop("history", None)
                        plan_result.pop("_id", None)
                        plan_result: dict
                        return responses.ok_200(
                            {
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
                        )
                else:
                    print(
                        f"Error: Plan with ID {plan_id} for "
                        f"Shortlink {shortlink} does not exist."
                    )
                    return responses.gone_410()
            else:
                print("Link is inactive")
                return responses.gone_410()
        else:
            print("Link not found")
            return responses.gone_410()
    except Exception as e:
        print("Exception!!:", e)
        return responses.internal_server_error_500()
