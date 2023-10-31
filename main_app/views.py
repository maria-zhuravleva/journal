from django.shortcuts import render

from django.http import HttpResponse

class Article: 
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

articles = [
  Article('Lolo', 'tabby', 'Kinda rude.', 3),
  Article('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
  Article('Fancy', 'bombay', 'Happy fluff ball.', 4),
  Article('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]

def home(request):
  return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')

def about(request):
  return render(request, 'about.html')

def article_index(request):
  return render(request, 'articles/index.html', { 'articles': articles })
