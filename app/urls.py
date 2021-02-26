"""
Urls for application app
"""

from django.urls import path
from app.views import PhotoViewCreate, PhotoViewList, PhotoViewUpdate


urlpatterns = [
    path('photo/<int:pk>/', PhotoViewUpdate.as_view()),
    path('photo/create/', PhotoViewCreate.as_view()),
    path('', PhotoViewList.as_view())
]
