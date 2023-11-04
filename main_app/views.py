from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Article, Photo
import uuid
import boto3

# Add these "constant" variables below the imports
S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'marias-the-journal-bucket'


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
    form.instance.author = self.request.user   
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

@login_required  
def like_article(request, article_id):
    article = Article.objects.get(id=article_id)
    liked = json.loads(request.body).get('liked') 
    if liked:
      article.likes += 1
    else:
      article.likes -= 1
    article.save()
    return JsonResponse({'likes': article.likes})


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


def add_photo(request, article_id):
  photos = request.FILES.getlist('photo-file') 
  
  if photos:
    for photo_file in photos:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

      try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        photo = Photo(url=url, article_id=article_id)
        article_photo = Photo.objects.filter(article_id=article_id)
        photo.save()
        # if article_photo.first():
        #   article_photo.first().delete()
        # photo.save()
      except Exception as err:
        print('An error occurred uploading file to S3: %s' % err)
  return redirect('article-detail', article_id=article_id)
  # photo_file = request.FILES.get('photo-file', None)
  # if photo_file:
  #   s3 = boto3.client('s3')
  #   key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

  #   try:
  #     s3.upload_fileobj(photo_file, BUCKET, key)
  #     url = f"{S3_BASE_URL}{BUCKET}/{key}"
  #     photo = Photo(url=url, article_id=article_id)
  #     article_photo = Photo.objects.filter(article_id=article_id)
  #     if article_photo.first():
  #       article_photo.first().delete()
  #     photo.save()
  #   except Exception as err:
  #     print('An error occurred uploading file to S3: %s' % err)

@require_http_methods(["DELETE"])
def delete_photo(request, photo_id):
  photo = get_object_or_404(Photo, id=photo_id)
  article_id = photo.article.id
  photo.delete()
  return redirect('article-detail', article_id=article_id)
