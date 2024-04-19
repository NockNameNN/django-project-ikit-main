from rest_framework import serializers

from blogs.models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
        )
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "author",
            "tags",
            "category",
            "comments",
        )
        model = Post
