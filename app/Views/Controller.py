from django.db.migrations import serializer
from django.http import JsonResponse
from rest_framework.views import APIView

from app.Models.BaseModel import BaseModel
from app.serializers.Serializer import Serializer


class Controller(APIView):
    
    def __init__(self):
        super().__init__()
    
    def serialize(self, models : BaseModel|list[BaseModel], route_type : str):
        return JsonResponse(Serializer.serialize(models, route_type),safe=False)
