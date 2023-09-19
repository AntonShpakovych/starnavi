import json
from typing import List

from bot.entities import Post


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


def write_post_result(posts: List[Post]) -> None:
    with open("post_result.json", "w+") as post_file:
        json.dump(posts, post_file, cls=PostEncoder, indent=4)
