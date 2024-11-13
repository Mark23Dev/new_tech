# apps/feedback/views.py
from rest_framework import viewsets
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
