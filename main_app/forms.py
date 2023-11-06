# from django import forms
# from .models import Photo

# class PhotoEditForm(forms.ModelForm):
#   class Meta:
#     model = Photo
#     fields = ['new_photo']  
#     labels = {
#       'new_photo': 'Choose photo'
#     }

#     new_photo = forms.ImageField(label='Choose photo')




from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
  class Meta:
    model = Article
    fields = ['topic', 'title', 'content_main', 'content_section_1', 'content_section_2']
