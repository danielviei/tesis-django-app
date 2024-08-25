from django import forms
from django.utils.translation import gettext_lazy as _
from project.models.publication import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["title", "content", "image"]
        labels = {
            "title": _("Título"),
            "content": _("Contenido"),
            "image": _("Imagen"),
        }
        widgets = {
            "image": forms.ClearableFileInput(),
        }
