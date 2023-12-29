from fastapi import APIRouter, Request, HTTPException, Depends, Response
from datetime import datetime

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.post("", include_in_schema=False, status_code=201)
@router.post("/{plan_id}/_planstates")
def post_planstate(
    plan_id,
    planstate_data: type_definitions.CreatePlanstate,
    req: Request,
    sub: str = Depends(check_auth),
) -> type_definitions.PlanInDB:
    # make_current = "makeCurrent" in self.event.get("queryStringParameters", {})
    db = ENV.database
    plan_details = db.plans.find_one(
        {"_id": type_definitions.ObjectId(plan_id)},
        {
            "_id": 0,
            "ownedBy": 1,
        },
    )

    if plan_details["ownedBy"] == sub:
        number_of_edges = 0

        for ln in planstate_data["lines"]:
            for cons in ln["connections"]:
                number_of_edges += len(cons["nodes"])

        planstate_data["numberOfEdges"] = number_of_edges
        planstate_data["numberOfLines"] = len(planstate_data["lines"])
        planstate_data["numberOfNodes"] = len(planstate_data["nodes"])
        planstate_data["numberOfLabels"] = len(planstate_data["labels"])

        planstate_data["createdAt"] = datetime.now().isoformat()

        created_result = db.planstates.insert_one(planstate_data)
        print("Created planstate:", created_result)

        set_plan_data = {
            "lastModifiedAt": planstate_data["createdAt"],
        }

        if planstate_data.make_current:
            set_plan_data["currentState"] = (created_result.inserted_id,)
            set_plan_data["numberOfEdges"] = planstate_data["numberOfEdges"]
            set_plan_data["numberOfLines"] = planstate_data["numberOfLines"]
            set_plan_data["numberOfNodes"] = planstate_data["numberOfNodes"]
            set_plan_data["numberOfLabels"] = planstate_data["numberOfLabels"]

        db.plans.update_one(
            {"_id": type_definitions.ObjectId(plan_id)},
            {
                "$push": {
                    "history": created_result.inserted_id,
                },
                "$set": set_plan_data,
            },
        )

        return {"planstateID": str(created_result.inserted_id), **planstate_data}
    else:
        raise responses.unauthorized_401()


@router.get("/{plan_id}/_planstates/{planstate_id}")
def get_planstate(
    plan_id, planstate_id, req: Request, sub: str = Depends(check_auth)
) -> type_definitions.PlanstateInDB:
    db = ENV.database
    plan_details = db.plans.find_one(
        {"_id": type_definitions.ObjectId(plan_id)},
        {"_id": 0, "ownedBy": 1, "history": 1},
    )

    if plan_details:
        if plan_details["ownedBy"] == sub:
            if type_definitions.ObjectId(planstate_id) in plan_details["history"]:
                planstate = db.planstates.find_one(
                    {"_id": type_definitions.ObjectId(planstate_id)},
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
                "ownedBy doesn't match sub",
                plan_details["ownedBy"],
                sub,
            )
            raise responses.unauthorized_401()
    else:
        print(f"Plan with id {plan_id} not found", plan_details)
        raise responses.gone_410()
