from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('1/', include('organizations.urls', namespace='organizations')),
    path('', include('device_message.urls', namespace='device_message'))


] 
