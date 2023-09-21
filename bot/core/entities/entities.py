from typing import List, Dict


class User:
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            email: str,
            password: str,
            access: str = None,
            posts: List['Post'] = None
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.access = access
        self.password = password
        self.posts = posts or []

    def login_credentials(self) -> Dict[str, str]:
        """Provide data for generate access token"""
        return {"email": self.email, "password": self.password}

    def jwt_authentication_headers(self) -> Dict[str, str]:
        """Provide header for jwt-authentication"""
        return {"Authorization": f"Bearer {self.access}"}


class Post:
    def __init__(
            self,
            id: int,
            title: str,
            description: str,
            user: User,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.user = user


class Like:
    def __init__(
            self,
            id: int,
            user: int,
            post: int
    ) -> None:
        self.id = id
        self.user = user
        self.post = post

    @classmethod
    def is_already_exists(
            cls,
            likes: List["Like"],
            user: User,
            post: Post
    ) -> bool:
        """Check if user likes the post"""
        for like in likes:
            if like.user == user.id and like.post == post.id:
                return True
        return False

    @classmethod
    def del_like_object(
            cls,
            likes: List["Like"],
            user: User,
            post: Post
    ) -> None:
        """Delete a like if a user likes a post he has already liked"""
        for like in likes:
            if like.user == user.id and like.post == post.id:
                del like
