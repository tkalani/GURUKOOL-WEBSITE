from django.conf.urls import include, url
from .views import CourseList, DoubtCreate

app_name = 'Api'

urlpatterns = [
		url(r'^courses/$', CourseList.as_view(), name='course-list'),
        url(r'^doubts/$', DoubtCreate.as_view(), name='doubt'),
	]
