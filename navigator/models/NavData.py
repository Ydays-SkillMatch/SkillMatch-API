from django.db import models

from skillmatch.MasterModels.BaseModel import BaseModel
from users import models as user


class NavData(models.Model):
    type = models.CharField(max_length=255)
    data = models.TextField()
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    
    def __repr__(self):
        return f"<NavData {self.type}: {self.data}>"