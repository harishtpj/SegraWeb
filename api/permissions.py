from rest_framework.permissions import BasePermission
from .models import SmartBin

class IsSmartBin(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, SmartBin) and request.user.is_active
