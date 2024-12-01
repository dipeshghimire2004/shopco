from django.urls import path
from .views import  GoogleLoginAPIView
from . import views

urlpatterns = [
    path('', views.api_home, name='api_home'),  # Handles the /api/ endpoint
    path('register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('google/', GoogleLoginAPIView.as_view(), name='googlelogin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
]
