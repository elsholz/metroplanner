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
from bson.objectid import ObjectId
import request_schemas


def get_basic_plan_data():
    pass


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
                                    return responses.gone_410()
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
                                return responses.gone_410()
                        else:
                            print("Link is not active")
                            return responses.gone_410()
                    else:
                        print(f"Link {shortlink} not found")
                        return responses.gone_410()
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
                path_parameters = self.event["pathParameters"]
                userid = path_parameters["userID"]

                try:
                    db = self.env.get_database()
                    user_result = db.users.find_one({"_id": userid})
                    print("User result:", user_result)
                    if user_result:
                        user_data = {
                            "bio": user_result["bio"],
                            "displayName": user_result["displayName"],
                            "profilePicture": user_result["profilePicture"],
                            "public": (public := user_result["public"]),
                        }
                        if public:
                            # collect plans created
                            # collect plans liked
                            print("User Profile is public")
                        else:
                            print("User Profile is not public")
                            return responses.ok(user_data)

                    else:
                        return responses.gone_410()
                except Exception as e:
                    return responses.internal_server_error_500()

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

                        plans_created = list(
                            db.plans.find(
                                {"ownedBy": self.sub},
                                {
                                    "planName": 1,
                                    "planDescription": 1,
                                    "_id": 1,
                                    "planShortlink": 1,
                                    "public": 1,
                                },
                            )
                        )
                        for p in plans_created:
                            p["planId"] = str(p["_id"])

                            if not "planShortlink" in p:
                                plan_link = db.links.find_one({"plan": p["_id"]})
                                if plan_link:
                                    p["planShortlink"] = plan_link["_id"]

                            del p["_id"]

                        likes = []
                        for liked_planid in user_result["likesGiven"]:
                            print("Get shortlink for plan with id", liked_planid)
                            liked_plan_shortlink = db.links.find_one(
                                {"plan": liked_planid}, {"_id": 1}
                            )
                            print("Liked plan Shortlink:", liked_plan_shortlink)
                            likes.append(liked_plan_shortlink["_id"])
                        user_result["likesGiven"] = likes

                        print("plans as list: ", plans_created)
                        user_result["plansCreated"] = plans_created

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

                        user_data["plansCreated"] = []

                        print("User Creation result", user_creation_result)
                        return responses.ok_200(user_data)
                except Exception as e:
                    print("Exception!!:", e)
                    return responses.internal_server_error_500()

        class PatchUser(EndpointMethod):
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
                        jsonschema.validate(
                            instance=data, schema=request_schemas.patch_user_schema
                        )
                        db = self.env.get_database()
                        updated_result = db.users.find_one_and_update(
                            {
                                "_id": self.sub,
                            },
                            {"$set": data},
                            return_document=ReturnDocument.AFTER,
                        )
                        print("Updated result:", updated_result)
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

            def __call__(self) -> Dict:
                try:
                    path_parameters = self.event["pathParameters"]
                    planid = path_parameters["planID"]
                    db = self.env.get_database()
                    plan_details = db.plans.find_one(
                        {"_id": ObjectId(planid)},
                        {
                            "_id": 0,
                        },
                    )

                    if plan_details["ownedBy"] == self.sub:
                        print("Found plan Details: ", plan_details)

                        if forked_from := plan_details["forkedFrom"]:
                            plan_details["forkedFrom"] = str(forked_from)
                        if current_state := plan_details["currentState"]:
                            plan_details["currentState"] = str(current_state)
                        if isinstance(
                            current_colortheme := plan_details["currentColorTheme"],
                            ObjectId,
                        ):
                            plan_details["currentColorTheme"] = str(current_colortheme)

                        states = []
                        for planstateid in plan_details["history"]:
                            planstate_details = db.planstates.find_one(
                                {"_id": planstateid},
                                {
                                    "_id": 0,
                                    "createdAt": 1,
                                    "numberOfEdges": 1,
                                    "numberOfLines": 1,
                                    "numberOfNodes": 1,
                                    "numberOfLabels": 1,
                                },
                            )
                            if not planstate_details:
                                print(
                                    f"Warning: Planstate details for planstateid {planstateid} not found."
                                )
                                continue
                            planstate_details["planstateid"] = str(planstateid)
                            print("Found planstate details:", planstate_details)
                            states.append(planstate_details)

                        print("states:", states)
                        plan_details["history"] = states

                        shortlinks = list(
                            db.links.find({"plan": ObjectId(planid)}, {"plan": 0})
                        )

                        shortlinks_with_stats = []

                        for shortlink in shortlinks:
                            if shortlink["active"]:
                                print("Shortlink: ", shortlink)
                                shortlink_stats = db.stats.find_one(
                                    {
                                        "_id": {
                                            "plan": ObjectId(planid),
                                            "link": shortlink["_id"],
                                        }
                                    },
                                    {"_id": 0},
                                )
                                if shortlink_stats:
                                    print("found shortlink stats:", shortlink_stats)
                                    shortlink["stats"] = shortlink_stats
                                else:
                                    shortlink["stats"] = {"totalCount": 0, "views": {}}
                                del shortlink["active"]
                                shortlinks_with_stats.append(shortlink)
                        print("Shortlinks:", shortlinks_with_stats)

                        plan_details["shortlinks"] = shortlinks_with_stats
                        print("Plan Details:", plan_details)

                        return responses.ok_200(plan_details)
                    else:
                        return responses.unauthorized_401()

                except Exception as e:
                    print(e)
                    return responses.internal_server_error_500()

        class PatchPlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                try:
                    path_parameters = self.event["pathParameters"]
                    planid = path_parameters["planID"]
                    db = self.env.get_database()
                    plan_details = db.plans.find_one(
                        {
                            "_id": ObjectId(planid),
                        },
                        {
                            "_id": 0,
                            "ownedBy": 1,
                        },
                    )

                    if plan_details["ownedBy"] == self.sub:
                        data = json.loads(self.event["body"])
                        jsonschema.validate(
                            instance=data, schema=request_schemas.patch_plan_schema
                        )

                        set_data = {}

                        for k in [
                            "planName",
                            "planDescription",
                            "currentState",
                            "currentColorTheme",
                        ]:
                            if k == "currentColorTheme":
                                print("Can't change color theme atm")
                                return responses.not_implemented_501()
                            if k == "currentState":
                                new_id = ObjectId(data["currentState"])
                                get_planstate_result = db.planstates.find_one(
                                    {"_id": new_id}, {"_id": 1}
                                )
                                if get_planstate_result:
                                    print(
                                        "Found corresponding planstate!",
                                        get_planstate_result,
                                    )
                                else:
                                    print(
                                        "Did not find corresponding planstate!",
                                        get_planstate_result,
                                    )
                                    return responses.bad_request_400()
                                set_data[k] = new_id
                            else:
                                set_data[k] = data[k]

                        set_data["lastModifiedAt"] = datetime.now().isoformat()

                        db.plans.update_one(
                            {
                                "_id": ObjectId(planid),
                            },
                            {
                                "$set": set_data,
                            },
                        )

                        return responses.ok_200()
                    else:
                        return responses.unauthorized_401()
                except Exception as e:
                    print("Patching plan failed", e)
                    return responses.internal_server_error_500()

        class PostPlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                try:
                    print("Received request to create a new plan. Validating JSON data...")
                    data = json.loads(self.event["body"])
                    jsonschema.validate(
                        instance=data, schema=request_schemas.post_plan_schema
                    )
                    print("Data successfully validated:", data)

                    db = self.env.get_database()

                    new_plan_data = {
                        "planName": data["planName"],
                        "planDescription": data["planName"],
                        "forkedFrom": None,
                        "deleted": None,
                        "createdAt": (now := datetime.now().isoformat()),
                        "lastModifiedAt": now,
                        "likeCount": 0,
                        "ownedBy": self.sub,
                        "colorTheme": (theme := "colorful-dl"),
                        "currentNumberOfEdges": 0,
                        "currentNumberOfLines": 0,
                        "currentNumberOfNodes": 0,
                        "currentNumberOfLabels": 0,
                    }

                    print("initial data for new plan:", new_plan_data)

                    if fork_from := data.get("forkFrom", None):
                        print("Plan is to be forked from", fork_from)
                        if shortlink := fork_from.get("shortlink", None):
                            link_data = db.links.find_one({"_id": shortlink})

                            if link_data and link_data["active"]:
                                planid = link_data["plan"]
                            else:
                                return responses.gone_410()
                        else:
                            planid = ObjectId(fork_from.get("planID", None))

                        plan_details = db.plans.find_one(
                            {
                                "_id": planid,
                            },
                        )

                        if plan_details:
                            if shortlink or plan_details["ownedBy"] == self.sub:
                                planstateid = (
                                    ObjectId(fork_from["planstateID"])
                                    if not shortlink
                                    else plan_details["currentState"]
                                )

                                planstate = db.planstates.find_one(
                                    {
                                        "_id": planstateid,
                                    },
                                    {
                                        "_id": 0,
                                    },
                                )


                                if planstate:
                                    insert_planstate_res = db.planstates.insert_one(planstate)
                                    new_plan_data["currentNumberOfEdges"] = planstate["numberOfEdges"]
                                    new_plan_data["currentNumberOfLines"] = planstate['numberOfLines']
                                    new_plan_data["currentNumberOfNodes"] = planstate['numberOfNodes']
                                    new_plan_data["currentNumberOfLabels"] = planstate['numberOfLabels']
                                    new_plan_data["colorTheme"] = plan_details["colorTheme"]
                                else:
                                    return responses.gone_410()
                            else:
                                raise responses.unauthorized_401()
                        else:
                            return responses.gone_410()
                    else:
                        print("Creating plan from scratch")
                        insert_planstate_res = db.planstates.insert_one(
                            {
                                "createdAt": now,
                                "numberOfEdges": 0,
                                "numberOfLines": 0,
                                "numberOfNodes": 0,
                                "numberOfLabels": 0,
                                "nodes": {},
                                "lines": [],
                                "labels": {},
                                "globalOffsetX": 0,
                                "globalOffsetY": 0,
                                "planHeight": 10,
                                "planWidth": 10,
                                "colorTheme": theme,
                            }
                        )
                    print("Created plan, result:", insert_planstate_res)
                    new_plan_data["currentState"] = (
                        new_planstateid := insert_planstate_res["_id"]
                    )
                    new_plan_data["history"] = [new_planstateid]

                    insert_res = db.plans.insert_one(new_plan_data)
                    print("After insertion, this is the result:", insert_res)

                    return responses.created_201({'planid': str(insert_res['_id'])})

                except jsonschema.ValidationError as e:
                    print(e)
                    return responses.bad_request_400()
                except Exception as e:
                    print("Operation failed", e)
                    return responses.internal_server_error_500()

        class DeletePlan(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                return responses.not_implemented_501()

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

            def __call__(self) -> Dict:
                return responses.not_implemented_501()

        class PatchLink(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                return responses.not_implemented_501()

        class DeleteLink(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                return responses.not_implemented_501()

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

            def __call__(self) -> Dict:
                try:
                    path_parameters = self.event["pathParameters"]
                    planid = path_parameters["planID"]
                    make_current = "makeCurrent" in self.event.get(
                        "queryStringParameters", {}
                    )
                    db = self.env.get_database()
                    plan_details = db.plans.find_one(
                        {"_id": ObjectId(planid)},
                        {
                            "_id": 0,
                            "ownedBy": 1,
                        },
                    )

                    if plan_details["ownedBy"] == self.sub:
                        data = json.loads(self.event["body"])

                        try:
                            print(
                                "Planstate to be created for plan with id",
                                planid,
                                "Make current?",
                                make_current,
                            )
                            jsonschema.validate(
                                instance=data,
                                schema=request_schemas.post_planstate_schema,
                            )

                            number_of_edges = 0

                            for ln in data["lines"]:
                                for cons in ln["connections"]:
                                    number_of_edges += len(cons["nodes"])

                            data["numberOfEdges"] = number_of_edges
                            data["numberOfLines"] = len(data["lines"])
                            data["numberOfNodes"] = len(data["nodes"])
                            data["numberOfLabels"] = len(data["labels"])

                            data["createdAt"] = datetime.now().isoformat()

                            created_result = db.planstates.insert_one(data)
                            print("Created planstate:", created_result)

                            set_plan_data = {
                                "lastModifiedAt": data["createdAt"],
                            }

                            if make_current:
                                set_plan_data["currentState"] = (
                                    created_result.inserted_id,
                                )
                                set_plan_data["numberOfEdges"] = data["numberOfEdges"]
                                set_plan_data["numberOfLines"] = data["numberOfLines"]
                                set_plan_data["numberOfNodes"] = data["numberOfNodes"]
                                set_plan_data["numberOfLabels"] = data["numberOfLabels"]

                            db.plans.update_one(
                                {"_id": ObjectId(planid)},
                                {
                                    "$push": {
                                        "history": created_result.inserted_id,
                                    },
                                    "$set": set_plan_data,
                                },
                            )

                            return responses.created_201(
                                {"planstateID": str(created_result.inserted_id), **data}
                            )
                        except jsonschema.ValidationError as e:
                            print("Validation error creating planstate:", e)
                            return responses.bad_request_400()
                    else:
                        return responses.unauthorized_401()
                except Exception as e:
                    print("error creating planstate:", e)
                    return responses.internal_server_error_500()

        class GetPlanstate(EndpointMethod):
            def __init__(
                self, event, context, env: environment.Environment, sub
            ) -> None:
                self.event = event
                self.context = context
                self.env = env
                self.sub = sub

            def __call__(self) -> Dict:
                try:
                    path_parameters = self.event["pathParameters"]
                    planid = path_parameters["planID"]
                    planstateid = path_parameters["planstateID"]

                    db = self.env.get_database()
                    plan_details = db.plans.find_one(
                        {"_id": ObjectId(planid)},
                        {"_id": 0, "ownedBy": 1, "history": 1},
                    )

                    if plan_details:
                        if plan_details["ownedBy"] == self.sub:
                            if ObjectId(planstateid) in plan_details["history"]:
                                planstate = db.planstates.find_one(
                                    {"_id": ObjectId(planstateid)},
                                    {"_id": 0},
                                )

                                if planstate:
                                    print("Found planstate with id", planstateid)
                                    return responses.ok_200(planstate)
                                else:
                                    print(
                                        f"Planstate with id {planstateid} not found",
                                        planstate,
                                    )
                                    return responses.gone_410()
                            else:
                                print(
                                    "Requested Planstate not in plan history",
                                    planstateid,
                                    plan_details["history"],
                                )
                                return responses.gone_410()
                        else:
                            print(
                                "ownedBy doesn't match sub",
                                plan_details["ownedBy"],
                                self.sub,
                            )
                            return responses.unauthorized_401()
                    else:
                        print(f"Plan with id {planid} not found", plan_details)
                        return responses.gone_410()

                except Exception as e:
                    print("Exception during GET Planstate:", e)
                    return responses.internal_server_error_500()

        children = {POST: PostPlanstate, GET: GetPlanstate}

    children = {
        "/api/_user": UserEndpoints,
        "/api/_plans": PlanEndpoints,
        "/api/_plans/{planID}": PlanEndpoints,
        "/api/_links": LinkEndpoints,
        "/api/_links/{shortlink}": LinkEndpoints,
        "/api/_plans/{planID}/_planstates": PlanstateEndpoints,
        "/api/_plans/{planID}/_planstates/{planstateID}": PlanstateEndpoints,
    }
