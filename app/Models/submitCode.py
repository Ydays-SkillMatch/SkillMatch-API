from django.db import models

from app.Models.BaseModel import BaseModel
from app.Models.User import User
from app.Models.Exercice import Exercice

class SubmitCode(BaseModel):
    user_key = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    exercice_key = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name="submissions")
    user_code = models.TextField()
    is_correct = models.BooleanField(default=False)
    