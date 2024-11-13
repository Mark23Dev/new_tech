from django.contrib import admin
from .models import LearningPath, PathRecommendation, UserPathProgress, Technology

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    """Admin view for managing learning paths."""
    list_display = ('title', 'description', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('created_at',)

@admin.register(PathRecommendation)
class PathRecommendationAdmin(admin.ModelAdmin):
    """Admin view for managing path recommendations."""
    list_display = ('user', 'recommended_paths', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)

@admin.register(UserPathProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Admin view for managing user progress on paths."""
    list_display = ('user', 'learning_path', 'progress', 'updated_at')
    search_fields = ('user__username', 'learning_path__title')
    list_filter = ('updated_at',)
    ordering = ('-updated_at',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Admin view for managing technologies associated with learning paths."""
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('created_at',)
