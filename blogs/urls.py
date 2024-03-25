from django.urls import path, include
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView, delete_comment,
)

urlpatterns = [
    path("new/", BlogCreateView.as_view(), name="post_new"),
    path("<str:category>/<str:slug>", BlogDetailView.as_view(), name="post_detail"),
    path("<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("", BlogListView.as_view(), name="post_list"),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
]
