"""
View for "Photo book" project
"""

import logging

from django.db.models import F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from app.models import Photo, PhotoOpening
from .serializers import PhotoDetailSerializer, PhotoListSerializer, PhotoCreateSerializer


class PhotoDetailView(RetrieveUpdateDestroyAPIView):
    """
    Class for update photo name and detail view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()

    def get(self, request, *args, **kwargs):
        # Increase counter
        Photo.objects.filter(pk=kwargs['pk'], user=request.user.id).\
            update(view_counter=F('view_counter') + 1)
        # Write photo views in IsAuthenticatede
        try:
            PhotoOpening.objects.create(photo=Photo.objects.get(pk=kwargs['pk']))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset = Photo.objects.filter(id=kwargs['pk'], user=request.user.id)
        serializer = PhotoDetailSerializer(queryset, many=True)

        return Response(serializer.data)


class PhotoCreateView(CreateAPIView):
    """
    Class for creating new photo
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoCreateSerializer


class PhotoListView(ListAPIView):
    """
    Class for list view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoListSerializer
    queryset = Photo.objects.all()
