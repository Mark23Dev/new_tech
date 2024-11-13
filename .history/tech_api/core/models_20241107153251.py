# core/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.TextField()  # Description of the activity
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created

    def __str__(self):
        return f"{self.user.username} - {self.activity} at {self.timestamp}"
