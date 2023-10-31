from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('articles/', views.article_index, name='article-index'),
  path('articles/<int:article_id>/', views.article_detail, name='article-detail'),
  path('articles/create/', views.ArticleCreate.as_view(), name='article-create'),
]