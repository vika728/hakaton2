#
from rest_framework.permissions import BasePermission


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and str(obj.user).lower() == str(request.user.email).lower())


class IsAuth(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated)
#
# from django.contrib.auth.mixins import UserPassesTestMixin
#
#
# class SuperUserCheckMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)