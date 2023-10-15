"""
Test models
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(username, password):
    """Create and return new standard user"""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user(self):
        "Test creating user"
        username = 'Mateusz'
        password = 'supersecret123'
        user = create_user(username, password)

        self.assertEqual(user.get_username(), username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.tier, None)

    def test_create_user_without_username_raises_error(self):
        with self.assertRaises(ValueError):
            create_user('', 'superSecretPass')

    def test_create_superuser(self):
        """Test creating superuser"""
        user = get_user_model().objects.create_superuser('TestUser', 'secret1!')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_image(self):
        """Test creating new user image is successful"""
        user = create_user('TestUser', 'superSecretPass')
        user_image = models.UserImage.objects.create(user=user, title="Test title")

        self.assertEqual(str(user_image), user_image.title)

    @patch('core.models.uuid.uuid4')
    def test_user_image_file_name_uuid(self, mock_uuid):
        """Test generating path of an image"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, 'test.jpg')

        self.assertEqual(file_path, f'uploads/userimage/{uuid}.jpg')
