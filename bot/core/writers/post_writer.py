import json
from typing import List

from bot.core.entities.entities import Post
from bot.core.writers.utils import handle_folder_and_file


class PostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return {
                "id": obj.id,
                "title": obj.title,
                "description": obj.description,
                "user": obj.user.id
            }
        return super().default(obj)


def write_post_result(
        posts: List[Post],
        folder: str = "result",
        filename: str = "post_result.json"
) -> None:
    """Write result for post"""
    result_path = handle_folder_and_file(folder, filename)

    with open(result_path, "a") as post_file:
        json.dump(posts, post_file, cls=PostEncoder, indent=4)
