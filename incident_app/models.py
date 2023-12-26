from django.db import models
import uuid

# Create your models here.


class Incident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30)
    severity = models.IntegerField(default=5)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="pending")
    assigned_to = models.CharField(max_length=30, blank=True)

class Handler(models.Model):
    name = models.CharField(max_length=30)
    availablity = models.BooleanField(default=True)
    