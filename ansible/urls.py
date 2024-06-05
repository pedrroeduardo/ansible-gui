# ansible/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path('ws/', include('core.routing')),
]

admin.site.site_header = 'TFBern Ansible - Verwaltung'
