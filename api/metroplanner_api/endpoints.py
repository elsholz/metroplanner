from abc import ABC
from typing import Dict
from methods import GET, POST, PATCH, DELETE
import responses
import environment
from bson.objectid import ObjectId
from datetime import datetime


class Endpoint(ABC):
    children: Dict[str, "Endpoint"] = None


class EndpointMethod(ABC):
    pass


class PublicEndpoint(Endpoint):
    """
    Parent class for all public endpoints.
    """

    class PlanEndpoints(Endpoint):
        """
        Contains all endpoints for the plan resource.
        Currently only supports the GET method.
        """

        class GetPlan(EndpointMethod):
            """
            Returns all public information about a plan accessed by
            a shortlink. Data regarding the planstate (nodes, edges,
            labels, etc.) is NOT included here.
            """

            def __init__(self, event, context, env: environment.Environment) -> None:
                self.event = event
                self.context = context
                self.env = env

            def __call__(self) -> Dict:
                path_parameters = self.event["pathParameters"]
                shortlink = path_parameters["shortlink"]
                print(f"GET Request for plan for shortlink {shortlink}")
                try:
                    db = self.env.get_database()

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
                                    return responses.not_found_404()
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
                                            ]
                                        }
                                    )
                            else:
                                print(
                                    f"Error: Plan with ID {plan_id} for "
                                    f"Shortlink {shortlink} does not exist."
                                )
                                return responses.not_found_404()
                        else:
                            print("Link is inactive")
                            return responses.not_found_404()
                    else:
                        print("Link not found")
                        return responses.not_found_404()
                    return responses.ok_200(link_result)

                except Exception as e:
                    print("Exception!!:", e)
                    return responses.ok_200(str(e))

        children = {GET: GetPlan}

    class PlanstateEndpoints(Endpoint):
        """
        Contains all endpoints for the planstate resource.
        Currently only supports the GET method.
        """

        class GetPlanstate(EndpointMethod):
            """
            Returns all plan state information. Format may change
            in the future to allow for better compression.
            """

            def __init__(self, event, context, env: environment.Environment) -> None:
                self.event = event
                self.context = context
                self.env = env

            def __call__(self) -> Dict:
                path_parameters = self.event["pathParameters"]
                shortlink = path_parameters["shortlink"]
                print(f"GET Request for planstate for shortlink {shortlink}")

                try:
                    db = self.env.get_database()
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
                                    return responses.not_found_404()
                                else:
                                    print(
                                        "Plan found and not deleted, getting latest state"
                                    )
                                    latest_state = db.planstates.find_one(
                                        {"_id": plan_result["currentState"]}, {"_id": 0}
                                    )
                                    print("Found latest state:", latest_state)
                                    latest_state["colorTheme"] = str(
                                        latest_state["colorTheme"]
                                    )

                                    time_to_hour = (
                                        datetime.now().isoformat().split(":")[0]
                                    )

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

                                    return responses.ok_200(latest_state)
                            else:
                                print(f"Plan with ID {plan_id} not found")
                                return responses.not_found_404()
                        else:
                            print("Link is not active")
                            return responses.not_found_404()
                    else:
                        print(f"Link {shortlink} not found")
                        return responses.not_found_404()
                except Exception as e:
                    print("Exception!!:", e)
                    return responses.ok_200(str(e))

        children = {GET: GetPlanstate}

    children = {
        "/plan/{shortlink}": PlanEndpoints,
        "/planstate/{shortlink}": PlanstateEndpoints,
    }


class PrivateEndpoint(Endpoint):
    """
    Parent class for all private endpoints.
    """

    children = {}
