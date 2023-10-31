from django.shortcuts import render
from .models import Article


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def article_index(request):
  articles = Article.objects.all()
  return render(request, 'articles/index.html', { 'articles': articles })
