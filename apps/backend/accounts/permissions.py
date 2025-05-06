from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner or admin
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the resource.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
