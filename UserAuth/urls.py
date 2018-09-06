from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'UserAuth'

urlpatterns = [
		url(r'^$', views.landingPage, name='landingPage'),
		url(r'^login/$', views.loginUser, name='login'),
		url(r'^signup/$', views.signupUser, name='signup'),
		url(r'^signup-professor/$', views.signupProfessor, name='signup-professor'),
		url(r'^signup-student/$', views.signupStudent, name='signup-student'),
		url(r'^login-professor/$', views.loginProfessor, name='login-professor'),
		url(r'^login-student/$', views.loginStudent, name='login-student'),

		url(r'^show-error/$', views.showError, name='show-error'),
	]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)