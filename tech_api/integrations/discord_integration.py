import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class DiscordIntegration:
    """Class to handle Discord integration."""

    BASE_URL = 'https://discord.com/api'
    AUTH_URL = f'{BASE_URL}/oauth2/authorize'
    TOKEN_URL = f'{BASE_URL}/oauth2/token'
    USER_URL = f'{BASE_URL}/users/@me'

    def __init__(self):
        self.client_id = settings.DISCORD_CLIENT_ID
        self.client_secret = settings.DISCORD_CLIENT_SECRET
        self.redirect_uri = settings.DISCORD_REDIRECT_URI
        self.scopes = 'identify email'  # Adjust the scopes based on your needs

    def get_auth_url(self):
        """Generate the Discord OAuth2 authorization URL."""
        return f"{self.AUTH_URL}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scopes}"

    def exchange_code_for_token(self, code):
        """Exchange the authorization code for an access token."""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'scope': self.scopes,
        }
        response = requests.post(self.TOKEN_URL, data=data)
        response_data = response.json()
        if response.status_code == 200:
            return response_data.get('access_token')
        return None

    def get_user_info(self, access_token):
        """Fetch user information from Discord using the access token."""
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get(self.USER_URL, headers=headers)
        return response.json() if response.status_code == 200 else None

    def connect_discord_account(self, user, access_token):
        """Connect a Discord account to a user."""
        user_info = self.get_user_info(access_token)
        if user_info:
            # Here you might want to save the Discord information
            discord_id = user_info['id']
            username = user_info['username']
            # Update the user's profile or create a new model to store Discord info
            # Example:
            user.discord_id = discord_id
            user.discord_username = username
            user.save()

            return True
        return False

# Usage
# You might want to instantiate this class and call its methods in your views.
