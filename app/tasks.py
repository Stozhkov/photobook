"""
Tasks for Celery
"""

import datetime
import logging

from io import BytesIO

import boto3
from PIL import Image
from resizeimage import resizeimage

from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count

# from .models import Setting
# from .models import PhotoOpening, Setting, User
from photobook.celery import app


def send_email(subject, message, from_email, to_email):
    """
    Task for sending e-mail
    :param subject:
    :param message:
    :param from_email:
    :param to_email:
    :return:
    """
    try:
        send_mail(subject,
                  message,
                  from_email,
                  [to_email],
                  fail_silently=False)
    except Exception as err:
        logging.warning("Error send e-mail. %s" % err)


def make_small_file(photo_id):
    """
    Task for making small photo
    :param photo_id:
    :return:
    """

    from app.models import Photo

    photo = Photo.objects.get(pk=photo_id)
    image = photo.original_file

    file_name = image.name.split('/')[-1]

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
    file_object = File(thumb_io, name=file_name)

    photo.small_file = file_object
    photo.save()


@app.task
def make_webp_file(photo_id):
    """
    Task for making webp photo.
    :param photo_id:
    :return:
    """

    from app.models import Photo

    photo = Photo.objects.get(pk=photo_id)
    image = photo.original_file

    file_name = image.name.split('/')[-1]

    image_obj = Image.open(image)
    image_obj.convert('RGB')

    thumb_io = BytesIO()
    new_file_name = '.'.join(file_name.split('.')[:-1]) + '.webp'

    image_obj.save(thumb_io, 'webp', quality=90)
    file_object = File(thumb_io, name=new_file_name)

    photo.webp_file = file_object
    photo.save()


@app.task
def make_files(photo_id):
    """
    Task for running "make_small_file" and "make_webp_file" one by one.
    :param photo_id:
    :return:
    """
    make_webp_file(photo_id)
    make_small_file(photo_id)


@app.task(bind=True)
def delete_file_from_s3(self, path: str) -> bool:
    """
    Function for deleting file from AWS S3 storage
    :param self:
    :param path:
    :return:
    """
    try:
        s3_client = boto3.client(
            "s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key='media/' + path
        )

        return True
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task
def choice_top_3(period: str) -> None:
    """
    Choice winner TOP 3.
    :param period: daily or monthly
    :return:
    """
    from .models import PhotoOpening, Setting, User

    if period == 'daily':
        date_start = datetime.datetime.combine(datetime.date.today(),
                                               datetime.datetime.min.time()) - datetime.timedelta(days=1)
        date_stop = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

        date_range = [date_start, date_stop]
        message_template = Setting.objects.get(name='daily_notification')
    else:
        date_stop = datetime.datetime.combine(datetime.date.today().replace(day=1), datetime.datetime.min.time())
        date_start = date_stop - datetime.timedelta(days=1)

        date_range = [
            date_start.replace(day=1),
            date_stop
        ]
        message_template = Setting.objects.get(name='mounthly_notification')

    max_views = PhotoOpening.objects.filter(date_view__range=date_range).\
                    values('photo_id').annotate(views=Count('photo_id')).order_by('-views')[:3]

    for view in max_views:
        user = User.objects.get(photo=view['photo_id'])

        message = str(message_template) % (user.first_name, user.last_name)
        send_email('Your photo in TOP 3', message, 'from@mail.ru', user.email)
