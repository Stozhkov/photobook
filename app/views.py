"""
View for "Photo book" project
"""

import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView

from app.models import Photo
from .serializers import PhotoDetailSerializer, PhotoListSerializer, PhotoCreateSerializer


class PhotoViewUpdate(RetrieveUpdateAPIView):
    """
    Class for update photo name and detail view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()


class PhotoViewCreate(CreateAPIView):
    """
    Class for creating new photo
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoCreateSerializer


class PhotoViewList(ListAPIView):
    """
    Class for list view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoListSerializer
    queryset = Photo.objects.all()
