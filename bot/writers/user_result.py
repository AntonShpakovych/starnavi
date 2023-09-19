import json
from typing import List

from bot.entities import User


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                "id": obj.id,
                "first_name": obj.first_name,
                "last_name": obj.last_name,
                "email": obj.email,
                "access": obj.access,
                "password": obj.password,
                "posts": [post.id for post in obj.posts]
            }
        return super().default(obj)


def write_user_result(users: List[User]) -> None:
    with open("user_result.json", "w+") as user_file:
        json.dump(users, user_file, cls=UserEncoder, indent=4)
