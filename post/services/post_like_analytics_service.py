from django.db.models import Count
from django.utils import timezone

from post.models import PostLike


class PostLikeAnalyticsService:
    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def make_aware_date(self):
        self.date_from = timezone.make_aware(
            timezone.datetime.strptime(self.date_from, "%Y-%m-%d")
        )
        self.date_to = timezone.make_aware(
            timezone.datetime.strptime(self.date_to, "%Y-%m-%d")
        )

    def produce_analytics(self):
        self.make_aware_date()

        analytics = PostLike.objects.filter(
            created_at__range=[self.date_from, self.date_to]
        ).values(
            "created_at__date"
        ).annotate(
            likes=Count("id")
        )

        return self.__serializer_analytics(analytics=analytics)

    @staticmethod
    def __serializer_analytics(analytics):
        return [
            {
                "date": analytic_item["created_at__date"],
                "likes": analytic_item["likes"]
            }
            for analytic_item in analytics
        ]
