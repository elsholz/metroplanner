from fastapi import APIRouter, Request, HTTPException, Depends
from datetime import datetime, timedelta
from bson.objectid import ObjectId as BsonObjectId
import random

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.post("/_plans", include_in_schema=False, status_code=201)
@router.post("/_plans/", status_code=201)
def post_plan(
    plan_data: type_definitions.PlanPrivatePostRequest,
    sub: str = Depends(check_auth),
) -> type_definitions.PlanPrivatePostResponse:
    print("Received request to create a new plan. Validating JSON data...")
    print("Data successfully validated:", plan_data)

    db = ENV.database
    user_data = db.users.find_one({"sub": sub})

    if user_data:
        user_id = user_data["_id"]
        new_plan_data = {
            "plan_name": plan_data.plan_name,
            "plan_description": plan_data.plan_description,
            "forked_from": None,
            "deleted": None,
            "created_at": (now := datetime.now().isoformat()),
            "last_modified_at": now,
            "like_count": 0,
            "owned_by": user_id,
            "color_theme": (theme := "colorful-dl"),
            "current_number_of_edges": 0,
            "current_number_of_lines": 0,
            "current_number_of_nodes": 0,
            "current_number_of_labels": 0,
        }

        print("initial data for new plan:", new_plan_data)

        if fork_from := plan_data.forkFrom:
            print("Plan is to be forked from", fork_from)
            link_is_active = False
            planstate_id = None
            planid = None

            if isinstance(
                fork_from, type_definitions.PlanPrivatePostRequest.ForkFromShortlink
            ):
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

            new_plan_data["forked_from"] = planid

            if plan_details and (link_is_active or user_id == plan_details["owned_by"]):
                planstate_id = planstate_id or plan_details["current_state"]

                planstate = db.planstates.find_one(
                    {
                        "_id": planstate_id,
                    },
                    {
                        "_id": 0,
                    },
                )

                planstate["created_at"] = now

                if planstate:
                    insert_planstate_res = db.planstates.insert_one(planstate)
                    new_plan_data["current_number_of_edges"] = planstate[
                        "number_of_edges"
                    ]
                    new_plan_data["current_number_of_lines"] = planstate[
                        "number_of_lines"
                    ]
                    new_plan_data["current_number_of_nodes"] = planstate[
                        "number_of_nodes"
                    ]
                    new_plan_data["current_number_of_labels"] = planstate[
                        "number_of_labels"
                    ]
                    new_plan_data["color_theme"] = plan_details["color_theme"]
                else:
                    raise responses.gone_410()
            else:
                raise responses.gone_410()
        else:
            print("Creating plan from scratch")
            insert_planstate_res = db.planstates.insert_one(
                {
                    "created_at": now,
                    "number_of_edges": 0,
                    "number_of_lines": 0,
                    "number_of_nodes": 0,
                    "number_of_labels": 0,
                    "nodes": {},
                    "lines": {},
                    "independent_labels": {},
                    "global_offset_x": 0,
                    "global_offset_y": 0,
                    "plan_height": 10,
                    "plan_width": 10,
                    "color_theme": theme,
                }
            )

        print("Created plan, result:", insert_planstate_res)
        new_plan_data["current_state"] = (
            new_planstateid := insert_planstate_res.inserted_id
        )
        new_plan_data["history"] = [new_planstateid]

        insert_res = db.plans.insert_one(new_plan_data)

        new_plan_id = insert_res.inserted_id
        Σ = "abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ3456789-"
        shortlink = "".join([random.choice(Σ) for _ in range(8)])

        db.links.insert_one(
            {
                "_id": shortlink,
                "plan": new_plan_id,
                "active": True,
            }
        )

        return {
            "planId": str(new_plan_id)
        }  # , 'primary_shortlink': shortlink, 'shortlinks': [shortlink], **new_plan_data}
    else:
        raise responses.bad_request_400()


@router.patch("/_plans/{plan_id}")
def patch_plan(
    plan_id: type_definitions.ObjectId,
    plan_data: type_definitions.PlanPrivatePatchRequest,
    sub: str = Depends(check_auth),
) -> type_definitions.PlanPrivatePatchResponse:
    db = ENV.database
    user_data = db.users.find_one({"sub": sub})

    plan_details = db.plans.find_one(
        {
            "_id": BsonObjectId(plan_id),
        },
        {
            "_id": 0,
            "owned_by": 1,
        },
    )

    if user_data and plan_details:
        if plan_details["owned_by"] == user_data["_id"]:
            set_data = plan_data.get_existing_fields()
            print("Data to set:", set_data)

            if not set_data:
                raise responses.bad_request_400()

            new_data = {
                "last_modified_at": datetime.now().isoformat(),
            }

            if new_id := set_data.get("current_state", None):
                new_id = BsonObjectId(new_id)
                get_planstate_result = db.planstates.find_one(
                    {"_id": new_id}, {"_id": 1}
                )
                if get_planstate_result:
                    print(
                        "Found corresponding planstate!",
                        get_planstate_result,
                    )
                    new_data["current_state"] = new_id
                else:
                    print(
                        "Did not find corresponding planstate!",
                        get_planstate_result,
                    )
                    raise responses.bad_request_400()

            if "plan_name" in set_data:
                new_data["plan_name"] = set_data["plan_name"]
            if "plan_description" in set_data:
                new_data["plan_description"] = set_data["plan_description"]

            db.plans.update_one(
                {
                    "_id": BsonObjectId(plan_id),
                },
                {
                    "$set": new_data,
                },
            )

            return new_data
        else:
            raise responses.unauthorized_401()
    else:
        raise responses.gone_410()


