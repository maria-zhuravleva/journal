from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Article


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def article_index(request):
  articles = Article.objects.all()
  return render(request, 'articles/index.html', { 'articles': articles })

def article_detail(request, article_id):
  article = Article.objects.get(id=article_id)
  return render(request, 'articles/detail.html', { 'article': article })

class ArticleCreate(CreateView):
  model = Article
  fields = '__all__'
  fields = ['title', 'content_main', 'content_section_1', 'content_section_2']
  success_url = '/articles/'