from abc import ABC
from typing import Dict
from methods import GET, POST, PATCH, DELETE
import responses
import environment


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
                path_parameters = event["pathParameters"]
                shortlink = path_parameters["shortlink"]
                print(f"GET Request for plan for shortlink {shortlink}")

                try:
                    links_collection = env.get_database().links
                    plans_collection = env.get_database().plans

                    link_result = links_collection.find_one({"_id": shortlink})
                    print('Link result:', link_result)
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
