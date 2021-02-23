# Generated by Django 3.1.6 on 2021-02-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210219_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='small_file',
            field=models.ImageField(default='no-image.png', upload_to='small'),
        ),
        migrations.AddField(
            model_name='photo',
            name='webm_file',
            field=models.ImageField(default='no-image.png', upload_to='webm'),
        ),
    ]
