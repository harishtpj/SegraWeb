from rest_framework import serializers

class IdentifySerializer(serializers.Serializer):
    face_encoding = serializers.CharField()

class DisposeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    waste_type = serializers.CharField()
    weight = serializers.FloatField()
