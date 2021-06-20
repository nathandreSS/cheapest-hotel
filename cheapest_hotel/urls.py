from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from cheapest_hotel.apps.hotel import urls


urlpatterns = [
    path('api/v1/', include(urls.v1_api_urlpatterns)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]



