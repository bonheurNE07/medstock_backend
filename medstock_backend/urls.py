from django.contrib import admin
from django.urls import path, include
from inventory.auth_views import urlpatterns as auth_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('inventory.urls')),
    path('api/auth/', include(auth_urls)),
]
