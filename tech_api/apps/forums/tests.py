from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ForumPost, ForumComment
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumPostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post_url = reverse('forum-post-list')

    def test_create_forum_post(self):
        response = self.client.post(self.post_url, {'title': 'Test Post', 'content': 'This is a test content.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForumPost.objects.count(), 1)
        self.assertEqual(ForumPost.objects.get().title, 'Test Post')

    def test_list_forum_posts(self):
        ForumPost.objects.create(title='First Post', content='Content of the first post.')
        ForumPost.objects.create(title='Second Post', content='Content of the second post.')

        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_forum_post(self):
        post = ForumPost.objects.create(title='Post to Retrieve', content='Retrieving this post.')
        url = reverse('forum-post-detail', args=[post.id])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post.title)

    def test_update_forum_post(self):
        post = ForumPost.objects.create(title='Original Title', content='Original content.')
        url = reverse('forum-post-detail', args=[post.id])
        
        response = self.client.put(url, {'title': 'Updated Title', 'content': 'Updated content.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')

    def test_delete_forum_post(self):
        post = ForumPost.objects.create(title='Post to Delete', content='This post will be deleted.')
        url = reverse('forum-post-detail', args=[post.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ForumPost.objects.count(), 0)


class ForumCommentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post = ForumPost.objects.create(title='Post for Comments', content='Content for comments.')
        self.comment_url = reverse('forum-comment-list', args=[self.post.id])

    def test_create_comment(self):
        response = self.client.post(self.comment_url, {'content': 'This is a comment.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForumComment.objects.count(), 1)
        self.assertEqual(ForumComment.objects.get().content, 'This is a comment.')

    def test_list_comments(self):
        ForumComment.objects.create(content='First comment.', post=self.post)
        ForumComment.objects.create(content='Second comment.', post=self.post)

        response = self.client.get(self.comment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_comment(self):
        comment = ForumComment.objects.create(content='Comment to update.', post=self.post)
        url = reverse('forum-comment-detail', args=[comment.id])
        
        response = self.client.put(url, {'content': 'Updated comment.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment.')

    def test_delete_comment(self):
        comment = ForumComment.objects.create(content='Comment to delete.', post=self.post)
        url = reverse('forum-comment-detail', args=[comment.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ForumComment.objects.count(), 0)
