from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include,url

router = DefaultRouter()
router.register(r'vehicles', views.VehicleDetails)
router.register(r'bookings', views.BookingAPI)
router.register(r'station', views.StationAPI)
router.register(r'slot-create', views.SlotCreateAPI)

urlpatterns = [
    url('', include(router.urls)),
    path('register/', views.RegisterAPI.as_view(), name = 'register'),
    path('login/', views.LoginAPI.as_view(), name = 'login'),
    path('email-verify/', views.EmailVerify.as_view(), name = 'email-verify'),
    path('slot/', views.SlotAPI.as_view(), name = 'slot'),
]