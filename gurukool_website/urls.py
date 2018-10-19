from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('UserAuth.urls', namespace='UserAuth')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^professor/', include('Professor.urls', namespace="Professor")),
	url(r'^student/', include('Student.urls', namespace="Student")),
    url(r'^api/', include('Api.urls', namespace="Api")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
