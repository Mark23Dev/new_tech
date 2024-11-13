import os
import requests
from requests.exceptions import HTTPError, ConnectionError
import logging
from decouple import config

# Load sensitive data from environment variables
API_BASE_URL = config('GEMINI_API_BASE_URL')
CLIENT_ID = config('GEMINI_CLIENT_ID')
CLIENT_SECRET = config('GEMINI_CLIENT_SECRET')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAPI:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.access_token = None
        self.authenticate()  # Authenticate at the start

    def authenticate(self):
        """Authenticate with the Gemini API and retrieve an access token."""
        auth_url = f"{self.base_url}/auth/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        try:
            response = requests.post(auth_url, data=data)
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
            logger.info("Successfully authenticated with Gemini API.")
        except (HTTPError, ConnectionError) as e:
            logger.error("Authentication failed: %s", e)
            raise

    def get_headers(self):
        """Return headers required for authenticated requests."""
        if not self.access_token:
            self.authenticate()  # Re-authenticate if no token is available
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_user_data(self, user_id):
        """Fetch user-specific data from Gemini based on user_id."""
        user_data_url = f"{self.base_url}/users/{user_id}/data"
        try:
            response = requests.get(user_data_url, headers=self.get_headers())
            response.raise_for_status()
            user_data = response.json()
            logger.info("Retrieved data for user %s", user_id)
            return user_data
        except (HTTPError, ConnectionError) as e:
            logger.error("Failed to fetch user data: %s", e)
            raise

    def get_recommendations(self, user_data):
        """Generate content recommendations based on user data."""
        recommendations_url = f"{self.base_url}/recommendations"
        try:
            response = requests.post(
                recommendations_url,
                headers=self.get_headers(),
                json={"user_data": user_data}
            )
            response.raise_for_status()
            recommendations = response.json().get("recommendations", [])
            logger.info("Received recommendations for user.")
            return recommendations
        except (HTTPError, ConnectionError) as e:
            logger.error("Failed to fetch recommendations: %s", e)
            raise

    def update_progress(self, user_id, progress_data):
        """Update user progress in Gemini to adjust learning path."""
        progress_url = f"{self.base_url}/users/{user_id}/progress"
        try:
            response = requests.put(
                progress_url,
                headers=self.get_headers(),
                json={"progress_data": progress_data}
            )
            response.raise_for_status()
            logger.info("Updated progress for user %s", user_id)
            return response.json()
        except (HTTPError, ConnectionError) as e:
            logger.error("Failed to update progress: %s", e)
            raise

# Usage Example:
if __name__ == "__main__":
    gemini_api = GeminiAPI()
    
    # Fetch user data and recommendations
    user_id = "example_user_id"
    user_data = gemini_api.get_user_data(user_id=user_id)
    recommendations = gemini_api.get_recommendations(user_data=user_data)
    print("User Recommendations:", recommendations)

    # Update user progress
    progress_data = {"completed_modules": 3, "current_module": 4}
    update_response = gemini_api.update_progress(user_id=user_id, progress_data=progress_data)
    print("Progress Update Response:", update_response)
