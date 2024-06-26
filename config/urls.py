from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls', namespace='users')),
    path('client/', include('client.urls', namespace='client')),
    path('client_service/', include('client_service.urls', namespace='client_service')),
    path('materials/', include('materials.urls', namespace='materials')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)