from django.db import models
from skillmatch.MasterModels.BaseModel import BaseModel
import uuid

class Language(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)

    def __repr__(self):
        return f"<Group {self.name}>"