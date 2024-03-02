from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from project.models.user_forms import (
    LoginForm,
    PasswordResetForm,
    RegisterForm,
    UpdateForm,
)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if form.instance.id != request.user.id:
                raise PermissionDenied
            form.save()
            return redirect("home")
    else:
        form = UpdateForm(instance=user)

    return render(request, "edit_user.html", {"form": form})


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            confirm_new_password = form.cleaned_data["confirm_new_password"]

            user = authenticate(email=request.user.email, password=old_password)

            if user is not None:
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    return redirect("profile")
                else:
                    print("Passwords don't match")
                    form.add_error("new_password", "Las contraseñas nuevas no coinciden.")
            else:
                print("Wrong password")
                form.add_error("old_password", "Contraseña actual incorrecta.")

    else:
        form = PasswordResetForm()
    return render(request, "password_reset.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            breakpoint()
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "home")
                return redirect(next_url)
            else:
                form.add_error("email", "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
