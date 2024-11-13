from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_verified']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            return {'user': user}
        raise serializers.ValidationError('Invalid email or password')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile details.
    """

    class Meta:
        model = User
        fields = ['email', 'username', 'is_verified', 'discord_id']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile details.
    """
    class Meta:
        model = User
        fields = ['username', 'discord_id']  # Add any additional fields as needed

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.discord_id = validated_data.get('discord_id', instance.discord_id)
        instance.save()
        return instance
