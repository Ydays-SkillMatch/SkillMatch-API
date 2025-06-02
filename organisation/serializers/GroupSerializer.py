from rest_framework import serializers

from organisation.models.Group import Group
from users.models import User

class UserGroupSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

class GroupsSerializer(serializers.ModelSerializer):  
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', read_only=True)
      
    class Meta:
        model = Group
        fields = ('uuid', 'name', 'created_at', 'owner_id')

class GroupSerializer(serializers.ModelSerializer):
    users = UserGroupSerializer(many=True, read_only=True)
    owner = UserGroupSerializer(read_only=True)
    
    class Meta:
        model = Group
        fields = ('uuid', 'name', 'users', 'owner', 'created_at')