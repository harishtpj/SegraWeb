from django.http import FileResponse, Http404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

User = get_user_model()

class UserFaceView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User not found")

        if not user.profile_photo:
            raise Http404("User has no profile photo")

        return FileResponse(
            user.profile_photo.open("rb"),
            content_type="image/jpeg"
        )
