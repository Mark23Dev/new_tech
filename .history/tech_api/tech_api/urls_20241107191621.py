from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/', include('apps.users.urls')),  # Users registration path
    path('login/', include('apps.users.urls')),     # Users login path
    path('logout/', include('apps.users.urls')),    # Users logout path
    path('reset-password/', include('apps.users.urls')),  # Reset password
    path('profile/', include('apps.users.urls')),    # Profile path
    path('profile/update/', include('apps.users.urls')),  # Profile update path
    path('discord-connect/', include('apps.users.urls')),  # Discord connection path
    path('delete/', include('apps.users.urls')),      # Delete user path
    # Other API paths
    path('api/feedback/', include('apps.feedback.urls')),
    path('api/admin_panel/', include('apps.admin_panel.urls')),
    path('api/events/', include('apps.events.urls')),
    path('api/forums/', include('apps.forums.urls')),
    path('api/hackathons/', include('apps.hackathons.urls')),
    path('api/institutions/', include('apps.institutions.urls')),
    path('api/paths/', include('apps.paths.urls')),
]
