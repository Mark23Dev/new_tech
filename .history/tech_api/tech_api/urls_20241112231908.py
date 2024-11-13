from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication

# Import the viewsets or views from the respective apps
from apps.events.views import EventViewSet, EventAttendeeViewSet, UserActivityLogViewSet
from apps.feedback.views import FeedbackViewSet, TestimonialViewSet
from apps.forums.views import ForumPostViewSet, ForumCommentViewSet
from apps.hackathons.views import ChallengeViewSet, SubmissionViewSet, LeaderboardEntryViewSet
from apps.institutions.views import InstitutionListView, InstitutionDetailView, RecommendedScholarshipsView, ScholarshipApplicationView, ApplicationStatusView
from apps.paths.views import LearningPathViewSet, TechnologyViewSet, RecommendedCourseViewSet
from apps.users.views import UserRegisterViewSet

# Registering viewsets with the router
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
   authentication_classes=[JWTAuthentication],
   security=[{'Bearer': []}],
)

urlpatterns = [
    path('api/', include(router.urls)),  # Your API routes
    path('swagger/', schema_view.as_view(), name='swagger-ui'),  # Swagger documentation URL

    # Include app-specific URLs if additional URLs exist
    path('api/users/', include('apps.users.urls')),
    path('api/feedback/', include('apps.feedback.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/forums/', include('apps.forums.urls')),
    path('api/hackathons/', include('apps.hackathons.urls')),
    path('api/paths/', include('apps.paths.urls')),
]
