from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from blogs.models import Post, Category, Comment
from .filters import PostFilter

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('category').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
