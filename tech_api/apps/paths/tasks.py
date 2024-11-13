from celery import shared_task
from django.contrib.auth.models import User
from .models import LearningPath, UserPathProgress
from .services import generate_learning_path, recommend_self_paced_courses

@shared_task
def generate_path_for_user(user_id, preferences):
    """
    Task to generate a personalized learning path for a user based on preferences.
    This is useful for generating paths in the background and avoiding long wait times.
    """
    user = User.objects.get(id=user_id)
    new_path = generate_learning_path(user, preferences)
    # Additional processing or logging can go here
    return f"Generated path {new_path.id} for user {user.username}"

@shared_task
def update_user_progress(user_id, path_id, progress):
    """
    Task to update the user’s progress on a learning path and perform any related actions
    (e.g., check completion and send recommendations if completed).
    """
    try:
        progress_record = UserPathProgress.objects.get(user_id=user_id, path_id=path_id)
        progress_record.progress = progress
        progress_record.save()

        # If path completed, recommend self-paced courses
        if progress == 100:
            recommendations = recommend_self_paced_courses(user_id, path_id)
            # Example: save recommendations to a log or notify user
            print(f"Recommendations for user {user_id}: {recommendations}")
    except UserPathProgress.DoesNotExist:
        print(f"No progress record found for user {user_id} on path {path_id}")
    return f"Progress updated to {progress}% for user {user_id} on path {path_id}"

@shared_task
def send_progress_reminders():
    """
    Task to send reminders to users who haven’t updated their learning path progress recently.
    This can run on a daily or weekly schedule.
    """
    # Example logic to fetch users with outdated progress updates
    inactive_users = UserPathProgress.objects.filter(last_updated__lt=timezone.now() - timedelta(days=7))
    for record in inactive_users:
        user = record.user
        # Send notification or email reminder (pseudo-code)
        print(f"Sending reminder to user {user.username} for path {record.path.id}")
    return "Progress reminders sent to inactive users."
