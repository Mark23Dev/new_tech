from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import User, Profile
from django.shortcuts import redirect
from django.conf import settings
from integrations.discord_integration import DiscordIntegration
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSetNewPasswordSerializer

)
from .permissions import IsAuthenticatedAndVerified, IsOwnerOrReadOnly

class UserRegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserProfileSerializer(user).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    API view to log in a user and return JWT tokens.
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


class UserLogoutView(generics.GenericAPIView):
    """
    API view to log out a user and invalidate their token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()  # Invalidate the token
        except (AttributeError, ValueError):
            return Response({"message": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserProfileView(generics.RetrieveAPIView):
    """
    API view to retrieve a user's profile details.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    API view to update user profile details.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user


class DiscordCallbackView(APIView):
    """
    API view to handle the Discord OAuth2 callback.
    """
    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({"message": "Authorization code not provided."}, status=status.HTTP_400_BAD_REQUEST)

        discord_integration = DiscordIntegration()
        access_token = discord_integration.exchange_code_for_token(code)
        if access_token:
            # Connect Discord account to user
            success = discord_integration.connect_discord_account(request.user, access_token)
            if success:
                return Response({"message": "Discord account connected successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to connect Discord account."}, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(generics.DestroyAPIView):
    """
    API view to delete a user account and profile.
    """
    permission_classes = [IsAuthenticatedAndVerified, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(APIView):
    """
    View to handle password reset token request.
    """
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset token sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    View to handle password reset token validation.
    """
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            request.session['user_id'] = serializer.validated_data['user'].id  # Store user ID in session
            return Response({"message": "Token is valid. Proceed to reset password."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetSetNewPasswordView(APIView):
    """
    View to set a new password after token validation.
    """
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"message": "Session expired or token validation required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        serializer = PasswordResetSetNewPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=user)
            request.session.pop('user_id', None)  # Clear session after setting the password
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserConnectDiscordView(generics.UpdateAPIView):
    """
    API view to connect the user's Discord account.
    """
    serializer_class = DiscordConnectSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Discord account connected successfully."}, status=status.HTTP_200_OK)