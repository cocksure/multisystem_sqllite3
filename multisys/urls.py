from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MultiSystem",
        default_version='v1',
        description='Universal Project',
        terms_of_service='demo.uz',
        contact=openapi.Contact(email='sanjarwer93@gmail.com'),
        license=openapi.License(name="demo license")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/depo/', include('depo.urls')),
    path('api/info/', include('info.urls')),
    path('api/hr/', include('hr.urls')),
    path('api/users/', include('users.urls')),
    path('api/purchase/', include('purchase.urls')),
    path('api/shared/', include('shared.urls')),

    # dj-rest-auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('dj_rest_auth.urls')),
    path('api/rest-auth/registration', include('dj_rest_auth.registration.urls')),



    # swagger
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='swagger-swagger-ui')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
