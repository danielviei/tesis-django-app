from django import forms
from project.models.publication import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["title", "image", "content"]
