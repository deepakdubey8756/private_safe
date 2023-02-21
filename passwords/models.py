from django.db import models
from django.contrib.auth.models import User 


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
