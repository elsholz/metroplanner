from fastapi import APIRouter
from bson.objectid import ObjectId
from json import loads

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV
import requests


router = APIRouter()


@router.get("/{user_id}")
def get_user(user_id) -> type_definitions.User:
    db = ENV.database
    try:
        user_id = ObjectId(user_id)
    except Exception:
        raise responses.bad_request_400()

    user_result = db.users.find_one({"_id": user_id})

    if user_result:
        sub = user_result['sub']

        print('sub:', sub)

        auth0_res = requests.get(
            f'https://{ENV.AUTH0_DOMAIN}/api/v2/users/{sub}',
            headers={
                "Authorization": f"Bearer {ENV.MGMT_API_ACCESS_TOKEN}"
            }
        )

        auth0_user = {}
        if auth0_res.status_code == 200:
            auth0_user = loads(auth0_res.content.decode())

        user_data = {
            "bio": user_result["bio"],
            "displayName": user_result.get("displayName", None) or auth0_user.get('nickname', None),
            "profilePicture": user_result.get("profilePicture", None) or auth0_user.get('picture', None), 
            # "public": (public := user_result["public"]), TODO
        }
            # if public: TODO: decide, whether private profiles should be possible.
            # TODO collect plans created
            # TODO collect plans liked
            # print("User Profile is public")

        plans_created = list(
            p
            for p in db.plans.find(
                {"ownedBy": user_id},
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

        user_data['plansCreated'] = plans_created

        return user_data

    else:
        raise responses.gone_410()
