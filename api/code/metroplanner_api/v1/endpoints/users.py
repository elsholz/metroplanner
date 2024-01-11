from fastapi import APIRouter
from bson.objectid import ObjectId

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV
import requests


router = APIRouter()


@router.get("/{user_id}")
def get_user(user_id) -> type_definitions.User:
    db = ENV.database
    user_result = db.users.find_one({"_id": ObjectId(user_id)})
    print("User result:", user_result)
    if user_result:
        sub = user_result['sub']

        print('sub:', sub)

        auth0_user = requests.get(
            f'https://{ENV.AUTH0_DOMAIN}/api/v2/users/{sub}',
            headers={
                "Authorization": f"Bearer {ENV.MGMT_API_ACCESS_TOKEN}"
            }
        )

        print('auth0user:', auth0_user)
        print('content:', auth0_user.content)

        raise responses.not_acceptable_406()

        user_data = {
            "bio": user_result["bio"],
            "displayName": user_result["displayName"],
            "profilePicture": user_result["profilePicture"],
            "public": (public := user_result["public"]),
        }
        if True:
            # if public: TODO: decide, whether private profiles should be possible.
            # TODO collect plans created
            # TODO collect plans liked
            print("User Profile is public")
            return user_data
        else:
            print("User Profile is not public")
            raise responses.forbidden_403()

    else:
        raise responses.gone_410()