@router.get("/_plans/{plan_id}")
def get_plan(
    plan_id: type_definitions.ObjectId, sub: str = Depends(check_auth)
) -> type_definitions.PlanPrivateGetResponse:
    db = ENV.database
    user_data = db.users.find_one({"sub": sub})
    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {
            "_id": 0,
        },
    )

    print("Found plan Details: ", plan_details)
    if user_data and plan_details:
        if plan_details["owned_by"] == user_data["_id"]:
            if plan_details.get("deleted", None) is not None:
                raise responses.gone_410()
            if forked_from := plan_details["forked_from"]:
                plan_details["forked_from"] = str(forked_from)
            if isinstance(
                current_colortheme := plan_details["color_theme"],
                BsonObjectId,
            ):
                plan_details["color_theme"] = str(current_colortheme)

            plan_details["current_state"] = str(plan_details["current_state"])

            states = []
            for planstateid in plan_details["history"]:
                planstate_details = db.planstates.find_one(
                    {"_id": planstateid},
                    {
                        "_id": 0,
                        "created_at": 1,
                        "number_of_edges": 1,
                        "number_of_lines": 1,
                        "number_of_nodes": 1,
                        "number_of_labels": 1,
                    },
                )
                if not planstate_details:
                    print(
                        f"Warning: Planstate details for planstateid {planstateid} not found."
                    )
                    continue
                planstate_details["planstate_id"] = str(planstateid)
                print("Found planstate details:", planstate_details)
                states.append(planstate_details)

            print("states:", states)
            plan_details["history"] = states

            shortlinks = list(
                db.links.find({"plan": BsonObjectId(plan_id)}, {"plan": 0, "_id": 1})
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

                        views = shortlink_stats["views"]
                        per_hour, per_day, per_month = [], [], []
                        now = datetime.now()

                        day_aggregate = 0
                        month_aggregate = 0

                        for hour in range(24 * 360):
                            time_to_get = now - timedelta(hours=hour)
                            time_to_hour = time_to_get.isoformat().split(":")[0]

                            ts = int(time_to_get.timestamp()) * 1000

                            # ts_hour = int(
                            #     datetime(*time_to_get.timetuple()[:4]).timestamp()
                            # )
                            # ts_day = int(
                            #     datetime(*time_to_get.timetuple()[:3]).timestamp()
                            # )
                            # ts_month = int(
                            #     datetime(*time_to_get.timetuple()[:3]).timestamp()
                            # )

                            v = views.get(time_to_hour, 0)
                            day_aggregate += v
                            month_aggregate += v

                            if hour < 25:
                                per_hour.append((ts, v))

                            if hour < 25 * 30 and not hour % 24:
                                per_day.append((ts, day_aggregate))
                                day_aggregate = 0

                            if not hour % (24 * 30):
                                per_month.append((ts, month_aggregate))
                                month_aggregate = 0

                        shortlink_stats["per_hour"] = list(reversed(per_hour))
                        shortlink_stats["per_day"] = list(reversed(per_day))
                        shortlink_stats["per_month"] = list(reversed(per_month))

                        del shortlink_stats["views"]

                        shortlink["stats"] = shortlink_stats

                    else:
                        shortlink["stats"] = {"totalCount": 0, "views": {}}
                    shortlink["shortlink"] = shortlink["_id"]
                    del shortlink["active"]
                    del shortlink["_id"]
                    shortlinks_with_stats.append(shortlink)

            print("Shortlinks:", shortlinks_with_stats)

            plan_details["shortlinks"] = shortlinks_with_stats
            print("Plan Details:", plan_details)
            plan_details["owned_by"] = str(plan_details["owned_by"])

            return plan_details
        else:
            raise responses.unauthorized_401()
    else:
        raise responses.gone_410()


@router.delete("/_plans/{plan_id}", status_code=204)
def delete_plan(plan_id: type_definitions.ObjectId, sub: str = Depends(check_auth)):
    db = ENV.database
    user_data = db.users.find_one({"sub": sub})
    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {
            "_id": 0,
            "owned_by": 1,
            "deleted": 1,
        },
    )

    print("Found plan Details: ", plan_details)
    if user_data and plan_details:
        if plan_details["owned_by"] == user_data["_id"]:
            if plan_details.get("deleted", None) is not None:
                raise responses.gone_410()
            db.plans.update_one(
                {"_id": BsonObjectId(plan_id)},
                {"$set": {"deleted": datetime.now().isoformat()}},
            )

        shortlinks = list(db.links.find({"plan": plan_id}))

        for shortlink in shortlinks:
            print("Shortlink", shortlink, "will be removed")
            db.links.delete_one({"_id": shortlink["_id"]})
    else:
        raise responses.gone_410()
