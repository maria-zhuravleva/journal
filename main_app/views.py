from django.shortcuts import render

from django.http import HttpResponse


def home(request):
  return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')

def about(request):
  return HttpResponse('<h1>About the CatCollector</h1>')
  # return render(request, '<h1>About the CatCollector</h1>')
