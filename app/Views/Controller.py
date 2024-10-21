from django.db.migrations import serializer
from django.http import JsonResponse
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.Models import baseModel
from app.serializers.Serializer import Serializer


class Controller(GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,):
    def returnJSON(self,model):
        return JsonResponse(Serializer.serialize(model),safe=False)
