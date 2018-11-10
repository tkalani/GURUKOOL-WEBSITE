from django.conf.urls import include, url
from . import views

app_name = 'Meeting'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^meeting-detail/(?P<meeting_id>\d+)/$', views.meeting_detail, name='meeting-detail'),
    url(r'^meeting-happened/(?P<meeting_id>\d+)/$', views.meeting_happened, name='meeting-happened'),
    url(r'^meeting-not-happened/(?P<meeting_id>\d+)/$', views.meeting_not_happened, name='meeting-not-happened'),
]
