import datetime

from skillmatch.MasterViews.BaseView import BaseView


class NavData(BaseView):
    
    def __init__(self):
        super().__init__()
        
    def post(self, request):
        data_type = request.POST.get('type')
        data = request.POST.get('data')
        user = request.POST.get('user')
        timestamp = request.POST.get('timestamp')
        created_at = datetime.now()
        
        new_navdata = NavData(type=data_type, data=data, user=user, timestamp=timestamp, created_at=created_at)
        new_navdata.save()
        
        return new_navdata