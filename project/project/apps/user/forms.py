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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
