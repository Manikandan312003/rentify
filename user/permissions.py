from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsOwnerOrAdminOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            requestedUser: User = request.user.profile
            return obj == requestedUser or requestedUser.is_superuser
        except:
            return False


class IsOwnerOrAdminOrReadOnlyPropertyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        requestedUser: User = request.user
        return obj.profile == requestedUser.profile or requestedUser.is_superuser
