from rest_framework.permissions import BasePermission


class IsAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.admin:
            return True
        else:
            return False