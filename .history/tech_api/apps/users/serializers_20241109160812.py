from rest_framework import serializers
from django.contrib.auth import authenticate
import uuid
from django.utils import timezone
from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Profile
from integrations.discord_integration import DiscordIntegration  # Adjust this import as necessary


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
    

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset token.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate token
        token = default_token_generator.make_token(user)
        
        # Send email with the token
        send_mail(
            subject="Password Reset Request",
            message=f"Use this token to confirm your identity: {token}",
            from_email="no-reply@example.com",
            recipient_list=[email],
        )

        return token

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming reset token without resetting password.
    """
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')
        
        try:
            user = User.objects.get(email=email)
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError("Invalid or expired token.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        attrs['user'] = user
        return attrs
    
class PasswordResetSetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        return attrs

    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save()


class DiscordConnectSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)  # This is the authorization code from Discord

    def validate_code(self, value):
        """Validate and exchange the code for a token, then retrieve user info from Discord."""
        discord_integration = DiscordIntegration()
        access_token = discord_integration.exchange_code_for_token(value)
        if not access_token:
            raise serializers.ValidationError("Invalid Discord authorization code.")

        # Get Discord user info with the token
        user_info = discord_integration.get_user_info(access_token)
        if not user_info:
            raise serializers.ValidationError("Could not retrieve Discord user information.")
        
        self.context['discord_user_info'] = user_info
        return value

    def save(self, **kwargs):
        """Connect the Discord account to the user instance."""
        user = self.context['request'].user
        discord_user_info = self.context.get('discord_user_info')

        user.discord_id = discord_user_info['id']
        user.discord_username = discord_user_info['username']
        user.save()
        return user