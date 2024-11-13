from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterViewSet,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserProfileUpdateView,
    UserConnectDiscordView,
    UserDeleteView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordResetSetNewPasswordView,
    DiscordCallbackView
)


urlpatterns = [
    # Register the rest of the views as paths
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('profile/connect/discord/', UserConnectDiscordView.as_view(), name='user-connect-discord'),
    path('discord/callback/', DiscordCallbackView.as_view(), name='discord_callback'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/set/', PasswordResetSetNewPasswordView.as_view(), name='password-reset-set'),
    path('register/', UserRegisterViewSet.as_view(), name='user-register'),
]

