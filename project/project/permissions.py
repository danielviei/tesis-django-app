from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access to all users.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow owners to edit the object.
        return obj.author_id == request.user
