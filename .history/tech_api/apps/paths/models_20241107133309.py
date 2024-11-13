from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Technology(models.Model):
    """
    Represents a technology or skill associated with a learning path.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class LearningPath(models.Model):
    """
    Represents a learning path, which can contain multiple modules or stages for users to complete.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    technologies = models.ManyToManyField(Technology, related_name="learning_paths")
    is_self_paced = models.BooleanField(default=False)
    estimated_duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserPathProgress(models.Model):
    """
    Tracks the progress of a user on a specific learning path.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="path_progress")
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="user_progress")
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Progress in percentage
    last_updated = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.path.title} - {self.progress}%"

class RecommendedCourse(models.Model):
    """
    Represents a self-paced course recommendation tied to a specific learning path.
    """
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="recommended_courses")
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=100)
    url = models.URLField()
    duration = models.DurationField(null=True, blank=True)
    recommended_for_completion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.provider})"

class ScholarshipApplication(models.Model):
    """
    Represents an application for a scholarship within a learning path.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scholarship_applications")
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="scholarship_applications")
    application_date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.path.title} - {self.status}"

class PathRecommendation(models.Model):
    """
    Represents a recommendation of a technology or course related to a learning path.
    This model is for recommending additional learning resources based on the path.
    """
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="path_recommendations")
    recommended_technology = models.ForeignKey(Technology, on_delete=models.CASCADE, related_name="path_recommendations", null=True, blank=True)
    recommended_course = models.ForeignKey(RecommendedCourse, on_delete=models.CASCADE, related_name="path_recommendations", null=True, blank=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Recommendation for {self.learning_path.title}: {self.recommended_technology.name if self.recommended_technology else self.recommended_course.title}"
