from rest_framework import serializers

from organisation.models.Group import Group
from users.models import User

class UserGroupSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class GroupsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('uuid', 'name', 'created_at')

class GroupSerializer(serializers.ModelSerializer):
    users = UserGroupSerializer(many=True)
    
    class Meta:
        model = Group
        fields = ('uuid', 'name', 'users', 'created_at')
        
        
        