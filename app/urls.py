"""
Urls for application app
"""

from django.urls import path
from app.views import PhotoCreateView, PhotoListView, PhotoDetailView, PublicPhotoListView, PhotoChangePrivacy


urlpatterns = [
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),
    path('photo/<int:pk>/change_privacy/', PhotoChangePrivacy.as_view()),
    path('photo/create/', PhotoCreateView.as_view()),
    path('public/', PublicPhotoListView.as_view()),
    path('', PhotoListView.as_view())
]
