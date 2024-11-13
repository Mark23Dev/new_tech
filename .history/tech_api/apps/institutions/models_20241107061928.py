from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Institution(models.Model):
    """Model to represent a partner institution."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    """Model to represent a scholarship offered by an institution."""
    institution = models.ForeignKey(Institution, related_name='scholarships', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    application_deadline = models.DateTimeField()
    financial_needs = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ScholarshipApplication(models.Model):
    """Model to represent a scholarship application submitted by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, related_name='applications', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.scholarship.title} - {self.status}"
