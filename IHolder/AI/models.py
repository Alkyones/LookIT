from django.db import models
from django.contrib.auth.models import User


class AIChatModelNew(models.Model):
    keyword = models.CharField(max_length=255)
    links = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s chat result for '{self.keyword}'"
