from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    generated_text = models.TextField()
    language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)