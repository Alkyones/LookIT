from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SavedEvents(models.Model):
    title = models.CharField(max_length=500)
    timeEvent= models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    publisher = models.CharField(max_length=500)

    posting_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class searchSavedEvents(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    eventDate = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    online = models.BooleanField(default=False)

    posting_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class userSavedEventsModel(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    eventDate = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    online = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title + '-' + self.user