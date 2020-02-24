from django.urls import path
from . import views

app_name = 'device_message'

urlpatterns = [
	path('', views.messages, name='messages'),
	

]
