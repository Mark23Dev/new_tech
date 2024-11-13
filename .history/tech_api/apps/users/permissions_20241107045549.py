from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


class IsAuthenticatedAndVerified(permissions.BasePermission):
    """
    Custom permission that only allows access to authenticated and verified users.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if user is verified
        return request.user.is_verified


class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to allow only admins or the user themselves to access certain views.
    """

    def has_object_permission(self, request, view, obj):
        # Allow if the user is an admin
        if request.user and request.user.is_staff:
            return True

        # Allow if the user is the owner of the profile
        return obj == request.user
