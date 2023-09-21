from django.contrib import admin

from post.models import Post, PostLike


admin.site.register(Post)
admin.site.register(PostLike)
