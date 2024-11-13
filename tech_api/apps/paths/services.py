from .models import LearningPath, Technology, UserPathProgress
from django.contrib.auth.models import User
from .integrations import gemma_api, gemini_api  # Assuming you have API integrations set up

def get_personalized_recommendations(user):
    """Fetch personalized learning path recommendations for the user."""
    # Example logic to fetch recommendations from an external service
    recommendations = gemma_api.get_recommendations(user.profile)
    return recommendations

def generate_learning_path(user, preferences):
    """Generate a learning path using an external AI API like Gemma or Gemini."""
    path_data = gemini_api.generate_path(user, preferences)
    path, created = LearningPath.objects.update_or_create(
        user=user,
        defaults={'data': path_data}
    )
    return path

def get_learning_path_details(path_id):
    """Retrieve details for a specific learning path."""
    return LearningPath.objects.filter(id=path_id).first()

def update_user_progress(user, path_id, progress_data):
    """Update the user's progress on a specific learning path."""
    user_path_progress, created = UserPathProgress.objects.update_or_create(
        user=user,
        path_id=path_id,
        defaults={'progress': progress_data}
    )
    return user_path_progress

def list_technologies():
    """List all technologies associated with learning paths."""
    return Technology.objects.all()

def recommend_self_paced_courses(user, path_id):
    """Recommend self-paced courses based on the user-selected path."""
    learning_path = get_learning_path_details(path_id)
    if not learning_path:
        return None

    # Example logic to recommend self-paced courses
    recommendations = gemma_api.get_self_paced_courses(user.profile, learning_path)
    return recommendations
