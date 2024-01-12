from fastapi import APIRouter, Request, HTTPException, Depends
from pymongo import ReturnDocument

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.get("", include_in_schema=False)
@router.get("/")
def get_user(sub: str = Depends(check_auth)) -> type_definitions.UserPrivateGetResponse:
    db = ENV.database
    user_result = db.users.find_one({"sub": sub})
    if user_result:
        print("Found User Profile:", user_result)

        plans_created = list(
            p
            for p in db.plans.find(
                {"owned_by": user_result['_id']},
                {
                    "plan_name": 1,
                    "plan_description": 1,
                    "_id": 1,
                    "plan_shortlink": 1,  # TODO: Primary Shorlink
                    "primary_shortlink": 1,
                    "public": 1,
                    "deleted": 1,
                },
            )
            if not p.get("deleted", False)
        )

        for p in plans_created:
            p["planId"] = str(p["_id"])

            if "plan_shortlink" not in p:
                plan_links = db.links.find({"plan": p["_id"]})
                if plan_links:
                    p["shortlinks"] = [{"shortlink": p["_id"]} for p in plan_links]
            if "primary_shortlink" not in p:
                p["primary_shortlink"] = p.get("shortlinks", [{}])[0].get(
                    "shortlink", None
                )

            del p["_id"]

        likes = []

        for liked_planid in user_result["likes_given"]:
            print("Get shortlink for plan with id", liked_planid)
            liked_plan_shortlink = db.links.find_one({"plan": liked_planid}, {"_id": 1})
            print("Liked plan Shortlink:", liked_plan_shortlink)
            likes.append(liked_plan_shortlink["_id"])
        user_result["likes_given"] = likes

        print("plans as list: ", plans_created)
        user_result["plans_created"] = plans_created

        return user_result
    else:
        print("User profile not found, creating profile.")
        user_creation_result = db.users.insert_one(
            user_data := {
                "sub": sub,
                "display_name": "",
                "public": True,
                "profile_views": 0,
                "likes_given": [],
                "profile_picture": None,
                "bio": "",
                "plans_created" : [],
            }
        )

        print("User Creation result", user_creation_result)
        return user_data


@router.patch("", include_in_schema=False)
@router.patch("/")
def patch_user(
    user_data: type_definitions.UserPrivatePatchRequest, req: Request, sub: str = Depends(check_auth)
) -> type_definitions.UserPrivatePatchResponse:
    db = ENV.database
    set_data = user_data.get_existing_fields()

    print('Existing fields', set_data)

    updated_result = db.users.find_one_and_update(
        {
            "sub": sub,
        },
        {"$set": set_data},
        return_document=ReturnDocument.AFTER,
    )
    print("Updated result:", updated_result)
    if updated_result:
        return updated_result
    else:
        raise responses.internal_server_error_500()
