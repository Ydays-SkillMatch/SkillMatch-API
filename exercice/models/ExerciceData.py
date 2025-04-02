from django.db import models

from skillmatch.MasterModels.BaseModel import BaseModel
from language.models import Language

class Exercice(BaseModel):
    name = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)
    timer = models.IntegerField()
    ex_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    test = models.TextField()
    correct = models.TextField()

    def __repr__(self):
        return f"<User {self.name}>"