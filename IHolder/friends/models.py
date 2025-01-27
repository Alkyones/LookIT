from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Friends(models.Model):
    friend = models.CharField(max_length=255)
    
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.friend}-{self.user}'