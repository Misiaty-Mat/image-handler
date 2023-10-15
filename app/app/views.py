import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from core.models import TemporaryLink, UserImage


@api_view(('GET',))
def serve_media(request, path):
    """Serve media and restrict access to unalowed users"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    file_exist = os.path.exists(file_path) and os.path.isfile(file_path)

    request_token = request.query_params.get('token')
    can_download = False

    if file_exist:
        if request_token:
            link = TemporaryLink.objects.get(token=request_token)
            can_download = link.is_token_valid()

        if not can_download:
            user = get_user_model().objects.filter(username=request.user).first()
            if user:
                can_download = user.tier and user.tier.can_see_original

        if can_download:
            with open(file_path, 'rb') as file:
                __, extension = os.path.splitext(file.name)
                content_type = f'image/{UserImage.CONTENT_TYPES[extension[1::]]}'
                return HttpResponse(file.read(), content_type=content_type)

    payload = {'error': "File does not exist or you have no permission to see it"}
    return Response(payload, status=status.HTTP_400_BAD_REQUEST)
