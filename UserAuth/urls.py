from django.conf.urls import include, url
from . import views
from . import utils
from django.contrib.auth.views import logout

app_name = 'UserAuth'

urlpatterns = [
		url(r'^$', views.landingPage.as_view(), name='landingPage'),
		url(r'^login/$', views.Login.as_view(), name='login'),
		url(r'^signup/$', views.SignUp.as_view(), name='signup'),
		url(r'^signup-user/(?P<type>[\w\-]+)$', views.signupUser.as_view(), name='signup-user'),
		url(r'^login-user/(?P<type>[\w\-]+)', views.LoginUser.as_view(), name='login-user'),
		url(r'^send-verification-data/(?P<user_group>[\w\-]+)/(?P<send_to>[\w\-]+)$', views.send_verification_data, name='send-verification-data'),

		url(r'^show-message/$', utils.show_message, name='show-message'),

		url(r'^logout/$', logout, {'next_page': '/'}, name='logout'), 
	]