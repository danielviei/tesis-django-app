from django.db import models

from project.models.user import CustomUser
from project.models.publication import Publication


class Comment(models.Model):
    content = models.TextField()
    author_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    publication_id = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="comments"
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
