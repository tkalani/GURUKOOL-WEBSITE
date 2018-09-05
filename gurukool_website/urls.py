from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('UserAuth.urls', namespace='UserAuth')),
    url(r'^professor/', include('Professor.urls', namespace="Professor")),
	url(r'^student/', include('Student.urls', namespace="Student")),
]
