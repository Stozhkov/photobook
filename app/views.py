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
        photo = Photo.objects.get(pk=kwargs['pk'])

        if photo.user.id != request.user.id:
            if not photo.is_public:
                return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                Photo.objects.filter(pk=kwargs['pk']).update(view_counter=F('view_counter') + 1)

                PhotoOpening.objects.create(photo=Photo.objects.get(pk=kwargs['pk']))

                queryset = Photo.objects.filter(id=kwargs['pk'])
        else:
            queryset = Photo.objects.filter(id=kwargs['pk'], user=request.user.id)

        serializer = PhotoDetailSerializer(queryset, many=True)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(pk=kwargs['pk'],
                                        user=request.user.id).update(name=request.data['name'])
        if not queryset:
            return Response(data='Error.', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhotoDetailSerializer(queryset, many=True)
            return Response(serializer.data)


class PhotoCreateView(CreateAPIView):
    """
    Class for creating new photo
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoCreateSerializer

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return self.create(request, *args, **kwargs)


class PhotoListView(ListAPIView):
    """
    Class for list view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoListSerializer

    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(user=request.user.id)

        if not queryset:
            return Response(data='No photo for view', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhotoListSerializer(queryset, many=True)
            return Response(serializer.data)


class PublicPhotoListView(PhotoListView):
    """
    Class for public list view
    """

    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.filter(is_public=True)

        if not queryset:
            return Response(data='No photos for view', status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhotoListSerializer(queryset, many=True)
            return Response(serializer.data)
