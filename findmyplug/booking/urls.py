from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name = 'register'),
    path('login/', views.LoginAPI.as_view(), name = 'login'),
    path('email-verify/', views.EmailVerify.as_view(), name = 'email-verify'),
]