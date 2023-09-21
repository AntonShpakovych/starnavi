from drf_spectacular.utils import extend_schema

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import (
    UserSerializer,
    UserManageSerializer,
    UserActivitySerializer
)


@extend_schema(tags=["User"])
class UserCreateView(generics.CreateAPIView):
    """This api view create user"""
    serializer_class = UserSerializer


@extend_schema(tags=["User"])
class ManageUserView(generics.RetrieveUpdateAPIView):
    """This api view handle information(update) for 'request.user'"""
    serializer_class = UserManageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


@extend_schema(tags=["User"])
class UserActivityView(generics.RetrieveAPIView):
    """This api view show activities for 'request.user'"""
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user
