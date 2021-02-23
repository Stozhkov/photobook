"""
View for "Photo book" project
"""

import logging

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import F

from app.models import Photo, View
from app.serializers import PhotoSerializer, PhotoListSerializer


class PhotoListView(APIView):
    """
    Class for list of photo
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET method
        :param request:
        :return Response:
        """
        queryset = Photo.objects.filter(user=request.user.id)
        serializer_class = PhotoListSerializer(queryset, many=True)

        return Response(serializer_class.data)


class PhotoView(APIView):
    """
    Class for photo
    """
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser, MultiPartParser, FormParser)

    def get(self, request, photo_id=None):
        """
        GET method
        :param request:
        :param photo_id:
        :return Response:
        """
        if photo_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Photo.objects.filter(id=photo_id,
                             user=request.user.id).update(view_counter=F('view_counter') + 1)
        View.objects.create(photo=Photo.objects.get(pk=photo_id))

        queryset = Photo.objects.filter(id=photo_id, user=request.user.id)
        serializer = PhotoSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, photo_id=None):
        """
        POST method
        :param request:
        :param photo_id:
        :return Response:
        """
        if photo_id is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if 'original_file' not in request.data:
            logging.error('File no received')
            raise ParseError('File no received')

        input_data = request.data
        input_data['user'] = request.user.id

        serializer = PhotoSerializer(data=input_data)

        if serializer.is_valid():
            serializer.save()
        else:
            logging.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, photo_id):
        """
        PUT method
        :param request:
        :param photo_id:
        :return Response:
        """
        if photo_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        photo = Photo.objects.filter(id=photo_id,
                                     user=request.user.id).update(name=request.data['name'])

        if not photo:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
