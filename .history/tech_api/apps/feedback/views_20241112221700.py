from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Feedback.
    Only authenticated users can submit feedback, and users can
    only view, update, or delete their own feedback. Admins can
    access all feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return feedback based on user permissions:
        - Admins can see all feedback.
        - Regular users can only see their own feedback.
        """
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associate the feedback with the authenticated user upon submission.
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Delete specific feedback.
        Users can only delete their own feedback; admins can delete any feedback.
        """
        feedback = self.get_object()
        if feedback.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete this feedback."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update specific feedback.
        Users can only update their own feedback; admins can update any feedback.
        """
        feedback = self.get_object()
        if feedback.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to update this feedback."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
