from django.db import models

from app.Models.BaseModel import BaseModel
from app.Models.Group import Group

class User(BaseModel):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.TextField()
    admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)

    def __repr__(self):
        return f"<User {self.username}>"