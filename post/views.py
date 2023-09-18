from rest_framework import viewsets, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from post.models import Post, PostLike
from post.permissions import IsOwnerOrIsAuthenticatedReadOnly
from post.serializers import (
    PostSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    PostLikeSerializer
)
from post.services.post_like_analytics_service import PostLikeAnalyticsService


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        if self.action == "retrieve":
            return Post.objects.prefetch_related("user", "likes")
        return Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostRetrieveSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
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

    def delete(self, request, pk):
        post = get_object_or_404(
            PostLike,
            user_id=request.user.id,
            post_id=pk
        )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeAnalyticsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
