from django.contrib import admin
from .models import LearningPath, PathRecommendation, UserPathProgress, Technology, RecommendedCourse, ScholarshipApplication

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    """Admin view for managing learning paths."""
    list_display = ('title', 'description', 'created_at', 'is_self_paced', 'estimated_duration')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'is_self_paced')
    ordering = ('-created_at',)

@admin.register(PathRecommendation)
class PathRecommendationAdmin(admin.ModelAdmin):
    """Admin view for managing path recommendations."""
    list_display = ('learning_path', 'recommended_technology', 'recommended_course')
    search_fields = ('learning_path__title', 'recommended_technology__name', 'recommended_course__title')
    list_filter = ('learning_path',)

@admin.register(UserPathProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Admin view for managing user progress on paths."""
    list_display = ('user', 'path', 'progress', 'last_updated', 'started_at')
    search_fields = ('user__username', 'path__title')
    list_filter = ('last_updated',)
    ordering = ('-last_updated',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Admin view for managing technologies associated with learning paths."""
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(RecommendedCourse)
class RecommendedCourseAdmin(admin.ModelAdmin):
    """Admin view for managing recommended courses."""
    list_display = ('title', 'provider', 'path', 'duration', 'recommended_for_completion')
    search_fields = ('title', 'provider', 'path__title')
    list_filter = ('recommended_for_completion',)
    ordering = ('title',)

@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    """Admin view for managing scholarship applications."""
    list_display = ('user', 'path', 'status', 'application_date')
    search_fields = ('user__username', 'path__title')
    list_filter = ('status', 'application_date')
    ordering = ('-application_date',)
