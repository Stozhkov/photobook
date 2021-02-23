"""
Models for "Photo book" project.
"""

from io import BytesIO
from PIL import Image
from resizeimage import resizeimage

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File


class Photo(models.Model):
    """
    This model for photo file.
    """
    name = models.CharField(max_length=150, blank=False)
    original_file = models.ImageField(upload_to='original', default='no-image.png')
    small_file = models.ImageField(upload_to='small', default='no-image.png')
    webp_file = models.ImageField(upload_to='webp', default='no-image.png')
    date_upload = models.DateTimeField(auto_now_add=True)
    view_counter = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.small_file = self.__make_small_file()
        self.webp_file = self.__make_webp_file()

        super().save(*args, **kwargs)

    def __make_small_file(self):

        image = self.original_file

        image_obj = Image.open(image)

        file_format = image_obj.format
        width, height = image_obj.size

        image_obj.convert('RGB')

        if width > height:
            image_obj = resizeimage.resize_width(image_obj, 150)
        else:
            image_obj = resizeimage.resize_height(image_obj, 150)

        thumb_io = BytesIO()

        image_obj.save(thumb_io, file_format, quality=90)
        file_object = File(thumb_io, name=image.name)

        return file_object

    def __make_webp_file(self):

        image = self.original_file

        image_obj = Image.open(image)
        image_obj.convert('RGB')

        thumb_io = BytesIO()
        new_file_name = '.'.join(image.name.split('.')[:-1]) + '.webp'

        image_obj.save(thumb_io, 'webp', quality=90)
        file_object = File(thumb_io, name=new_file_name)

        return file_object

    def __str__(self):
        return str(self.name)


class View(models.Model):
    """
    This model for count views
    """
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_view = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.photo.name} - {self.date_view}'


class Setting(models.Model):
    """
    This model for settings
    """
    name = models.CharField(max_length=25, blank=False)
    value = models.CharField(max_length=250, blank=False)

    def __str__(self):
        return f'{self.name} - {self.value}'
