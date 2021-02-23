"""
Urls for application app
"""

from django.urls import path
from app.views import PhotoListView, PhotoView


urlpatterns = [
    path('list/', PhotoListView.as_view(), name='all-photo'),
    path('photo/<photo_id>/', PhotoView.as_view(), name='photo'),
    path('photo/', PhotoView.as_view(), name='photo'),
]
