from django.conf.urls import include, url
from . import views
from . import utils
from django.conf.urls.static import static
from django.conf import settings

app_name = 'UserAuth'

urlpatterns = [
		url(r'^$', views.landingPage.as_view(), name='landingPage'),
		url(r'^login/$', views.Login.as_view(), name='login'),
		url(r'^signup/$', views.SignUp.as_view(), name='signup'),
		url(r'^signup-user/(?P<type>[\w\-]+)$', views.signupUser.as_view(), name='signup-user'),
		url(r'^login-user/(?P<type>[\w\-]+)', views.LoginUser.as_view(), name='login-user'),

		url(r'^show-message/$', utils.show_message, name='show-message'),
	]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)