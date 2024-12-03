from django.db import models

from app.Models.BaseModel import BaseModel


class Exercice(BaseModel):
    name = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)
    timer = models.IntegerField()
    ex_language = models.CharField(max_length=255)
    test = models.TextField()
    correct = models.TextField()

    def __repr__(self):
        return f"<User {self.name}>"