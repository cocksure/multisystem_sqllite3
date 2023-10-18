from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/depo/', include('depo.urls')),
    path('api/info/', include('info.urls')),
    path('api/hr/', include('hr.urls')),
    path('api/users/', include('users.urls')),
    path('api/purchase/', include('users.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)