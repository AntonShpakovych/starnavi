from typing import Dict, List

from bot.core.dispatchers.api_dispatchers import (
    UserAPIDispatcher,
    PostAPIDispatcher,
    LikeAPIDispatcher
)
from bot.core.entities.entities import Like, User, Post
from bot.core.readers.config_reader import ConfigReader

from bot.core.writers.like_writer import write_like_result
from bot.core.writers.post_writer import write_post_result
from bot.core.writers.user_writer import write_user_result


class StarNaviBot:
    """StarNaviBot is a bot designed to demonstrate API interaction."""
    def __init__(self, path_to_config: str) -> None:
        self.settings: Dict[str, int] = self.set_settings(
            path_to_config=path_to_config
        )

    def show_api_work(self) -> None:
        """
        Demonstrates API interactions by creating
        users, posts, and likes and collecting the results.
        """
        user_dispatcher = self._initialize_user_dispatcher()
        post_dispatcher = self._initialize_post_dispatcher()
        like_dispatcher = self._initialize_like_dispatcher()

        users = user_dispatcher.provide_users()
        posts = post_dispatcher.provide_posts(users=users)
        likes = like_dispatcher.provide_likes(users=users, posts=posts)

        self._collect_results(
            users=users,
            posts=posts,
            likes=likes
        )

    @staticmethod
    def _collect_results(
            users: List[User],
            posts: List[Post],
            likes: List[Like]
    ) -> None:
        """Collects and writes the results of API interactions."""
        write_user_result(users=users)
        write_post_result(posts=posts)
        write_like_result(likes=likes)

    def _initialize_user_dispatcher(self) -> UserAPIDispatcher:
        """Initializes a UserAPIDispatcher instance based on the bot's settings."""
        return UserAPIDispatcher(
            number_of_users=self.settings["number_of_users"]
        )

    def _initialize_post_dispatcher(self) -> PostAPIDispatcher:
        """Initializes a PostAPIDispatcher instance based on the bot's settings."""
        return PostAPIDispatcher(
            max_posts_per_user=self.settings["max_posts_per_user"],
        )

    def _initialize_like_dispatcher(self) -> LikeAPIDispatcher:
        """Initializes a LikeAPIDispatcher instance based on the bot's settings."""
        return LikeAPIDispatcher(
            max_likes_per_user=self.settings["max_likes_per_user"]
        )

    @staticmethod
    def set_settings(path_to_config: str) -> Dict[str, int]:
        """Reads and sets bot settings from a configuration file."""
        return ConfigReader(
            path_to_config=path_to_config
        ).handle_config()
