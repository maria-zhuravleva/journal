from django.forms import ModelForm
from django import forms
from .models import Article


class SearchForm(forms.Form):
  search_query = forms.CharField(max_length=100, label=False, required=False,
    widget=forms.TextInput(attrs={'placeholder': 'Search by topic...'}),
  )


class ArticleForm(ModelForm):
  content_main = forms.CharField(widget=forms.Textarea(attrs={'wrap': 'hard'}))
  class Meta:
    model = Article
    fields = ['topic', 'title', 'content_main', 'content_section_1', 'content_section_2']
    
