from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from project.models.user import CustomUser as User


class Publication(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="publications/")
    content = models.TextField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Publication")
        verbose_name_plural = _("Publications")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("publication_detail", args=[str(self.id)])
