from django import forms
from .models import Photo

class PhotoEditForm(forms.ModelForm):
  new_photo = forms.ImageField(required=False)

  class Meta:
    model = Photo
    fields = ['url', 'new_photo']  
