from fastapi import APIRouter, Request, HTTPException, Depends
from pymongo import ReturnDocument

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.get("/")
def get_user(
    request: Request, sub: str = Depends(check_auth)
) -> type_definitions.UserInDB:
    try:
        db = ENV.database
        user_result = db.users.find_one({"_id": sub})
        if user_result:
            print("Found User Profile:", user_result)

            plans_created = list(
                db.plans.find(
                    {"ownedBy": sub},
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
                    "_id": sub,
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
        raise responses.internal_server_error_500()


@router.patch("/")
def patch_user(
    user_data: type_definitions.UpdateUser, req: Request, sub: str = Depends(check_auth)
) -> type_definitions.UserInDB:
    try:
        # jsonschema.validate(instance=data, schema=request_schemas.patch_user_schema)
        db = ENV.database
        updated_result = db.users.find_one_and_update(
            {
                "_id": sub,
            },
            {"$set": user_data},
            return_document=ReturnDocument.AFTER,
        )
        print("Updated result:", updated_result)
        if updated_result:
            return responses.ok_200(updated_result)
        else:
            return responses.internal_server_error_500()
    except KeyError as e:
        print(e)
        return responses.bad_request_400()
    except Exception as e:
        print(e)
        return responses.internal_server_error_500()
