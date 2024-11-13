from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserProfileUpdateView,
    UserConnectDiscordView,
    UserDeleteView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordResetSetNewPasswordView
)

urlpatterns = [
    # User Registration and Login
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # User Logout
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    
    # Connect Discord
    path('profile/connect/discord/', UserConnectDiscordView.as_view(), name='user-connect-discord'),
    
    # Delete User Account
    path('delete/', UserDeleteView.as_view(), name='user-delete'),
    
    # Password Reset
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/set/', PasswordResetSetNewPasswordView.as_view(), name='password-reset-set'),
]
