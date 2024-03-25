from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles, name="article.index"), # R
    path('create/', views.article_create, name="article.create"), #C
    path('update/<int:article_id>/', views.article_update, name="article.update"),  # U
    path('remove/<int:article_id>/', views.article_delete, name="article.delete"), #D
]
