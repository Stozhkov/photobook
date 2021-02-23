"""
Serializers for "Photo book" project
"""

from django.conf import settings
from rest_framework import serializers
from app.models import Photo


class PhotoListSerializer(serializers.ModelSerializer):
    """
    Serializer for list view
    """
    class Meta:
        """
        Meta class
        """
        model = Photo
        read_only_fields = ('view_counter', 'date_upload')
        fields = ('id', 'name', 'small_file', 'user', 'view_counter')


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializer for one photo
    """
    def validate(self, attrs):

        file_name = str(attrs['original_file'])
        file_extension = file_name.split('.')[-1]

        if file_extension.lower() not in ['png', 'jpg', 'jpeg']:
            raise serializers.ValidationError('Wrong file type.')

        if len(attrs['original_file']) > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError('File too large.')

        return attrs

    class Meta:

        """
        Meta class
        """
        model = Photo
        read_only_fields = ('view_counter', 'date_upload')
        fields = ('id', 'name', 'original_file', 'small_file', 'webp_file', 'user', 'view_counter')
