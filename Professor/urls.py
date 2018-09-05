from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout

app_name = 'Professor'

urlpatterns = [
		url(r'^$', views.dashboard, name='dashboard'),
		url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
	]