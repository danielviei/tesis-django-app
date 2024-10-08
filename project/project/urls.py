"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

from project.controllers.user_views import (
    forgot_password,
    login_view,
    password_reset,
    register,
    profile,
    reset_password,
)
from project.controllers.publication_views import (
    DeletePublicationView,
    PublicationDetailView,
    edit_publication,
    register_publication,
    list_publications,
)
from project.controllers.comment_views import (
    AddCommentView,
    DeleteCommentView,
    EditCommentView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", list_publications, name="home"),
    # user
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("password-reset/", password_reset, name="password_reset"),
    path(
        "forgot-password/",
        forgot_password,
        name="forgot_password",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        reset_password,
        name="password_reset_done",
    ),
    # publication
    path("create-publication/", register_publication, name="create_publication"),
    path(
        "publications/<int:pk>/",
        PublicationDetailView.as_view(),
        name="publication_detail",
    ),
    path(
        "publications/<int:pk>/edit/",
        edit_publication,
        name="edit_publication",
    ),
    path(
        "publications/<int:pk>/delete/",
        DeletePublicationView.as_view(),
        name="delete_publication",
    ),
    # comments
    path(
        "publications/<int:pk>/add-comment/",
        AddCommentView.as_view(),
        name="add_comment",
    ),
    path(
        "comments/<int:pk>/edit/",
        EditCommentView.as_view(),
        name="edit_comment",
    ),
    path(
        "comments/<int:pk>/delete/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
