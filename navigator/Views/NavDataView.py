from datetime import datetime

from django.http import JsonResponse

from navigator.models.NavData import NavData
from navigator.serializers.NavDataSerializer import NavDataSerializer
from skillmatch.MasterViews.BaseView import BaseView
from users.models import User


class NavDataView(BaseView):
    serializer_class = NavDataSerializer
    model_class = NavData
    
    def __init__(self):
        super().__init__()
        
    def post(self, request):
        data_type = request.data["type"]
        data = request.data["data"]
        user = User.objects.get(id=request.data["user"]["id"])
        timestamp = datetime.fromtimestamp(int(request.data["timestamp"]))
        created_at = datetime.now()
        
        new_navdata = NavData(data_type=data_type, data=data, user=user, timestamp=timestamp, created_at=created_at)
        new_navdata.save()
        
        serializer = NavDataSerializer(new_navdata)
        return JsonResponse(serializer.data, safe=False)