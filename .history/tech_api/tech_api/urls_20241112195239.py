from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/users/', include('apps.users.urls')),
    path('api/feedback/', include('apps.feedback.urls')),
    path('api/admin_panel/', include('apps.admin_panel.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/forums/', include('apps.forums.urls')),
    path('api/hackathons/', include('apps.hackathons.urls')),
    path('api/institutions/', include('apps.institutions.urls')),
    path('api/paths/', include('apps.paths.urls')),
]
