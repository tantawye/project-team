from django.urls import path

from .views import api2,ObjectDetectionView2

urlpatterns = [
    path('',api2),
    path('s/',ObjectDetectionView2)

]



