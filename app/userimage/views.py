"""
Vievs for user images API
"""
import os
import uuid
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import UserImage, TemporaryLink
from userimage import serializers

from PIL import Image


def error_message(error_message, status_code):
    """Custom error response"""
    return {
        'message': {'error': _(error_message)},
        'status': status_code
    }


def validate_thumbnail_request(request):
    """Validate thumbnail request send by user"""
    user_tier = request.user.tier
    if not user_tier:
        max_thumbnail_height = 200
        can_see_original = False
    else:
        max_thumbnail_height = user_tier.max_thumbnail_height
        can_see_original = user_tier.can_see_original

    request_image_height = request.query_params.get('image_height')
    print(can_see_original)
    if request_image_height is None and not can_see_original:
        return error_message(
            'Your account tier does not allow you to create thumbnail of that size.',
            status.HTTP_403_FORBIDDEN
        )

    if not request_image_height.isdigit():
        return error_message(
            'The value of "image_height" parameter is not a number',
            status.HTTP_400_BAD_REQUEST
        )

    request_image_height = int(request_image_height)

    if request_image_height > max_thumbnail_height:
        return error_message(
            'Your account tier does not allow to create thumbnails of that size',
            status.HTTP_403_FORBIDDEN
        )


def validate_generate_link_request(request):
    """Validate generate link request send by user"""
    user_tier = request.user.tier
    if not user_tier or not user_tier.can_generate_links:
        return error_message(
            'Your account tier does not allow to create links to this image',
            status.HTTP_403_FORBIDDEN
        )

    request_link_live_time = request.query_params.get('live_time')
    if not request_link_live_time or not request_link_live_time.isdigit():
        return error_message(
            'The value of "live_time" parameter is incorrect',
            status.HTTP_400_BAD_REQUEST
        )

    request_link_live_time = int(request_link_live_time)
    if request_link_live_time < 300 or request_link_live_time > 30000:
        return error_message(
            'You can only create links with live time between 300 and 30000 seconds',
            status.HTTP_400_BAD_REQUEST
        )


class UserImageViewSet(viewsets.ModelViewSet):
    """View for handling user image API"""
    serializer_class = serializers.UserImageSerializer
    queryset = UserImage.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get user images for user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return serializers.ImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new user image"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image"""
        user_image = self.get_object()
        serializer = self.get_serializer(user_image, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, url_path='thumbnail')
    def thumbnail(self, request, pk=None):
        """Get thumbnail image"""
        error = validate_thumbnail_request(request)
        if error:
            return Response(error['message'], status=error['status'])

        request_image_height = int(request.query_params.get('image_height'))
        image = self.get_object().image
        pil_image = Image.open(image.file)
        __, extension = os.path.splitext(image.file.name)
        image_format = UserImage.CONTENT_TYPES[extension[1::]]
        response = HttpResponse(content_type="image/" + image_format)
        thumbnail = pil_image.copy()
        thumbnail.thumbnail((request_image_height, request_image_height))
        thumbnail.save(response, image_format)

        return response

    @action(methods=['GET'], detail=True, url_path='generate-link')
    def fetch_temp_link(self, request, pk=None):
        """Get temporary link to the image"""
        error = validate_generate_link_request(request)
        if error:
            return Response(error['message'], status=error['status'])

        request_link_live_time = int(request.query_params.get('live_time'))
        expiration_time = datetime.now() + timedelta(seconds=request_link_live_time)
        token = uuid.uuid4()
        user_image = self.get_object()
        TemporaryLink.objects.create(
            token=token,
            expiration_time=expiration_time,
            user_image=user_image
        )
        url = get_current_site(request).domain + user_image.image.url + f'?token={token}'
        payload = {'link': 'http://' + url}
        return Response(payload, status=status.HTTP_200_OK)
