# admin_panel/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)  # Additional details about the activity
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Optionally log the IP address

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"

    class Meta:
        verbose_name = 'User Activity Log'
        verbose_name_plural = 'User Activity Logs'
        ordering = ['-timestamp']
