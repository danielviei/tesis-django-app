import smtplib
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from project.models.user_forms import (
    CustomResetPasswordForm,
    ForgotPasswordForm,
    LoginForm,
    PasswordResetForm,
    RegisterForm,
    UpdateForm,
)
from project.models.user import CustomUser
from project.settings import (
    BASE_URL,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
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


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                send_reset_password_email(
                    user.email,
                    "Restablecer contraseña",
                    f"{BASE_URL}/password-reset/{uidb64}/{token}",
                )
            messages.success(
                request,
                "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.",
            )
            return render(request, "reset_password_message.html")
    else:
        form = ForgotPasswordForm()
    return render(request, "forgot_password.html", {"form": form})


def generate_password_reset_token(user):
    return default_token_generator.make_token(user)


def send_reset_password_email(to_email, subject, message):
    # Define your Gmail username and password
    gmail_user = EMAIL_HOST_USER
    gmail_password = EMAIL_HOST_PASSWORD

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    # Try to log in to the Gmail SMTP server and send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.quit()
        print("Email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


def get_user_from_password_reset_token(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            return None
    except (CustomUser.DoesNotExist, ValueError):
        return None
    return user


def reset_password(request, uidb64, token):
    user = get_user_from_password_reset_token(uidb64, token)
    if user is None:
        messages.error(
            request,
            "El token de restablecimiento de contraseña no es válido o ha expirado.",
        )
        return redirect("forgot_password")
    if request.method == "POST":
        form = CustomResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            messages.success(request, "Tu contraseña se ha restablecido correctamente.")
            return redirect("login")
    else:
        form = CustomResetPasswordForm()
    return render(request, "reset_password.html", {"form": form})


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
                    form.add_error(
                        "new_password", "Las contraseñas nuevas no coinciden."
                    )
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
