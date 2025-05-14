from django.db import models
from django.core.validators import MinValueValidator
from skillmatch.MasterModels.BaseModel import BaseModel
from language.models import Language

class Exercice(BaseModel):
    name = models.CharField(max_length=255)
    describe = models.TextField()
    timer = models.IntegerField(validators=[MinValueValidator(1)])
    ex_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="exercices")
    test = models.TextField()
    correct = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.ex_language.name})"
