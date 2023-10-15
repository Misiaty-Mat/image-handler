"""
Test for the Django admin page capabilities
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Tier


class AdminSiteTests(TestCase):
    """Test for Django Admin"""

    def setUp(self):
        """Set up resources before tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser('Admin321', 'superSecret123')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username='mateusz',
            password='123456',
            tier=Tier.objects.get(name='Basic')
        )

    def test_users_list(self):
        """Test user listing"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.tier)

    def test_edit_user(self):
        """Test edit user page funtionality"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test create user page"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
