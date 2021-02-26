"""
Urls for application app
"""

from django.urls import path
from app.views import PhotoCreateView, PhotoListView, PhotoDetailView


urlpatterns = [
    path('photo/<int:pk>/', PhotoDetailView.as_view()),
    path('photo/create/', PhotoCreateView.as_view()),
    path('', PhotoListView.as_view())
]
