from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.auth import SmartBinAuthentication
from api.permissions import IsSmartBin
from api.serializers import IdentifySerializer, DisposeSerializer
from accounts.models import User
from ecocoins.services import credit_ecocoins, can_credit, calculate_points


class IdentifyUserView(APIView):
    authentication_classes = [SmartBinAuthentication]
    permission_classes = [IsSmartBin]

    def post(self, request):
        serializer = IdentifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # TODO: Integrate with actual face recognition logic
        user = recognize_user(serializer.validated_data["face_encoding"])

        if not user:
            return Response(
                {"error": "User not recognized"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "user_id": user.id,
            "name": user.get_full_name(),
        })


class DisposeWasteView(APIView):
    authentication_classes = [SmartBinAuthentication]
    permission_classes = [IsSmartBin]

    def post(self, request):
        serializer = DisposeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=serializer.validated_data["user_id"])

        points = calculate_points(
            serializer.validated_data,
            user
        )

        if not can_credit(user, points):
            return Response(
                {"error": "Daily limit exceeded"},
                status=status.HTTP_403_FORBIDDEN
            )

        credit_ecocoins(user, points, serializer.validated_data["waste_type"])

        return Response({
            "points": points,
            "balance": user.ecocoin_balance
        })
