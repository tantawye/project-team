from django.urls import path
from.views import ObjectDetectionView
urlpatterns = [
    path('', ObjectDetectionView),
]
