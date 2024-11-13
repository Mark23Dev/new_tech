from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import EventViewSet, EventAttendeeViewSet, UserActivityLogViewSet, FeedbackViewSet, TestimonialViewSet, ForumPostViewSet, ForumCommentViewSet, ChallengeViewSet, SubmissionViewSet, LeaderboardEntryViewSet, InstitutionViewSet, ScholarshipViewSet, ScholarshipApplicationViewSet, LearningPathViewSet, TechnologyViewSet, RecommendedCourseViewSet, UserRegisterViewSet

# Registering viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'attendees', EventAttendeeViewSet)
router.register(r'activity-logs', UserActivityLogViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'forum-posts', ForumPostViewSet)
router.register(r'forum-comments', ForumCommentViewSet)
router.register(r'challenge', ChallengeViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'leaderboard', LeaderboardEntryViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'scholarships', ScholarshipViewSet)
router.register(r'scholarship-applications', ScholarshipApplicationViewSet)
router.register(r'learning-paths', LearningPathViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'recommended-courses', RecommendedCourseViewSet)
router.register(r'register', UserRegisterViewSet)

# Swagger schema view setup
schema_view = get_schema_view(
   openapi.Info(
      title="FutureFemTech API",
      default_version='v1',
      description="API documentation for FutureFemTech project",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@futurefemtech.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('api/users/', include('apps.users.urls')),
    path('api/feedback/', include('apps.feedback.urls')),
    path('api/admin_panel/', include('apps.admin_panel.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/forums/', include('apps.forums.urls')),
    path('api/hackathons/', include('apps.hackathons.urls')),
    path('api/institutions/', include('apps.institutions.urls')),
    path('api/paths/', include('apps.paths.urls')),
]
