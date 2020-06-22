from rest_framework  import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check use to edit their own profile"""
        return obj.id == request.user.id
        