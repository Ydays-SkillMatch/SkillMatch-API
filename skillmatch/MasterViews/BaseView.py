import datetime

from MasterModels.BaseModel import BaseModel
from rest_framework.views import APIView


class BaseView(APIView):
    
    def __init__(self):
        super().__init__()
        
    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid:
            return BaseModel.objects.all()
        return BaseModel.objects.get(uuid=uuid)
    
    def post(self, request):
        pass
    
    def put(self, request):
        pass
    
    def delete(self, request):
        uuid = request.GET.get('uuid')
        model = BaseModel.objects.get(uuid=uuid)
        model.deleted_at = datetime.now()