from django.conf.urls import include, url
from . import views

app_name = 'Doubt'

urlpatterns = [
    url(r'^course/(?P<course_id>\d+)/$', views.show_doubt, name='doubt-list'),
]
