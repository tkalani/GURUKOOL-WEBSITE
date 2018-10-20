from django.conf.urls import include, url
from . import views

app_name = 'Professor'

urlpatterns = [
		url(r'^$', views.dashboard, name='dashboard'),
		url(r'^create-poll/$', views.create_poll, name='create-poll'),
		url(r'^poll/(?P<poll_id>\d+)/$', views.show_poll, name='poll'),
		url(r'^create-quiz/$', views.create_quiz, name='create-quiz'),
		url(r'^quiz/(?P<quiz_id>\d+)/$', views.show_quiz, name='quiz'),
		url(r'^doubt/(?P<course_id>\d+)/$', views.show_doubt, name='doubt-list'),
	]
