from django.contrib import admin
from django.urls import path

from creator_video.views import download_video, index

urlpatterns = [
    path('', index),
    path('<str:message>', download_video, name='download_video'),
    path('admin/', admin.site.urls),
]
