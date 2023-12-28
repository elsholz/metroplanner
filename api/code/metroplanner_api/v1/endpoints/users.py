from fastapi import APIRouter

from ... import type_definitions
from ... import responses
from ...environment import check_auth, ENV


router = APIRouter()


@router.get("/{user_id}")
def get_user(user_id) -> type_definitions.User:
    try:
        db = ENV.database
        user_result = db.users.find_one({"_id": user_id})
        print("User result:", user_result)
        if user_result:
            user_data = {
                "bio": user_result["bio"],
                "displayName": user_result["displayName"],
                "profilePicture": user_result["profilePicture"],
                "public": (public := user_result["public"]),
            }
            if public:
                # TODO collect plans created
                # TODO collect plans liked
                print("User Profile is public")
                return responses.ok(user_data)
            else:
                print("User Profile is not public")
                raise responses.forbidden_403()

        else:
            raise responses.gone_410()
    except Exception as e:
        raise responses.internal_server_error_500()
