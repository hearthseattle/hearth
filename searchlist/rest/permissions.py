"""API permissions classes."""
from rest_framework import permissions


class ResourcePermission(permissions.BasePermission):
    """Custom permission to allow owners and admins to edit."""

    def has_object_permission(self, request, view, obj):
        """Set permissions at the object level for API requests."""
        # Reads (GET, HEAD and OPTIONS) are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Writes are owner or admin only
        return obj.owner == request.user or request.user.is_superuser
