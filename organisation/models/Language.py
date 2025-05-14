from django.db import models
from skillmatch.MasterModels.BaseModel import BaseModel

class Language(BaseModel):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=4)

    def __repr__(self):
        return f"<Group {self.name}>"