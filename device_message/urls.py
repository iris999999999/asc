from django.urls import path
from . import views

app_name = 'device_message'

urlpatterns = [
	path('', views.messages, name='messages'),
	path('save_from_html', views.save_from_html, name='save'),
	path('refreshPage', views.refreshPage, name='refresh_page'),
]
