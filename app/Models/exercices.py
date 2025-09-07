from django.db import models

# from rest_framework.authtoken.admin import User
from app.Models.User import User
from app.Models.BaseModel import BaseModel


class Exercise(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User)
    code_test = models.TextField()

    def __str__(self):
        return self.title