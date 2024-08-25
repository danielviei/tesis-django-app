from django.db import models
from django.utils.translation import gettext_lazy as _

from project.models.user import CustomUser
from project.models.publication import Publication


class Comment(models.Model):
    content = models.TextField(verbose_name=_("Content"))
    author_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Author"))
    publication_id = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="comments",
        verbose_name=_("Publication"),
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content
