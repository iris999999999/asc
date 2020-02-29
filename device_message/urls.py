from django.urls import path
from . import views

app_name = 'device_message'

urlpatterns = [
	path('', views.messages, name='messages'),
	#path('save', views.save_report_from_button, name='save_report'),
	path('index', views.index, name='hello'),
	path('return_', views.return_, name='return'),
	

]
