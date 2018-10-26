from django.conf.urls import include, url
from .views import *
from . import views

app_name = 'Api'

urlpatterns = [
		url(r'^login/$', Login.as_view(), name='login'),
		url(r'^courses/(?P<type>[\w\-]+)/(?P<menu>[\w\-]+)/$', CourseList.as_view(), name='course-list'),
        url(r'^doubts/(?P<course_id>\d+)/$', DoubtCreate.as_view(), name='doubt'),
		url(r'^courses/(?P<course_id>\d+)/doubts/$', CourseDoubt.as_view(), name='course-doubt'),
		url(r'^comments/(?P<doubt_id>\d+)/$', CommentCreate.as_view(), name='comment'),
		url(r'^quiz-details/(?P<quiz_id>[\w\-]+)/$', QuizDetails.as_view(), name='quiz-details'),
		url(r'^check-quiz/(?P<quiz_id>[\w\-]+)/(?P<course_id>[\w\-]+)/$', CheckQuiz.as_view(), name='check-quiz'),
		url(r'^comment-on-doubt/$', CommentOnDoubt.as_view(), name='comment-on-doubt'),
		url(r'^quiz-complete/$', QuizComplete.as_view(), name='quiz-complete'),
		url(r'^meeting/(?P<type>[\w\-]+)/$',MeetingManage.as_view(), name='meeting-create'),
		# url(r'^test/$', views.Test, name='test'),
	]
