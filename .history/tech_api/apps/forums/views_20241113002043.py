from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import ForumPost, ForumComment
from .serializers import ForumPostSerializer, ForumCommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# Forum Post Views

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user as the author of the post
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_post(self, request, pk=None):
        # Delete the post instance and return HTTP 204
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Forum Comment Views

class ForumCommentViewSet(viewsets.ModelViewSet):
    queryset = ForumComment.objects.all()  # Define the queryset here
    serializer_class = ForumCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return ForumComment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(ForumPost, id=post_id)
        serializer.save(author=self.request.user, post=post)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_comment(self, request, pk=None):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
