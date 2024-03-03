from django.contrib import admin
from .models.comment import Comment
from .models.publication import Publication
from .models.user import CustomUser

admin.site.register(CustomUser)
admin.site.register(Publication)
admin.site.register(Comment)
