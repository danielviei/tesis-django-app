from django.db import models
from django.urls import reverse

from project.apps.user.models import CustomUser as User


class Publication(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="images/publications/")
    content = models.TextField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("publication:publication_detail", args=[str(self.id)])
