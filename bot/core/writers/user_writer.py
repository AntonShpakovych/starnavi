import json
from typing import List

from bot.core.entities.entities import User
from bot.core.writers.utils import handle_folder_and_file


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


def write_user_result(
        users: List[User],
        folder: str = "result",
        filename: str = "user_result.json"
) -> None:
    """Write result for user"""
    result_path = handle_folder_and_file(folder, filename)

    with open(result_path, "a") as user_file:
        json.dump(users, user_file, cls=UserEncoder, indent=4)
