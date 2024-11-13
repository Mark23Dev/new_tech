from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

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
