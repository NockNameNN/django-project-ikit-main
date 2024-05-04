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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    comments = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "slug",
            "author",
            "tags",
            "category",
            "comments",
        )
        model = Post

    def get_comments(self, instance):
        include_comments = self.context['request'].query_params.get('include') == 'comments'
        if include_comments:
            return CommentSerializer(instance.comments.all(), many=True).data
        else:
            return None
