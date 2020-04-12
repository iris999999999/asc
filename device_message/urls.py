from django.urls import path
from . import views

app_name = 'device_message'

urlpatterns = [
	path('refresh_page', views.refreshPage, name='refresh_page'),
	path('save_from_html', views.save_from_html, name='save'),
	path('', views.PageBootstrap, name='PageBootstrap'),
]
