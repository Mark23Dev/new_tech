from rest_framework import serializers
from .models import Feedback, Testimonial

class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for the Feedback model.
    """
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']  # User and created_at are auto-filled

class TestimonialSerializer(serializers.ModelSerializer):
    """
    Serializer for the Testimonial model.
    """
    class Meta:
        model = Testimonial
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']  # User and created_at are auto-filled
