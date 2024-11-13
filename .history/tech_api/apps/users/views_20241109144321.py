from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import User, Profile
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,

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


class UserConnectDiscordView(generics.UpdateAPIView):
    """
    API view to connect the user's Discord account.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def update(self, request, *args, **kwargs):
        user = request.user
        discord_id = request.data.get("discord_id")

        # Assuming you have some method to validate the Discord ID
        user.discord_id = discord_id
        user.save()

        return Response({"message": "Discord account connected successfully."}, status=status.HTTP_200_OK)


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


class PasswordResetView(generics.GenericAPIView):
    """
    API view to handle password reset requests.
    """
    # Assume you have a serializer for handling password resets
    # serializer_class = PasswordResetSerializer

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Logic for password reset goes here
        return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


