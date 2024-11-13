from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedAndVerified, IsAdminOrSelf

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsOwnerOrReadOnly]

    def get_queryset(self):
        # If the user is an admin, they can see all profiles
        if self.request.user.is_staff:
            return User.objects.all()
        # Otherwise, return only the logged-in user's profile
        return User.objects.filter(id=self.request.user.id)

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        return User.objects.all()
