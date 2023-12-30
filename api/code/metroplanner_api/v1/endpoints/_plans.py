from fastapi import APIRouter, Request, HTTPException, Depends
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId
import random

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.post("", include_in_schema=False, status_code=201)
@router.post("/", status_code=201)
def post_plan(
    plan_data: type_definitions.CreatePlan, req: Request, sub: str = Depends(check_auth)
) -> type_definitions.PlanID:
    print("Received request to create a new plan. Validating JSON data...")
    print("Data successfully validated:", plan_data)

    db = ENV.database

    new_plan_data = {
        "planName": plan_data.plan_name,
        "planDescription": plan_data.plan_description,
        "forkedFrom": None,
        "deleted": None,
        "createdAt": (now := datetime.now().isoformat()),
        "lastModifiedAt": now,
        "likeCount": 0,
        "ownedBy": sub,
        "colorTheme": (theme := "colorful-dl"),
        "currentNumberOfEdges": 0,
        "currentNumberOfLines": 0,
        "currentNumberOfNodes": 0,
        "currentNumberOfLabels": 0,
    }

    print("initial data for new plan:", new_plan_data)

    if fork_from := plan_data.forkFrom:
        print("Plan is to be forked from", fork_from)
        link_is_active = False
        planstate_id = None
        if isinstance(fork_from, type_definitions.ForkFromShortlink):
            link_data = db.links.find_one({"_id": fork_from.shortlink})

            if link_data:
                planid = link_data["plan"]
            else:
                raise responses.gone_410()
            if link_data.get("active"):
                link_is_active = True
        else:
            # ForkFromPrivatePlan
            planid = BsonObjectId(fork_from.plan_id)
            if fork_from.planstate_id:
                planstate_id = BsonObjectId(fork_from.planstate_id)

        plan_details = db.plans.find_one(
            {
                "_id": planid,
            },
        )

        if plan_details and (link_is_active or sub == plan_details["ownedBy"]):
            planstate_id = planstate_id or plan_details["currentState"]

            planstate = db.planstates.find_one(
                {
                    "_id": planstate_id,
                },
                {
                    "_id": 0,
                },
            )

            if planstate:
                insert_planstate_res = db.planstates.insert_one(planstate)
                new_plan_data["currentNumberOfEdges"] = planstate["numberOfEdges"]
                new_plan_data["currentNumberOfLines"] = planstate["numberOfLines"]
                new_plan_data["currentNumberOfNodes"] = planstate["numberOfNodes"]
                new_plan_data["currentNumberOfLabels"] = planstate["numberOfLabels"]
                new_plan_data["colorTheme"] = plan_details["colorTheme"]
            else:
                raise responses.gone_410()
        else:
            raise responses.gone_410()
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
        new_planstateid := insert_planstate_res.inserted_id
    )
    new_plan_data["history"] = [new_planstateid]

    insert_res = db.plans.insert_one(new_plan_data)
    print("After insertion, this is the result:", insert_res)

    new_plan_id = insert_res.inserted_id
    Σ = "abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ3456789-"
    db.links.insert_one(
        {
            "_id": "".join([random.choice(Σ) for _ in range(8)]),
            "plan": new_plan_id,
            "active": True,
        }
    )

    return {"planId": str(new_plan_id)}


@router.patch("/{plan_id}")
def patch_plan(
    plan_id: type_definitions.ObjectId,
    plan_data: type_definitions.UpdatePlan,
    req: Request,
    sub: str = Depends(check_auth),
) -> type_definitions.PlanInDB:
    db = ENV.database
    plan_details = db.plans.find_one(
        {
            "_id": plan_id,
        },
        {
            "_id": 0,
            "ownedBy": 1,
        },
    )

    if plan_details["ownedBy"] == sub:
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
                new_id = BsonObjectId(plan_data["currentState"])
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
                set_data[k] = plan_data[k]

        set_data["lastModifiedAt"] = datetime.now().isoformat()

        db.plans.update_one(
            {
                "_id": plan_id,
            },
            {
                "$set": set_data,
            },
        )
    else:
        return responses.unauthorized_401()


@router.get("/{plan_id}")
def get_plan(
    plan_id, req: Request, sub: str = Depends(check_auth)
) -> type_definitions.PlanPrivateViewExtended:
    db = ENV.database
    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {
            "_id": 0,
        },
    )

    print("Found plan Details: ", plan_details)
    if plan_details:
        if plan_details["ownedBy"] == sub:
            if plan_details.get("deleted", None) is not None:
                # plan has been deleted
                raise responses.gone_410()

            if forked_from := plan_details["forkedFrom"]:
                plan_details["forkedFrom"] = str(forked_from)
            if current_state := plan_details["currentState"]:
                plan_details["currentState"] = str(current_state)
            if isinstance(
                current_colortheme := plan_details["colorTheme"],
                BsonObjectId,
            ):
                plan_details["colorTheme"] = str(current_colortheme)

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
                db.links.find({"plan": BsonObjectId(plan_id)}, {"plan": 0})
            )

            shortlinks_with_stats = []

            for shortlink in shortlinks:
                if shortlink["active"]:
                    print("Shortlink: ", shortlink)
                    shortlink_stats = db.stats.find_one(
                        {
                            "_id": {
                                "plan": BsonObjectId(plan_id),
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

            return plan_details
        else:
            raise responses.unauthorized_401()
    else:
        raise responses.gone_410()


@router.delete("/{plan_id}", status_code=204)
def delete_plan(
    plan_id: type_definitions.ObjectId, req: Request, sub: str = Depends(check_auth)
):
    db = ENV.database
    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {
            "_id": 0,
            "ownedBy": 1,
            "deleted": 1,
        },
    )

    print("Found plan Details: ", plan_details)
    if plan_details:
        if plan_details["ownedBy"] == sub:
            if plan_details.get("deleted", None) is not None:
                raise responses.gone_410()
            db.plans.update_one(
                {"_id": plan_id}, {"$set": {"deleted": datetime.now().isoformat()}}
            )

        shortlinks = list(db.links.find({"plan": plan_id}))

        for shortlink in shortlinks:
            print("Shortlink", shortlink, "will be removed")
            db.links.delete_one({"_id": shortlink["_id"]})
    else:
        raise responses.gone_410()
