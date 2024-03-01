from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from project.models.publication import Publication
from project.permissions import IsOwnerOrReadOnly

from project.models.publication_forms import PublicationForm


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


def list_publications(request):
    publications_list = Publication.objects.all()
    paginator = Paginator(publications_list, 10)

    page_number = request.GET.get("page")
    publications = paginator.get_page(page_number)

    return render(request, "list_publications.html", {"publications": publications})


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "publication_detail.html"
    permission_classes = [IsOwnerOrReadOnly]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
