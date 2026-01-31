from rest_framework.permissions import BasePermission

class IsSmartBin(BasePermission):
    def has_permission(self, request, view):
        return request.user is not None
