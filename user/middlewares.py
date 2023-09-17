from django.utils import timezone
from rest_framework.reverse import reverse


class UserActivityMiddleware:
    AVOID_PATH = [reverse("user:activities")]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
                request.user.is_authenticated
                and request.path not in UserActivityMiddleware.AVOID_PATH
        ):
            user = request.user
            user.last_request = timezone.now()
            user.save()

        return response
