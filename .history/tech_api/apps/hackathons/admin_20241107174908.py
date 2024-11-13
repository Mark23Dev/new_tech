from django.contrib import admin
from .models import Challenge, Submission

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active', 'start_date', 'end_date')
    ordering = ('-start_date',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'submitted_at', 'score')
    search_fields = ('challenge__title', 'user__username')
    list_filter = ('challenge',)
    ordering = ('-submitted_at',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'submission_date', 'score')  # Use 'submission_date'
    search_fields = ('challenge__title', 'user__username')
    list_filter = ('challenge',)
    ordering = ('-submission_date',) 