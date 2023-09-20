SCHEMA = {
    "type": "object",
    "properties": {
        "number_of_users": {
            "type": "integer"
        },
        "max_posts_per_user": {
            "type": "integer"
        },
        "max_likes_per_user": {
            "type": "integer"
        }
    },
    "required": ["number_of_users", "max_posts_per_user", "max_likes_per_user"],
    "additionalProperties": False
}
