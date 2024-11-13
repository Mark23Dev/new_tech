from celery import shared_task
from .models import ForumPost, ForumComment
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def notify_users_of_new_post(post_id):
    """
    Notify users of a new forum post via email or any other notification system.
    """
    try:
        post = ForumPost.objects.get(id=post_id)
        # Logic to notify users (e.g., sending emails)
        # This is a placeholder for actual notification logic
        logger.info(f"Notified users of new post: {post.title}")
    except ForumPost.DoesNotExist:
        logger.error(f"ForumPost with id {post_id} does not exist.")


@shared_task
def archive_old_comments():
    """
    Archive comments that are older than a certain threshold (e.g., 1 year).
    """
    one_year_ago = timezone.now() - timezone.timedelta(days=365)
    old_comments = ForumComment.objects.filter(created_at__lt=one_year_ago)

    for comment in old_comments:
        # Logic to archive comment
        # This is a placeholder for actual archiving logic
        comment.is_archived = True
        comment.save()
        logger.info(f"Archived comment: {comment.content} from post {comment.post.title}")

