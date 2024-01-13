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
) -> type_definitions.PlanstatePrivatePostResponse:
    db = ENV.database
    user_data = db.users.find_one({"sub": sub})
    plan_details = db.plans.find_one(
        {"_id": BsonObjectId(plan_id)},
        {
            "_id": 0,
            "owned_by": 1,
        },
    )

    if user_data and plan_details:
        if plan_details["owned_by"] == user_data["_id"]:
            number_of_edges = 0
            set_planstate_data = {}

            for ln_id, ln in planstate_data.lines.items():
                for cons in ln.connections:
                    number_of_edges += (len(cons.nodes) or 1) - 1

            set_planstate_data["number_of_edges"] = number_of_edges
            set_planstate_data["number_of_lines"] = len(planstate_data.lines)
            set_planstate_data["number_of_nodes"] = len(planstate_data.nodes)
            set_planstate_data["number_of_labels"] = len(
                planstate_data.independent_labels
            ) + len([True for n in planstate_data.nodes.values() if n.label.text])

            set_planstate_data["created_at"] = (now := datetime.now().isoformat())
            planstate_dumped_data = planstate_data.model_dump()

            created_result = db.planstates.insert_one(
                set_planstate_data
                | {
                    "lines": planstate_dumped_data["lines"],
                    "nodes": planstate_dumped_data["nodes"],
                    "independent_labels": planstate_dumped_data["independent_labels"],
                }
            )
            print("Created planstate:", created_result)

            set_plan_data = {
                "last_modified_at": now,
            }

            if planstate_data.make_current:
                set_plan_data["current_state"] = created_result.inserted_id
                set_plan_data["current_number_of_edges"] = set_planstate_data[
                    "number_of_edges"
                ]
                set_plan_data["current_number_of_lines"] = set_planstate_data[
                    "number_of_lines"
                ]
                set_plan_data["current_number_of_nodes"] = set_planstate_data[
                    "number_of_nodes"
                ]
                set_plan_data["current_number_of_labels"] = set_planstate_data[
                    "number_of_labels"
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

            return {
                "planstateId": str(created_result.inserted_id)
            }  # , **planstate_data}
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
        {"_id": 0, "owned_by": 1, "history": 1},
    )

    if user_data and plan_details:
        if plan_details["owned_by"] == user_data["_id"]:
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
