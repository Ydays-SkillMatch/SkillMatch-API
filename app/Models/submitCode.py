from django.db import models

from app.Models import BaseModel, User, Exercise

class SubmitCode(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="submissions")
    user_code = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


