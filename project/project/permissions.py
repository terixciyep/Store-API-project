from rest_framework.permissions import BasePermission


class VerifyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_verify is True