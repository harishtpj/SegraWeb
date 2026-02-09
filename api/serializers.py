from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class IdentifySerializer(serializers.Serializer):
    face_encoding = serializers.CharField()

class DisposeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    waste_type = serializers.CharField()
    weight = serializers.FloatField()
    
class UserListSerializer(serializers.ModelSerializer):
    has_photo = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["username", "has_photo"]
    def get_has_photo(self, obj):
        return bool(obj.profile_photo)
