from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PublicationForm


@login_required
def register_publication(request):
    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.author_id = request.user
            publication.save()
            return redirect("home")
    else:
        form = PublicationForm()

    return render(request, "create_publication.html", {"form": form})
