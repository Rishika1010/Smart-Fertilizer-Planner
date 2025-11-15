"""
URL configuration for fertilizer_planner project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('parcels/', include('parcels.urls')),
    path('fertilizers/', include('fertilizers.urls')),
    path('reports/', include('reports.urls')),
]

admin.site.site_header = "Smart Fertilizer Planner Administration"
admin.site.site_title = "Fertilizer Planner Admin"
admin.site.index_title = "Welcome to Smart Fertilizer Planner Admin"

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

