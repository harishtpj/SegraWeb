from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import SmartBin

class SmartBinAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("X-BIN-KEY")

        if not api_key:
            return None

        try:
            bin = SmartBin.objects.get(api_key=api_key, is_active=True)
        except SmartBin.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive bin")

        return (bin, None)
