from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Observation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='observations/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
