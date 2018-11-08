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
		url(r'^auth/callback/(?P<user_token>.+)$', views.redirectPage, name='redirection'),
	]

# Our Client Id and Client Key
# "_id": "5bd09a7e89128700158c1e94",
#     "email": "anurag.g16@iiits.in",
#     "group": "B01",
#     "callback": "localhost:8000/auth/callback/",
#     "__v": 0,
#     "clientSecret": "27da906cca2278407c4717551f8ccae5d2fb89da47009050f3671245f2a14440f9c282152877f7d6b08d3f19696d94844b9f74ac901752424045f9190910d0bd"
