from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Import your app's views and viewsets
from events.views import EventViewSet, EventAttendeeViewSet  # Example imports from your app
from feedback.views import FeedbackViewSet, TestimonialViewSet
# Add other views as per your project structure

# Register viewsets here
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'attendees', EventAttendeeViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'testimonials', TestimonialViewSet)
# Add more routes for other apps (challenges, forum, etc.)

# Set up Swagger UI
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
