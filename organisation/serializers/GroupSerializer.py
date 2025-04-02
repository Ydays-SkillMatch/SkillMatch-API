from rest_framework import serializers

from organisation.models.Group import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('uuid', 'name', 'users', 'created_at')