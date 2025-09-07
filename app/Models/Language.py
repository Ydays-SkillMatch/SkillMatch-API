from django.db import models

from app.Models.BaseModel import BaseModel

class Language(BaseModel):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=4,default="py")

    def __repr__(self):
        return f"<Group {self.name}>"