# core/permissions.py

from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access certain views.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to edit.
    Unauthenticated users can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows users to edit their own data,
    but others can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

# Example usage
# from core.permissions import IsAdminUser

# class MyView(APIView):
#     permission_classes = [IsAdminUser]
#     ...
