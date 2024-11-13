from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegisterViewSet,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserProfileUpdateView,
    DiscordCallbackView,
    UserDeleteView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordResetSetNewPasswordView,
    UserConnectDiscordView,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='user-register')

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('delete/', UserDeleteView.as_view(), name='user-delete'),
    path('discord/callback/', DiscordCallbackView.as_view(), name='discord-callback'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/set-new-password/', PasswordResetSetNewPasswordView.as_view(), name='password-reset-set-new-password'),
    path('connect-discord/', UserConnectDiscordView.as_view(), name='user-connect-discord'),
    
    # Include the router URLs for the UserRegisterViewSet
    path('', include(router.urls)),
]
