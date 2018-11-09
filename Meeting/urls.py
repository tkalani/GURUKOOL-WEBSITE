from django.conf.urls import include, url
from . import views

app_name = 'Meeting'

urlpatterns = [
    url(r'^meeting-detail/(?P<meeting_id>\d+)/$', views.meeting_detail, name='meeting-detail'),
    url(r'^', views.index, name='index'),
]
