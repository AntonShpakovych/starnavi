import json
from typing import List

from bot.core.entities.entities import Like
from bot.core.writers.utils import handle_folder_and_file


class LikeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Like):
            return {
                "id": obj.id,
                "user": obj.user,
                "post": obj.post
            }
        return super().default(obj)


def write_like_result(
        likes: List[Like],
        folder: str = "result",
        filename: str = "like_result.json"
) -> None:
    """Write result for like"""
    result_path = handle_folder_and_file(folder, filename)

    with open(result_path, "a") as like_file:
        json.dump(likes, like_file, cls=LikeEncoder, indent=4)
