from django.urls import path
from . import views

app_name = 'ornizations'

urlpatterns = [
	path('', views.organization_views, name='organization_views'),
	

]
