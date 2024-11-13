from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Feedback, Testimonial
from .serializers import FeedbackSerializer, TestimonialSerializer

class SubmitFeedbackView(generics.CreateAPIView):
    """
    View to submit feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Associate feedback with the user


class AddTestimonialView(generics.CreateAPIView):
    """
    View to add a testimonial.
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Associate testimonial with the user


class ListTestimonialsView(generics.ListAPIView):
    """
    View to list all testimonials.
    """
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]  # Make this view accessible to anyone
