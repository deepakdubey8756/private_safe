from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class CountAcess(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    
    def __str__(self):
        return self.author