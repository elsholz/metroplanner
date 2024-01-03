from bson.objectid import ObjectId
from fastapi import APIRouter
from datetime import datetime

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.get("/{shortlink}")
def get_planstates(shortlink) -> type_definitions.PlanstatePublicGetResponse:
    print(f"GET Request for planstate for shortlink {shortlink}")

    db = ENV.database
    link_result = db.links.find_one({"_id": shortlink})
    print("Link result:", link_result)
    if link_result:
        if link_result["active"]:
            print("Link is active")
            plan_id = link_result["plan"]
            print("Plan ID is:", plan_id)
            plan_result = db.plans.find_one(
                {"_id": plan_id}, {"currentState": 1, "deleted": 1}
            )
            print("Plan result:", plan_result)
            if plan_result:
                if plan_result.get("deleted", None):
                    print(
                        f"Error: Plan with ID {plan_id} for "
                        f"Shortlink {shortlink} has been deleted."
                    )
                    raise responses.gone_410()
                else:
                    print("Plan found and not deleted, getting latest state")
                    latest_state = db.planstates.find_one(
                        {"_id": plan_result["currentState"]}, {"_id": 0}
                    )
                    print("Found latest state:", latest_state)
                    # latest_state["colorTheme"] = str(latest_state["colorTheme"])

                    time_to_hour = datetime.now().isoformat().split(":")[0]

                    try:
                        print("Updating stats")
                        update_stats_result = db.stats.update_one(
                            {
                                "_id": {
                                    "plan": plan_id,
                                    "link": shortlink,
                                }
                            },
                            {
                                "$inc": {
                                    "totalCount": 1,
                                    f"views.{time_to_hour}": 1,
                                }
                            },
                            upsert=True,
                        )
                        print(update_stats_result)
                    except Exception as e:
                        print("Error updating statistics:", e)

                    return latest_state
            else:
                print(f"Plan with ID {plan_id} not found")
                raise responses.gone_410()
        else:
            print("Link is not active")
            raise responses.gone_410()
    else:
        print(f"Link {shortlink} not found")
        raise responses.gone_410()
