import yaml
from django.db.models import Model
from rest_framework import serializers


class Serializer(serializers.ModelSerializer):
    def serialize(model):
        dic = {}
        model_name = model.__class__.__name__
        with open(f"{model_name}Serializer.yml") as stream:
             param = yaml.safe_load(stream)
        for key, value in param:
            dic[key] = model[value]
