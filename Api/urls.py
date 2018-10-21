from django.conf.urls import include, url
from .views import CourseList, DoubtCreate, CommentCreate, CourseDoubt

app_name = 'Api'

urlpatterns = [
		url(r'^courses/(?P<type>[\w\-]+)/$', CourseList.as_view(), name='course-list'),
        url(r'^doubts/$', DoubtCreate.as_view(), name='doubt'),
		url(r'^courses/(?P<course_id>\d+)/doubts/$', CourseDoubt.as_view(), name='course-doubt'),
		url(r'^comments/(?P<doubt_id>\d+)/$', CommentCreate.as_view(), name='comment'),
	]
