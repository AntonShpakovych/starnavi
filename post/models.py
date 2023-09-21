from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    title = models.CharField(
        max_length=30,
        unique=True
    )
    description = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="posts"
    )

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="post_likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f"Post: {self.post} User: {self.user}"
