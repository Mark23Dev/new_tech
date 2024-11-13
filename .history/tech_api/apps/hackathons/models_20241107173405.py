from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.title

class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='submissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    score = models.IntegerField(default=0)  # Score awarded for the submission

    def __str__(self):
        return f'Submission by {self.user.username} for {self.challenge.title}'

class LeaderboardEntry(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='leaderboard_entries', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leaderboard_entries', on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('challenge', 'user')  # Ensure a user can only have one entry per challenge

    def __str__(self):
        return f'Leaderboard Entry for {self.user.username} in {self.challenge.title}'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'submission_date', 'score')  # Use 'submission_date'
    search_fields = ('challenge__title', 'user__username')
    list_filter = ('challenge',)
    ordering = ('-submission_date',) 