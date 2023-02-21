from abc import ABC
from typing import Dict
from methods import GET, POST, PATCH, DELETE
import responses
import environment
from bson.objectid import ObjectId


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
                    links_collection = self.env.get_database().links
                    plans_collection = self.env.get_database().plans
                    stats_collection = self.env.get_database().stats

                    link_result = links_collection.find_one({"_id": shortlink})
                    print("Link result:", link_result)
                    if link_result:
                        if link_result["active"]:
                            print('Link is active')
                            plan_id = link_result["plan"]
                            print('Plan ID is:', plan_id)
                            plan_result = plans_collection.find_one(
                                {"_id": plan_id},
                                {
                                    "_id": 0,
                                    "planName": 1,
                                    "ownedBy": 1,
                                    "forkedFrom": 1,
                                    "deleted": 1,
                                    "createdAt": 1,
                                    "lastModifiedAt": 1,
                                    "likeCount": 1,
                                    "currentColorTheme": 1,
                                    "currentNumberOfEdges": 1,
                                    "currentNumberOfLabels": 1,
                                    "currentNumberOfLines": 1,
                                    "currentNumberOfNodes": 1,
                                },
                            )
                            print('Plan result:', plan_result)
                            if plan_result:
                                if plan_result.get("deleted", None):
                                    print(
                                        f"Error: Plan with ID {plan_id} for "
                                        f"Shortlink {shortlink} has been deleted."
                                    )
                                    return responses.not_found_404()
                                else:
                                    print("Plan found and not deleted, getting stats")
                                    stats_result = stats_collection.find_one(
                                        {
                                            "_id": {
                                                "plan": plan_id,
                                                "link": shortlink,
                                            }
                                        },
                                        {
                                            "totalCound": 1,
                                            "_id": 0,
                                        },
                                    ) or {}
                                    print('Stats found:', stats_result)
                                    plan_result['totalViewCount'] = stats_result.get('totalCount', 0)
                                    for k,v in plan_result.items():
                                        if isinstance(v, ObjectId):
                                            plan_result[k] = str(v)
                                    return responses.ok_200(plan_result)
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

            def __init__(self, event, context) -> None:
                path_parameters = event["pathParameters"]
                shortlink = path_parameters["shortlink"]
                print(f"GET Request for planstate for shortlink {shortlink}")

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
