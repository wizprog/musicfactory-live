
from django.forms import ModelForm
from .models import Track
from django import forms

class CreateTrackForm(forms.Form):
    artist = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    file = forms.FileField()


class UploadFileForm(ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'file']