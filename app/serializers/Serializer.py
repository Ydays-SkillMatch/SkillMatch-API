import yaml
import pdb
from rest_framework import serializers

from app.Models.BaseModel import BaseModel


class Serializer(serializers.ModelSerializer):
    def serialize(model : BaseModel|list[BaseModel], route_type : str):
        # var = type(model)
        # pdb.set_trace()
        dic = {}
        model_name = model.__class__.__name__
        if model_name == "QuerySet":
            return [Serializer.serialize(m,route_type) for m in model]
        
        if type(model) == list:
            return [Serializer.serialize(m,route_type) for m in model]
        
        with open(f"/app/app/serializers/ModelSerializer/{model_name}Serializer.yml") as stream:
            param = yaml.safe_load(stream)
        
        for key in param:
            value = param[key]
            
            if route_type not in value["rights"]: continue
            serialized_name = value["serialized_name"] if value["serialized_name"] else key
            serialized_value = model[key]
            
            if isinstance(serialized_value, BaseModel):
                serialized_value = Serializer.serialize(serialized_value)
            
            dic[serialized_name] = serialized_value
            
        return dic
    
class ExerciseSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    describe = serializers.CharField(required=True)
    timer = serializers.IntegerField(required=True, min_value=0)
    language = serializers.CharField(required=True, max_length=250)
    Test = serializers.CharField(required=True, max_length=250)

class GroupSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True, max_length=255)
    name = serializers.CharField(required=True, max_length=255)
    uuidUser = serializers.CharField(required=True, max_length=50)
    
class LanguageSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    extension = serializers.CharField(required=True, max_length=50)
    
class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255)
    email = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=250)
    
class UserMSerializer(serializers.Serializer):
    uuid = serializers.CharField(required=True, max_length=250)
    username = serializers.CharField(required=True, max_length=255)
    email = serializers.CharField(required=True, max_length=255)
    admin = serializers.BooleanField(required=True)