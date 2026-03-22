from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.auth import SmartBinAuthentication
from api.permissions import IsSmartBin
from api.serializers import DisposeSerializer
from accounts.models import User
from ecocoins.services import credit_ecocoins, can_credit, calculate_points
from api.vision import VisionServiceError, identify_user_from_face, classify_waste_image


class IdentifyUserView(APIView):
    authentication_classes = [SmartBinAuthentication]
    permission_classes = [IsSmartBin]

    def post(self, request):
        if not request.body:
            return Response(
                {"error": "Raw image bytes required in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            match = identify_user_from_face(request.body)
        except VisionServiceError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        if not match:
            return Response(
                {
                    "status": "unknown",
                    "message": "User not recognized"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user, confidence = match
        return Response(
            {
                "status": "success",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "name": user.get_full_name(),
                },
                "confidence": confidence,
            },
            status=status.HTTP_200_OK,
        )

class DisposeWasteView(APIView):
    authentication_classes = [SmartBinAuthentication]
    permission_classes = [IsSmartBin]

    def post(self, request):
        serializer = DisposeSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data.get("user_id")
        waste_image = request.body
        weight = serializer.validated_data.get("weight", 1.0)

        if not waste_image:
            return Response(
                {"error": "Raw image bytes required in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            waste_type = classify_waste_image(waste_image)
        except VisionServiceError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
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
