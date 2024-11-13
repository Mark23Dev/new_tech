from rest_framework import serializers
from .models import ForumPost, ForumComment

class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumComment
        fields = ['id', 'post', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'post', 'created_at', 'updated_at']
