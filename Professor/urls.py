from django.conf.urls import include, url
from . import views

app_name = 'Professor'

urlpatterns = [
		url(r'^$', views.dashboard, name='dashboard'),
		url(r'^create-poll/$', views.create_poll, name='create-poll'),
		url(r'^poll/(?P<poll_id>\d+)/$', views.show_poll, name='poll'),
		url(r'^poll/$', views.show_all_polls, name='all-poll'),
		url(r'^quiz/$', views.show_all_quiz, name='all-quiz'),
		url(r'^create-quiz/$', views.create_quiz, name='create-quiz'),
		url(r'^quiz/(?P<quiz_id>\d+)/$', views.show_quiz, name='quiz'),
		url(r'^conduct-quiz/(?P<quiz_id>\d+)/$', views.conduct_quiz, name='conduct-quiz'),
		url(r'^stop-quiz/(?P<quiz_id>\d+)/$', views.stop_quiz, name='stop-quiz'),
		url(r'^conduct-poll/(?P<poll_id>\d+)/$', views.conduct_poll, name='conduct-poll'),
		url(r'^stop-poll/(?P<poll_id>\d+)/$', views.stop_poll, name='stop-poll'),
		url(r'^conducted-poll/(?P<poll_id>\d+)/$', views.conducted_poll, name='conducted-poll'),
		url(r'^conducted-quiz/(?P<quiz_id>\d+)/$', views.conducted_quiz, name='conducted-quiz'),
		url(r'^quiz-result/(?P<quiz_id>\d+)/$', views.quiz_result, name='quiz-result'),
		url(r'^view-quiz-responses/(?P<quiz_id>\d+)/$', views.view_quiz_reponses, name='view-quiz-responses'),
		url(r'^question-wise-result/$', views.question_wise_result, name='question-wise-result'),
		url(r'^quiz-result-pdf/(?P<quiz_id>\d+)/$', views.quiz_result_pdf, name='quiz-result-pdf'),
		url(r'^quiz-result-csv/(?P<quiz_id>\d+)/$', views.quiz_result_csv, name='quiz-result-csv'),
	]
