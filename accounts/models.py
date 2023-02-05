from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=250)
    isVerfied = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username
