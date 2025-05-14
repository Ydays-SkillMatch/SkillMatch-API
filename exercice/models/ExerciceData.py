from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from skillmatch.MasterModels.BaseModel import BaseModel
from language.models import Language
from users.serializers import UserSerializer
from users.models import User


class Exercice(BaseModel):
    uuid_user = models.ManyToManyField(related_name='exercices', to=settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    describe = models.TextField()
    timer = models.IntegerField(validators=[MinValueValidator(1)])
    ex_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="exercices")
    test = models.TextField()
    correct = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.ex_language.name})"
