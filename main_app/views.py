from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import ArticleForm
from .forms import SearchForm
from .models import Article, Photo
import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'marias-the-journal-bucket'


class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def article_index(request):
  search_form = SearchForm(request.GET)
  articles = Article.objects.all().order_by('-created_at')
  no_results = False

  if search_form.is_valid():
    search_query = search_form.cleaned_data.get('search_query')
    if search_query:
      articles = articles.filter(topic__icontains=search_query)
      if not articles.exists():
        no_results = True

  paginator = Paginator(articles, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'articles/index.html', {
    'page_obj': page_obj,
    'search_form': search_form,
    'no_results': no_results,
  })


@login_required
def article_detail(request, article_id):
  article = Article.objects.get(id=article_id)
  context = {
    'article': article,
    'photo_section1': Photo.objects.filter(article=article)[:2],
    'photo_section2': Photo.objects.filter(article=article)[2:],
  }
  return render(request, 'articles/detail.html', context)


class ArticleCreate(UserPassesTestMixin, CreateView):
  model = Article
  fields = ['topic', 'title', 'content_main', 'content_section_1', 'content_section_2']

  def form_valid(self, form):
    form.instance.author = self.request.user   
    return super().form_valid(form)
  
  def test_func(self):
    return self.request.user.is_superuser

class ArticleUpdate(UserPassesTestMixin, UpdateView):
  model = Article
  fields = ['topic', 'title', 'content_main', 'content_section_1', 'content_section_2']

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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_photo(request, article_id):
  photos = request.FILES.getlist('photo-file') 
  photo_section1 = []
  photo_section2 = []

  if photos:
    for index, photo_file in enumerate(photos):
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]

      try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        photo = Photo(url=url, article_id=article_id)
        photo.save()

        if index < 2:
          photo_section1.append(photo)
        else:
          photo_section2.append(photo)

      except Exception as err:
        print('An error occurred uploading file to S3: %s' % err)
        
  return redirect('article-detail', article_id=article_id)



@require_http_methods(["POST", "DELETE"])
def delete_photo(request, photo_id):
  photo = get_object_or_404(Photo, id=photo_id)
  article_id = photo.article.id
  photo.delete()
  return redirect('article-detail', article_id=article_id)



