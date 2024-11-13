from rest_framework import serializers
from .models import Institution, Scholarship, ScholarshipApplication


class InstitutionSerializer(serializers.ModelSerializer):
    """Serializer for the Institution model."""
    class Meta:
        model = Institution
        fields = '__all__'  # or specify fields explicitly


class ScholarshipSerializer(serializers.ModelSerializer):
    """Serializer for the Scholarship model."""
    class Meta:
        model = Scholarship
        fields = '__all__'  # or specify fields explicitly


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    """Serializer for the ScholarshipApplication model."""
    class Meta:
        model = ScholarshipApplication
        fields = ['id', 'user', 'scholarship', 'application_date', 'status']
        read_only_fields = ['id', 'user', 'application_date', 'status']  # User and date should be set automatically

    def create(self, validated_data):
        """Override the create method to set the user automatically."""
        validated_data['user'] = self.context['request'].user  # Set the user to the current user
        return super().create(validated_data)
