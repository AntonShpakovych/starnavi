import random
from typing import List, Dict

import requests
from faker import Faker

from bot.entities import User, Post, Like


class UserAPIDispatcher:
    SIGN_UP_USER_URL: str = "http://localhost:8000/api/v1/user/"
    LOGIN_USER_URL: str = "http://localhost:8000/api/v1/user/token/"

    def __init__(self, number_of_users: int) -> None:
        self.number_of_users = number_of_users
        self.users = []

    def provide_users(self) -> List[User]:
        self._sign_up_users()
        self._login_users()

        return self.users

    def _sign_up_users(self) -> None:
        for _ in range(self.number_of_users):
            data = self._generate_random_user_data()
            response=requests.post(
                url=self.SIGN_UP_USER_URL,
                data=data
            ).json()
            user = User(id=response.get("id"), **data)
            self.users.append(user)

    def _login_users(self) -> None:
        for user in self.users:
            response = requests.post(
                url=self.LOGIN_USER_URL,
                data=user.login_credentials()
            ).json()
            user.access = response.get("access")

    @staticmethod
    def _generate_random_user_data():
        faker = Faker()
        return {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password()
        }


class PostAPIDispatcher:
    POST_CREATE_URL: str = "http://localhost:8000/api/v1/post/"

    def __init__(
            self,
            max_posts_per_user: int,
    ) -> None:
        self.max_posts_per_user = max_posts_per_user
        self.posts = []

    def provide_posts(self, users: List[User]):
        self._create_posts(users=users)

        return self.posts

    def _create_posts(
            self,
            users: List[User]
    ) -> None:
        for user in users:
            num_posts = random.randint(1, self.max_posts_per_user)

            for _ in range(num_posts):
                data = self._generate_random_post_data()
                response = requests.post(
                    url=self.POST_CREATE_URL,
                    data=data,
                    headers=user.jwt_authentication_headers()
                ).json()
                post = Post(id=response.get("id"), user=user, **data)
                user.posts.append(post)
                self.posts.append(post)

    @staticmethod
    def _generate_random_post_data() -> Dict[str, str]:
        faker = Faker()
        return {
            "title": faker.name(),
            "description": faker.text()
        }


class LikeAPIDispatcher:
    URL_LIKE_BASE: str = "http://localhost:8000/api/v1/post"

    def __init__(self, max_likes_per_user: int) -> None:
        self.max_likes_per_user = max_likes_per_user

    def provide_likes(
            self,
            users: List[User],
            posts: List[Post]
    ) -> List[Like]:
        likes = []

        for user in users:
            num_likes = random.randint(1, self.max_likes_per_user)

            for _ in range(num_likes):
                post = random.choice(posts)
                data = {"likes": likes, "user": user, "post": post}

                if Like.is_already_exists(**data):
                    Like.del_like_object(**data)
                else:
                    response = requests.post(
                        url=f"{self.URL_LIKE_BASE}/{post.id}/like/",
                        headers=user.jwt_authentication_headers()
                    ).json()

                    like = Like(**response)
                    likes.append(like)
        return likes
