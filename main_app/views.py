from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Article


class Home(LoginView):
  template_name = 'home.html'

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
  fields = ['title', 'content_main', 'content_section_1', 'content_section_2']

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)

class ArticleUpdate(UpdateView):
  model = Article
  fields = ['title', 'content_main', 'content_section_1', 'content_section_2']

class ArticleDelete(DeleteView):
  model = Article
  success_url = '/articles/'