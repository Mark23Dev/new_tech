from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Feedback
from .serializers import FeedbackSerializer

class SubmitFeedbackView(generics.CreateAPIView):
    """
    View to submit feedback.
    Only authenticated users can submit feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associate the feedback with the authenticated user upon submission.
        """
        serializer.save(user=self.request.user)  # Associate feedback with the user


class ListFeedbackView(generics.ListAPIView):
    """
    View to list all feedback.
    Admins can see all feedback, users can see only their own.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return feedback based on the user:
        - Admins can see all feedback.
        - Regular users can only see their own feedback.
        """
        if self.request.user.is_staff:  # Admin can see all feedback
            return Feedback.objects.all()
        else:  # Regular user can only see their own feedback
            return Feedback.objects.filter(user=self.request.user)


class RetrieveFeedbackView(generics.RetrieveAPIView):
    """
    View to retrieve specific feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve the feedback instance for the given user.
        """
        feedback = super().get_object()
        if feedback.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to view this feedback.")
        return feedback


class UpdateFeedbackView(generics.UpdateAPIView):
    """
    View to update specific feedback.
    Users can only update their own feedback, admins can update any feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve the feedback instance for update.
        Ensure that the user can only update their own feedback.
        """
        feedback = super().get_object()
        if feedback.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to update this feedback.")
        return feedback

    def perform_update(self, serializer):
        """
        Save the updated feedback instance.
        """
        serializer.save()


class DeleteFeedbackView(generics.DestroyAPIView):
    """
    View to delete specific feedback.
    Users can only delete their own feedback, admins can delete any feedback.
    """
    queryset = Feedback.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve the feedback instance for deletion.
        Ensure that the user can only delete their own feedback.
        """
        feedback = super().get_object()
        if feedback.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to delete this feedback.")
        return feedback
