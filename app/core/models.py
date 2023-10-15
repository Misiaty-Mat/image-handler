"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator
from django.utils import timezone


def user_image_file_path(instance, filename):
    """Generate file path for new user image"""
    extension = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{extension}'

    return os.path.join('uploads', 'userimage', filename)


class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self, username, password=None, **extra_fields):
        """Create new user, store in database and return it"""
        if not username:
            raise ValueError('User need to have an username.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Create and return superuser"""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """System user"""
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tier = models.ForeignKey('Tier', on_delete=models.SET_NULL, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Tier(models.Model):
    """Account tier model"""
    name = models.CharField(max_length=50, unique=True)
    max_thumbnail_height = models.PositiveIntegerField(
        default=200,
        validators=[MinValueValidator(1)]
    )
    can_see_original = models.BooleanField(default=False)
    can_generate_links = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class UserImage(models.Model):
    """User image object"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=user_image_file_path)

    CONTENT_TYPES = {
        'png': 'png',
        'jpg': 'jpeg'
    }

    def __str__(self) -> str:
        return self.title


class TemporaryLink(models.Model):
    "Temporary link access to image model"
    token = models.CharField(max_length=50, unique=True)
    expiration_time = models.DateTimeField()
    user_image = models.ForeignKey('UserImage', on_delete=models.CASCADE)

    def is_token_valid(self):
        return timezone.now() < self.expiration_time
