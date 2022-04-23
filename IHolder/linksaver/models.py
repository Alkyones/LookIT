from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class linksModel(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)