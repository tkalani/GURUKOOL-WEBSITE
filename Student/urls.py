from django.conf.urls import include, url
from . import views

app_name = 'Student'

urlpatterns = [
		url(r'^$', views.dashboard, name='dashboard'),
	]