from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    title = models.CharField(max_length=150)
    body = models.TextField()
