from django.urls import include, path

from rest_framework import routers

from post.views import (
    PostViewSet,
    PostLikeView,
    PostLikeAnalyticsView
)


router = routers.DefaultRouter()
router.register("", PostViewSet, basename="post")

urlpatterns = [
    path(
        "analytics/",
        PostLikeAnalyticsView.as_view(),
        name="post-like-analytics"
    ),
    path(
        "",
        include(router.urls),
        name="post"
    ),
    path(
        "<int:pk>/like/",
        PostLikeView.as_view(),
        name="post-like"
    ),

]

app_name = "post"
