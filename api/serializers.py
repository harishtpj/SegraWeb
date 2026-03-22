from rest_framework import serializers

class DisposeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    weight = serializers.FloatField(required=False, default=1.0)
