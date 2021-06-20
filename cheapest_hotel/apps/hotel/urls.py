from rest_framework.routers import DefaultRouter

from django.urls import include, path

from hotel import views

app_name = 'hotel'

router = DefaultRouter()
router.register(r'hotel', views.HotelViewSet)
router.register(r'tax', views.TaxViewSet)

v1_api_urlpatterns = [
    path('', include(router.urls)),
    path('cheapest/', views.Cheapest.as_view(), name='cheapest')
]