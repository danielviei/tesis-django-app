from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


from project.models.publication import Publication
from project.models.publication_forms import PublicationForm
from project.permissions import IsOwnerOrReadOnly


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


@login_required
def edit_publication(request, pk):
    publication = get_object_or_404(Publication, id=pk)

    # Check that the logged in user is the author of the publication
    if request.user != publication.author_id:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PublicationForm(instance=publication)

    return render(request, "edit_publication.html", {"form": form})


class DeletePublicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        publication = Publication.objects.get(pk=pk)
        if request.user != publication.author_id:
            return Response(
                {"error": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        publication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicationDetailView(DetailView):
    model = Publication
    template_name = "publication_detail.html"
    permission_classes = [IsOwnerOrReadOnly]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
