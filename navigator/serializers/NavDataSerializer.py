from rest_framework import serializers

from navigator.models.NavData import NavData


class NavDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavData
        fields = ('uuid', 'data_type', 'data', 'user', 'timestamp')
