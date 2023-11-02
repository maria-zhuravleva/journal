from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('articles/', views.article_index, name='article-index'),
  path('articles/<int:article_id>/', views.article_detail, name='article-detail'),
  path('articles/create/', views.ArticleCreate.as_view(), name='article-create'),
  path('articles/<int:pk>/update/', views.ArticleUpdate.as_view(), name='article-update'),
  path('articles/<int:pk>/delete/', views.ArticleDelete.as_view(), name='article-delete'),
  path('accounts/signup/', views.signup, name='signup'),
  path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
]