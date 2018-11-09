from django.conf.urls import include, url
from . import views

app_name = 'Doubt'

urlpatterns = [
    url(r'^course/(?P<course_id>\d+)/$', views.show_doubt, name='doubt-list'),
    url(r'^doubt-detail/(?P<doubt_id>\d+)/$', views.doubt, name='doubt'),
    url(r'^post-comment/(?P<doubt_id>\d+)/$', views.create_comment, name='post-comment'),
    url(r'^$', views.all_doubts, name='index'),
]
