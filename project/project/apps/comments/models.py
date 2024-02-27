from django.db import models


class Comment(models.Model):
    content = models.TextField()
    author_id = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    publication_id = models.ForeignKey(
        "publication.Publication", on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
