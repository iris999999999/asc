from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('device_message.urls', namespace='device_message')),
    
    ]
