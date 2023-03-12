from abc import ABC, abstractmethod
from typing import Dict
from methods import GET, POST, PATCH, DELETE
import responses
import environment
from bson.objectid import ObjectId
from datetime import datetime
import jsonschema
import json
from pymongo import ReturnDocument


class EndpointCollection(ABC):
    """
    A Collection of an endpoint's methods or of subordinate
    endpoint collections.
    """

    children: Dict[str, "EndpointCollection"] = None


class EndpointMethod(ABC):
    """
    Baseclass for all endpoint methods.
    Methods are first instantiated and then invoked like a function
    call, hence the __call__ magic method needs be defined.
    """

    @abstractmethod
    def __call__(self) -> Dict:
        ...


class PublicEndpoint(EndpointCollection):
    """
    Contains all public endpoint collections.
    """

    class PlanEndpoints(EndpointCollection):
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
                                                "planDescription",
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
                except Exception as e:
                    print("Exception!!:", e)
                    return responses.internal_server_error_500()

        children = {GET: GetPlan}

    class PlanstateEndpoints(EndpointCollection):
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
                    return responses.internal_server_error_500()

        children = {GET: GetPlanstate}

    class ColorthemeEndpoints(EndpointCollection):
        class GetColorTheme(EndpointMethod):
            def __init__(self, event, context, env: environment.Environment) -> None:
                self.event = event
                self.context = context
                self.env = env

            def __call__(self) -> Dict:
                try:
                    db = self.env.get_database()
                except Exception as e:
                    print("Exception!!:", e)
                    return responses.internal_server_error_500()

        children = {GET: GetColorTheme}

    class UserEndpoints(EndpointCollection):
        class GetUser(EndpointMethod):
            def __init__(self, event, context, env: environment.Environment) -> None:
                self.event = event
                self.context = context
                self.env = env

            def __call__(self) -> Dict:
                pass

        children = {GET: GetUser}

    children = {
        "/api/plans/{shortlink}": PlanEndpoints,
        "/api/planstates/{shortlink}": PlanstateEndpoints,
        "/api/colorthemes/{colorThemeID}": ColorthemeEndpoints,
        "/api/users/{sub}": UserEndpoints,
    }


class PrivateEndpoint(EndpointCollection):
    """
    Contains all private endpoint collections.
    """

    class UserEndpoints(EndpointCollection):
        class GetUser(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                try:
                    db = self.env.get_database()
                    user_result = db.users.find_one({"_id": self.sub})
                    if user_result:
                        print("Found User Profile:", user_result)
                        return responses.ok_200(user_result)
                    else:
                        print("User profile not found, creating profile.")
                        user_creation_result = db.users.insert_one(
                            user_data := {
                                "_id": self.sub,
                                "displayName": "",
                                "public": False,
                                "profileViews": 0,
                                "likesGiven": [],
                                "profilePicture": None,
                                "bio": "",
                            }
                        )

                        print("User Creation result", user_creation_result)
                        return responses.ok_200(user_data)
                except Exception as e:
                    print("Exception!!:", e)
                    return responses.internal_server_error_500()

        class PatchUser(EndpointMethod):
            schema = {
                "type": "object",
                "properties": {
                    "bio": {
                        "type": "string",
                        "pattern": "^([.]*)$",
                        "minLength": 0,
                        "maxLength": 250,
                    },
                    "displayName": {
                        "type": "string",
                        "pattern": "^.*$",
                        "minLength": 3,
                        "maxLength": 20,
                    },
                    "profilePicture": {
                        "oneOf": [
                            {
                                "type": "string",
                                "pattern": "^https://dev.ich-hab-plan.de.*$",
                                "minLength": 10,
                                "maxLength": 150,
                            },
                            {"type": "null"},
                        ]
                    },
                },
                "additionalProperties": False,
                "required": ["bio", "displayName", "profilePicture"],
            }

            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                print(self.event)
                try:
                    data = json.loads(self.event["body"])
                    try:
                        jsonschema.validate(instance=data, schema=self.schema)
                        db = self.env.get_database()
                        updated_result = db.users.update_one(
                            {
                                "_id": self.sub,
                            },
                            {"$set": data},
                            ReturnDocument.AFTER,
                        )
                        if updated_result:
                            return responses.ok_200(updated_result)
                        else:
                            return responses.internal_server_error_500()
                    except jsonschema.ValidationError as e:
                        print("Error validating user patch data", data)
                        return responses.bad_request_400()
                except KeyError as e:
                    print(e)
                    return responses.bad_request_400()
                except Exception as e:
                    print(e)
                    return responses.internal_server_error_500()

        children = {GET: GetUser, PATCH: PatchUser}

    class PlanEndpoints(EndpointCollection):
        class GetPlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        class PatchPlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        class PostPlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        class DeletePlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        children = {GET: GetPlan, PATCH: PatchPlan, POST: PostPlan, DELETE: DeletePlan}

    class LinkEndpoints(EndpointCollection):
        class PostLink(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        class PatchLink(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        class DeleteLink(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        children = {POST: PostLink, PATCH: PatchLink, DELETE: DeleteLink}

    class PlanstateEndpoints(EndpointCollection):
        class PostPlanstate(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        class GetPlanstate(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

        children = {POST: PostPlanstate, GET: GetPlanstate}

    children = {
        "/api/_user": UserEndpoints,
        "/api/_plans": PlanEndpoints,
        "/api/_plans/{planID}": PlanEndpoints,
        "/api/_links": LinkEndpoints,
        "/api/_links/{shortlink}": LinkEndpoints,
        "/api/_planstates": PlanstateEndpoints,
        "/api/_planstates/{planstateID}": PlanstateEndpoints,
    }
