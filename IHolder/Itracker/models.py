from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class newsModel(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255 , null=True)
    image = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class userSavedNewsModel(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255 , null=True)
    image = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title