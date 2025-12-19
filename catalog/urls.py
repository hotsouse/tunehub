from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django_prometheus import exports as prometheus_exports
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('', views.home, name='home'),
    path('api/', include('api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('metrics/', prometheus_exports.ExportToDjangoView, name='metrics'),
    path('accounts/', include('accounts.urls')),
    path('music/', include('music.urls')),
    path('movies/', include('movies.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
