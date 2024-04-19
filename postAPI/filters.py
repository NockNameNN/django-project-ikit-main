import django_filters
from blogs.models import Post


class PostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['name', 'category']