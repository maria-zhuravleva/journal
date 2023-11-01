from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Article


class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def article_index(request):
  articles = Article.objects.all()
  return render(request, 'articles/index.html', { 'articles': articles })

@login_required
def article_detail(request, article_id):
  article = Article.objects.get(id=article_id)
  return render(request, 'articles/detail.html', { 'article': article })

class ArticleCreate(UserPassesTestMixin, CreateView):
  model = Article
  fields = ['title', 'content_main', 'content_section_1', 'content_section_2']

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)
  
  def test_func(self):
    return self.request.user.is_superuser

class ArticleUpdate(UserPassesTestMixin, UpdateView):
  model = Article
  fields = ['title', 'content_main', 'content_section_1', 'content_section_2']

  def test_func(self):
    return self.request.user.is_superuser

class ArticleDelete(UserPassesTestMixin, DeleteView):
  model = Article
  success_url = '/articles/'

  def test_func(self):
    return self.request.user.is_superuser

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('article-index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
