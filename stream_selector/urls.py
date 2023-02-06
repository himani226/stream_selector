from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('admin/stream/test', admin.site.urls),
    path('',include("streamselect.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    ]

handler404 = 'streamselect.views.error_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

