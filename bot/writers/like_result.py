import json
from typing import List

from bot.entities import Like


class LikeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Like):
            return {
                "id": obj.id,
                "user": obj.user,
                "post": obj.post
            }
        return super().default(obj)


def write_like_result(likes: List[Like]) -> None:
    with open("like_result.json", "w") as like_file:
        json.dump(likes, like_file, cls=LikeEncoder, indent=4)
