from django import forms
from django.contrib.auth.models import User
from .models import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["title", "image", "content"]
