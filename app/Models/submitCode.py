from django.db import models

from app.Models.BaseModel import BaseModel
from app.Models.User import User
from app.Models.exercices import Exercise

class SubmitCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="submissions")
    user_code = models.TextField()
    is_correct = models.BooleanField(default=False)
    