from django.conf.urls import include, url
from . import views

app_name = 'UserAuth'

urlpatterns = [
		url(r'^$', views.landingPage, name='landingPage'),
		url(r'^login/$', views.loginUser, name='login'),
		url(r'^signup/$', views.signupUser, name='signup'),
		url(r'^signup-professor/$', views.signupProfessor, name='signup-professor'),
		url(r'^signup-student/$', views.signupStudent, name='signup-student'),
	]