from rest_framework import permissions
from .models import CustomUser

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # For CustomUser model
        if isinstance(obj, CustomUser):
            return obj == request.user
        # For Profile model
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # For other models with 'owner'
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False