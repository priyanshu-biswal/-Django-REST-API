from datetime import datetime, time, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import BlogPost

class BlogPostAPITests(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create test posts for user1
        self.post1 = BlogPost.objects.create(
            title='First Post',
            content='Content for first post',
            author=self.user1
        )
        self.post2 = BlogPost.objects.create(
            title='Second Post',
            content='Django REST Framework testing',
            author=self.user1
        )

        # Create test post for user2
        self.post3 = BlogPost.objects.create(
            title='User2 Post',
            content='Content belonging to user 2',
            author=self.user2
        )

        self.list_url = reverse('post-list')
        self.detail_url = lambda pk: reverse('post-detail', kwargs={'pk': pk})

    def test_unauthenticated_access_denied(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_only_see_own_posts(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination total count
        self.assertEqual(response.data['count'], 2)

    def test_create_post(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Post',
            'content': 'This is a test post content'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'user1')

    def test_user_cannot_access_other_users_post(self):
        self.client.force_authenticate(user=self.user1)
        # Try to access user2's post
        response = self.client.get(self.detail_url(self.post3.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_post(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'Updated First Post',
            'content': 'Updated content'
        }
        response = self.client.put(self.detail_url(self.post1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated First Post')

    def test_delete_own_post(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url(self.post1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_posts(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"{self.list_url}?search=Framework")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Second Post')

    def test_filter_posts_by_creation_date(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        BlogPost.objects.filter(pk=self.post2.pk).update(
            created_at=timezone.make_aware(
                datetime.combine(yesterday, time.min)
            )
        )
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            self.list_url,
            {'created_at': timezone.localdate().isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.post1.id)

    def test_ordering_by_id(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.list_url, {'ordering': '-id'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [post['id'] for post in response.data['results']],
            [self.post2.id, self.post1.id],
        )

    def test_pagination_is_fixed_at_five_posts(self):
        for index in range(6):
            BlogPost.objects.create(
                title=f'Extra Post {index}',
                content='Extra content',
                author=self.user1,
            )
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.list_url, {'page_size': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 8)
        self.assertEqual(len(response.data['results']), 5)

    def test_token_authentication(self):
        response = self.client.post(
            reverse('api-token-auth'),
            {'username': 'user1', 'password': 'password123'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data['token']}"
        )
        posts_response = self.client.get(self.list_url)
        self.assertEqual(posts_response.status_code, status.HTTP_200_OK)

    def test_api_responses_are_json(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.list_url)

        self.assertEqual(response['Content-Type'], 'application/json')