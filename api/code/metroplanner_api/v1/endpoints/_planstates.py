from fastapi import APIRouter, Request, HTTPException, Depends, Response
from datetime import datetime
from bson.objectid import ObjectId as BsonObjectId

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.post("/_plans/{plan_id}/_planstates", status_code=201)
def post_planstate(
    plan_id,
    planstate_data: type_definitions.CreatePlanstate,
    sub: str = Depends(check_auth),
    make_current: bool = False,
) -> type_definitions.PlanstatePrivatePostResponse:
    db = ENV.database
    user_data = db.users.find_one({'sub': sub})
    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {
            "_id": 0,
            "ownedBy": 1,
        },
    )

    if user_data and plan_details:
        if plan_details["ownedBy"] == user_data['_id']:
            number_of_edges = 0
            for ln in planstate_data["lines"]:
                for cons in ln["connections"]:
                    number_of_edges += len(cons["nodes"])

            planstate_data["numberOfEdges"] = number_of_edges
            planstate_data["numberOfLines"] = len(planstate_data["lines"])
            planstate_data["numberOfNodes"] = len(planstate_data["nodes"])
            planstate_data["numberOfLabels"] = len(planstate_data["labels"])

            planstate_data["createdAt"] = (now := datetime.now().isoformat())

            created_result = db.planstates.insert_one(planstate_data)
            print("Created planstate:", created_result)

            set_plan_data = {
                "lastModifiedAt": now,
            }

            if make_current:
                if planstate_data.make_current:
                    set_plan_data["currentState"] = created_result.inserted_id
                    set_plan_data["currentNumberOfEdges"] = planstate_data[
                        "numberOfEdges"
                    ]
                    set_plan_data["currentNumberOfLines"] = planstate_data[
                        "numberOfLines"
                    ]
                    set_plan_data["currentNumberOfNodes"] = planstate_data[
                        "numberOfNodes"
                    ]
                    set_plan_data["currentNumberOfLabels"] = planstate_data[
                        "numberOfLabels"
                    ]

            db.plans.update_one(
                {"_id": BsonObjectId(plan_id)},
                {
                    "$push": {
                        "history": created_result.inserted_id,
                    },
                    "$set": set_plan_data,
                },
            )

            return {"planstateId": str(created_result.inserted_id)} #, **planstate_data}
        else:
            raise responses.unauthorized_401()
    else:
        raise responses.bad_request_400()


@router.get("/_plans/{plan_id}/_planstates/{planstate_id}")
def get_planstate(
    plan_id, planstate_id, req: Request, sub: str = Depends(check_auth)
) -> type_definitions.PlanstatePrivateGetResponse:
    db = ENV.database
    user_data = db.users.find_one({"sub": sub})

    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {"_id": 0, "ownedBy": 1, "history": 1},
    )

    if user_data and plan_details:
        if plan_details["ownedBy"] == user_data["_id"]:
            if BsonObjectId(planstate_id) in plan_details["history"]:
                planstate = db.planstates.find_one(
                    {"_id": BsonObjectId(planstate_id)},
                    {"_id": 0},
                )

                if planstate:
                    print("Found planstate with id", planstate_id)
                    return planstate
                else:
                    print(
                        f"Planstate with id {planstate_id} not found",
                        planstate,
                    )
                    raise responses.gone_410()
            else:
                print(
                    "Requested Planstate not in plan history",
                    planstate_id,
                    plan_details["history"],
                )
                raise responses.gone_410()
        else:
            print(
                "ownedBy doesn't match user id _id",
                plan_details["ownedBy"],
                sub,
                user_data["_id"],
            )
            raise responses.unauthorized_401()
    else:
        print(f"Plan with id {plan_id} not found", plan_details)
        raise responses.gone_410()
