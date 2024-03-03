from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    USER = "user"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "User"),
        (ADMIN, "Admin"),
    ]

    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default=USER,
    )
    img = models.ImageField(upload_to="users/", null=True, blank=True)

    last_login = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def get_full_name(self):
        return f"{self.name} {self.lastname}"

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        """
        ¿El usuario tiene permisos para ver el módulo `app_label`?
        (Siempre `True` para usuarios activos y superusuarios.)
        """
        return self.is_staff
