from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    PasswordResetView,
    UserProfileView,
    UserProfileUpdateView,
    UserConnectDiscordView,
    UserDeleteView,
)

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('auth/reset-password/', PasswordResetView.as_view(), name='password-reset'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('discord-connect/', UserConnectDiscordView.as_view(), name='connect-discord'),
    path('delete/', UserDeleteView.as_view(), name='delete-user'),
]
