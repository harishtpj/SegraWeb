from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
User = get_user_model()
from api.auth import SmartBinAuthentication
from api.permissions import IsSmartBin
from api.serializers import IdentifySerializer, DisposeSerializer
from accounts.models import User
from ecocoins.services import credit_ecocoins, can_credit, calculate_points


# NOTE: IdentifyUserView is deprecated - face recognition is handled by Flask app (getimgfromesp.py)
# The Flask app identifies the user and calls DisposeWasteView with user_id and waste_type
# class IdentifyUserView(APIView):
#     authentication_classes = [SmartBinAuthentication]
#     permission_classes = [IsSmartBin]
# 
#     def post(self, request):
#         serializer = IdentifySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = recognize_user(serializer.validated_data["face_encoding"])
#         if not user:
#             return Response(
#                 {"error": "User not recognized"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         return Response({
#             "user_id": user.id,
#             "name": user.get_full_name(),
#         })


class DisposeWasteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DisposeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data.get("user_id")
        waste_type = serializer.validated_data.get("waste_type")
        weight = serializer.validated_data.get("weight", 1.0)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Calculate points based on waste type and weight
        points_to_add = calculate_points(waste_type, weight)

        # Check daily limit
        if not can_credit(user, points_to_add):
            return Response({
                "error": "Daily limit reached",
                "message": "You've reached your daily ecocoin limit"
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Credit ecocoins using the service
        credit_ecocoins(user, points_to_add, waste_type, source="smart_bin")

        # Refresh to get updated balance
        user.refresh_from_db()

        return Response({
            "status": "success",
            "message": "Points awarded successfully",
            "points_added": points_to_add,
            "total_ecocoins": user.ecocoin_balance,
            "waste_type": waste_type,
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.get_full_name()
            }
        }, status=status.HTTP_200_OK)
