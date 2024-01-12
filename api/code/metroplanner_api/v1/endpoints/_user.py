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
                {"ownedBy": user_result['_id']},
                {
                    "planName": 1,
                    "planDescription": 1,
                    "_id": 1,
                    "planShortlink": 1,  # TODO: Primary Shorlink
                    "primaryShortlink": 1,
                    "public": 1,
                    "deleted": 1,
                },
            )
            if not p.get("deleted", False)
        )

        for p in plans_created:
            p["planId"] = str(p["_id"])

            if "planShortlink" not in p:
                plan_links = db.links.find({"plan": p["_id"]})
                if plan_links:
                    p["shortlinks"] = [{"shortlink": p["_id"]} for p in plan_links]
            if "primaryShortlink" not in p:
                p["primaryShortlink"] = p.get("shortlinks", [{}])[0].get(
                    "shortlink", None
                )

            del p["_id"]

        likes = []

        for liked_planid in user_result["likesGiven"]:
            print("Get shortlink for plan with id", liked_planid)
            liked_plan_shortlink = db.links.find_one({"plan": liked_planid}, {"_id": 1})
            print("Liked plan Shortlink:", liked_plan_shortlink)
            likes.append(liked_plan_shortlink["_id"])
        user_result["likesGiven"] = likes

        print("plans as list: ", plans_created)
        user_result["plansCreated"] = plans_created

        return user_result
    else:
        print("User profile not found, creating profile.")
        user_creation_result = db.users.insert_one(
            user_data := {
                "sub": sub,
                "displayName": "",
                "public": True,
                "profileViews": 0,
                "likesGiven": [],
                "profilePicture": None,
                "bio": "",
                "plansCreated" : [],
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
    new_user_data = {}

    if 'profile_picture' in set_data:
        new_user_data['profilePicture'] = set_data['profile_picture']
    if 'bio' in set_data:
        new_user_data['bio'] = set_data['bio']
    if 'display_name' in set_data:
        new_user_data['displayName'] = set_data['display_name']
    if 'public' in set_data:
        new_user_data['public'] = set_data['public']

    print('Existing fields', new_user_data)

    updated_result = db.users.find_one_and_update(
        {
            "sub": sub,
        },
        {"$set": new_user_data},
        return_document=ReturnDocument.AFTER,
    )
    print("Updated result:", updated_result)
    if updated_result:
        return updated_result
    else:
        raise responses.internal_server_error_500()
