from datetime import datetime

from django.http import JsonResponse
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