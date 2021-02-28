"""
Config admin panel
"""

from django.contrib import admin
from app.models import Photo, PhotoOpening, Setting


admin.site.register((Photo, PhotoOpening, Setting))
