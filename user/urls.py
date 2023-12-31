from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

from user.views import (
    UserCreateView,
    ManageUserView,
    UserActivityView,
)


urlpatterns = [
    path("", UserCreateView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("activities/", UserActivityView.as_view(), name="activities"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify")
]

app_name = "user"
