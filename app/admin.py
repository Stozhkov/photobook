"""
Config admin panel
"""

from django.contrib import admin
from app.models import Photo, View, Setting


admin.site.register((Photo, View, Setting))
