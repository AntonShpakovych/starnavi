from rest_framework import serializers

from post.models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "description"]


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "title", "description"]


class PostRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "user", "title", "description", "likes"]

    @staticmethod
    def get_user(obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    @staticmethod
    def get_likes(obj):
        return len(obj.likes.all())


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["post", "user"]
