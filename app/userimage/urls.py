"""
URL mapping for user images
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from userimage import views


router = DefaultRouter()
router.register('userimage', views.UserImageViewSet)

app_name = 'userimage'
urlpatterns = [path('', include(router.urls))]
