from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import LearningPath, UserPathProgress
from .services import recommend_self_paced_courses

@receiver(post_save, sender=UserPathProgress)
def update_learning_path_progress(sender, instance, created, **kwargs):
    """
    Triggered when a UserPathProgress instance is saved. If progress is updated,
    it checks if the path is complete and performs additional actions, like recommending further courses.
    """
    if instance.progress == 100:  # Assuming progress is stored as a percentage
        # Notify or recommend further courses
        self_paced_recommendations = recommend_self_paced_courses(instance.user, instance.path.id)
        # Example logging or storing recommendations
        print(f"Recommendations for user {instance.user}: {self_paced_recommendations}")

@receiver(post_save, sender=LearningPath)
def create_initial_user_progress(sender, instance, created, **kwargs):
    """
    Triggered when a new LearningPath is created. Initializes a UserPathProgress record for tracking.
    """
    if created:
        # Create initial progress entry for each user in the path
        UserPathProgress.objects.create(user=instance.user, path=instance, progress=0)
