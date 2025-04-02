from django.db import models

from skillmatch.MasterModels.BaseModel import BaseModel
from users.models import User

class Group(BaseModel):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    def __repr__(self):
        return f"<Group {self.name}>"