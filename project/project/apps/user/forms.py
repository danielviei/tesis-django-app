from django import forms
from .models import CustomUser


class ImageUploadWidget(forms.ClearableFileInput):
    template_name = "image_upload_widget.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({"class": "hidden", "id": "imgUpload"})
        return attrs


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ["name", "lastname", "email", "password", "password_confirm", "img"]
        widgets = {
            "img": ImageUploadWidget(attrs={"class": "hidden"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden")

