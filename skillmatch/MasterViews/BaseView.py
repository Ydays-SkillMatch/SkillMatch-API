from datetime import datetime
import yaml

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from skillmatch.MasterModels import BaseModel


class BaseView(APIView):

    def __init__(self):
        super().__init__()
        
    def get(self, request, uuid=None):
        objects = None
        hasmany = False

        if uuid:
            objects = self.model_class.objects.filter(deleted_at=None).get(uuid=uuid)
        else :
            objects = self.model_class.objects.filter(deleted_at=None).all()
            hasmany = True
        
        serializer = self.serializer_class(objects, many=hasmany)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        pass
    
    def put(self, request):
        pass
    
    def delete(self, request, uuid=None):
        model = self.model_class.objects.get(uuid=uuid)
        model.deleted_at = datetime.now()
        model.save()
        
        serializer = self.serializer_class(model)
        return JsonResponse(serializer.data, safe=False)

    def serialize(self, model: BaseModel | list[BaseModel], route_type: str):
        dic = {}
        model_name = model.__class__.__name__

        if model_name == "QuerySet":
            # Si c'est un QuerySet, on le sérialise de manière récursive
            return Response([self.serialize(m, route_type) for m in model])

        if isinstance(model, list):
            # Si c'est une liste d'objets, on sérialise chaque élément
            return Response([self.serialize(m, route_type) for m in model])

        # Charger le fichier YAML pour obtenir la configuration de sérialisation
        with open(f"/app/app/serializers/ModelSerializer/{model_name}Serializer.yml") as stream:
            param = yaml.safe_load(stream)

        for key in param:
            value = param[key]

            if route_type not in value["rights"]:
                continue

            serialized_name = value["serialized_name"] if value["serialized_name"] else key
            serialized_value = model[key]

            if isinstance(serialized_value, BaseModel):
                serialized_value = self.serialize(serialized_value, route_type)

            dic[serialized_name] = serialized_value

        # Retourner la réponse sous forme de Response
        return Response(dic)