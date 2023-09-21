from typing import Type

from django.db.models import QuerySet

from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from post.models import Post, PostLike
from post.permissions import IsOwnerOrIsAuthenticatedReadOnly
from post.serializers import (
    PostSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    PostLikeSerializer
)
from post.services.post_like_analytics_service import PostLikeAnalyticsService


@extend_schema(tags=["Post"])
class PostViewSet(viewsets.ModelViewSet):
    """This viewset handle all logic connected to 'Post'"""
    permission_classes = [IsOwnerOrIsAuthenticatedReadOnly]

    def get_queryset(self) -> QuerySet[Post]:
        if self.action == "retrieve":
            return Post.objects.prefetch_related("user", "likes")
        return Post.objects.all()

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostRetrieveSerializer
        return PostSerializer

    def perform_create(self, serializer: ModelSerializer) -> None:
        serializer.save(user=self.request.user)


@extend_schema(
    tags=["Post Like"],
)
class PostLikeView(views.APIView):
    """This API view allows authenticated users
    to create or delete a 'PostLike' object for specific 'Post'
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            201: PostLikeSerializer,
        }
    )
    def post(self, request: Request, pk: int) -> Response:
        data = {
            "post": pk,
            "user": request.user.id
        }

        serializer = PostLikeSerializer(data=data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, pk: int) -> Response:
        post = get_object_or_404(
            PostLike,
            user_id=request.user.id,
            post_id=pk
        )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Post Like Analytics"],
    parameters=[
        OpenApiParameter(
            name="date_from",
            description="Date from .ex(?date_from=1993-08-23)",
        ),
        OpenApiParameter(
            name="date_to",
            description="Date to .ex(?date_from=1993-08-25)",
        )
    ]
)
class PostLikeAnalyticsView(views.APIView):
    """This API view allows authenticated users check analytics about likes"""
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if not date_from or not date_to:
            return Response(
                {"error": "'date_from' and 'date_to' parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            analytics_service = PostLikeAnalyticsService(
                date_from=date_from,
                date_to=date_to
            )
            return Response(
                analytics_service.produce_analytics(),
                status=status.HTTP_200_OK
            )
        except ValueError:
            return Response(
                {"error": "Invalid date format .ex(YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )
