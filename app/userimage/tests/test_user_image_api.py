"""
Test for user image API
"""
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import UserImage, Tier

from userimage.serializers import UserImageSerializer

USER_IMAGES_URL = reverse('userimage:userimage-list')


def detail_url(user_image_id):
    """Create and return user image URL"""
    return reverse('userimage:userimage-detail', args=[user_image_id])


def image_upload_url(user_image_id):
    """Create and upload image and return its URL"""
    return reverse('userimage:userimage-upload-image', args=[user_image_id])


def create_user_image(user, **params):
    """Create and return test user image"""
    defaults = {
        'title': 'Test Title'
    }
    defaults.update(params)

    user_image = UserImage.objects.create(user=user, **defaults)
    return user_image


def create_user(username, password):
    """Create and return new standard user"""
    return get_user_model().objects.create_user(username, password)


def get_thumbnail_url(user_image_id, image_height):
    url = reverse('userimage:userimage-thumbnail', args=[user_image_id])[:-1]
    url += '?image_height=' + str(image_height)
    return url


class UserImageAPITests(TestCase):
    """Tests of user image API calls"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user('TestUser', 'Password1!')
        self.client.force_authenticate(self.user)

    def test_retrieve_user_images(self):
        """Test retieving a list of images which belong to user"""
        user2 = get_user_model().objects.create_user("Test user2", "123456")
        create_user_image(self.user)
        create_user_image(self.user)
        create_user_image(user2)

        response = self.client.get(USER_IMAGES_URL)

        user_images = UserImage.objects.filter(user=self.user).order_by('-id')
        serializer = UserImageSerializer(user_images, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_image_details(self):
        """Test get user image detail without account tier"""
        user_image = create_user_image(user=self.user)
        url = detail_url(user_image.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_image_detail(self):
        """Test get user image detail with tier that allows to see it"""
        tier = Tier.objects.create(name='Test', can_see_original=True)
        self.user.tier = tier
        user_image = create_user_image(user=self.user)

        url = detail_url(user_image.id)
        response = self.client.get(url)

        serializer = UserImageSerializer(user_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_user_image(self):
        """Test crating new user image"""
        payload = {
            'title': 'New image',
        }
        response = self.client.post(USER_IMAGES_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_image = UserImage.objects.get(id=response.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(user_image, k), v)
        self.assertEqual(user_image.user, self.user)

    def test_update_field(self):
        """Test an update of given field of user image"""
        user_image = create_user_image(user=self.user, title="Old title")
        url = detail_url(user_image.id)
        payload = {'title': 'New title'}

        response = self.client.patch(url, payload)
        user_image.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_image.title, payload['title'])

    def test_update_user_of_user_image(self):
        """Test update of image user should not be possible"""
        user2 = create_user('User2', 'Qwerty123456')
        user_image = create_user_image(self.user)
        payload = {'user': user2.id}
        url = detail_url(user_image.id)

        self.client.patch(url, payload)
        user_image.refresh_from_db()

        self.assertEqual(user_image.user, self.user)

    def test_delete_user_image(self):
        """Test deletion of user image"""
        user_image = create_user_image(self.user)
        url = detail_url(user_image.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserImage.objects.filter(id=user_image.id).exists())

    def test_delete_orher_users_image(self):
        """Test deletion of other user's image should not be possible"""
        user2 = create_user('User2', 'Qwerty123456')
        user_image = create_user_image(user2)
        url = detail_url(user_image.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(UserImage.objects.filter(id=user_image.id).exists())


class ImageUploadTests(TestCase):
    """Tests of image upload API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user('Mateusz', 'Password123')
        tier = Tier.objects.create(name='Basic')
        self.user.tier = tier
        self.client.force_authenticate(self.user)
        self.user_image = create_user_image(self.user)

    def tearDown(self):
        self.user_image.image.delete()

    def test_upload_image(self):
        """Test uploading an image"""
        url = image_upload_url(self.user_image.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (25, 25))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            response = self.client.post(url, payload, format='multipart')

        self.user_image.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
        self.assertTrue(os.path.exists(self.user_image.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.user_image.id)
        payload = {'image': 'iNvAlId'}
        response = self.client.post(url, payload, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
