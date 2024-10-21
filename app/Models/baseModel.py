import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    uuId = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()
