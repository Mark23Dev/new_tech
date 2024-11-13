from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Feedback, Testimonial  #
from .serializers import FeedbackSerializer, TestimonialSerializer

# Feedback Views

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class SubmitFeedbackView(generics.CreateAPIView):
    """
    Allows authenticated users to submit feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associates feedback with the authenticated user.
        """
        serializer.save(user=self.request.user)


class ListFeedbackView(generics.ListAPIView):
    """
    Lists all feedback for admins or feedback by the authenticated user.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns feedback based on user role:
        - Admins see all feedback.
        - Regular users see only their own feedback.
        """
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user)


class RetrieveFeedbackView(generics.RetrieveAPIView):
    """
    Allows users to retrieve their own feedback or for admins to retrieve any feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        feedback = super().get_object()
        if feedback.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to view this feedback.")
        return feedback


class UpdateFeedbackView(generics.UpdateAPIView):
    """
    Allows users to update their own feedback, or for admins to update any feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        feedback = super().get_object()
        if feedback.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to update this feedback.")
        return feedback


class DeleteFeedbackView(generics.DestroyAPIView):
    """
    Allows users to delete their own feedback, or for admins to delete any feedback.
    """
    queryset = Feedback.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        feedback = super().get_object()
        if feedback.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You do not have permission to delete this feedback.")
        return feedback

# Testimonial ViewSet
class TestimonialViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing testimonials.
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
