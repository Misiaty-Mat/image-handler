"""
Serializers for user image API
"""
from rest_framework import serializers

from core.models import UserImage


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for user images"""

    class Meta:
        model = UserImage
        fields = ['id', 'title', 'image']
        read_only_fields = ['id']


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to user"""

    class Meta:
        model = UserImage
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
